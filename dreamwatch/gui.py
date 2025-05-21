"""Basic GUI for YT-AutoScribe."""

from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QDateEdit,
)
from PySide6.QtCore import QDate

from .downloader import download_batch, validate_url


class DownloaderWidget(QWidget):
    """UI for downloading YouTube audio."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        url_row = QHBoxLayout()
        url_row.addWidget(QLabel("Playlist/URL:"))
        self.url_edit = QLineEdit()
        # validate URL as the user types
        self.url_edit.textChanged.connect(self._check_url)
        self.url_edit.editingFinished.connect(self._check_url)
        url_row.addWidget(self.url_edit)
        self.url_status = QLabel()
        url_row.addWidget(self.url_status)
        layout.addLayout(url_row)

        date_row = QHBoxLayout()
        date_row.addWidget(QLabel("From:"))
        self.from_edit = QDateEdit(calendarPopup=True)
        self.from_edit.setDisplayFormat("MM-dd-yyyy")
        # Start with blank text
        self.from_edit.setSpecialValueText("")
        self.from_edit.setDate(self.from_edit.minimumDate())
        date_row.addWidget(self.from_edit)
        date_row.addWidget(QLabel("To:"))
        self.to_edit = QDateEdit(calendarPopup=True)
        self.to_edit.setDisplayFormat("MM-dd-yyyy")
        self.to_edit.setSpecialValueText("")
        self.to_edit.setDate(self.to_edit.minimumDate())
        date_row.addWidget(self.to_edit)
        today_btn = QPushButton("Today")
        today_btn.clicked.connect(lambda: self.to_edit.setDate(QDate.currentDate()))
        date_row.addWidget(today_btn)
        layout.addLayout(date_row)

        dst_row = QHBoxLayout()
        dst_row.addWidget(QLabel("Destination:"))
        self.dst_edit = QLineEdit(str(Path("downloads") / "NewProject"))
        browse = QPushButton("Browse")
        browse.clicked.connect(self._browse)
        dst_row.addWidget(self.dst_edit)
        dst_row.addWidget(browse)
        layout.addLayout(dst_row)

        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self._start_download)
        layout.addWidget(self.download_btn)

    def _browse(self) -> None:
        """Open folder selection dialog."""

        folder = QFileDialog.getExistingDirectory(self, "Select download folder")
        if folder:
            self.dst_edit.setText(folder)

    def _check_url(self) -> None:
        """Validate the URL and update destination if valid."""

        url = self.url_edit.text().strip()
        if not url:
            self.url_status.setText("")
            return
        valid, folder = validate_url(url)
        if valid:
            self.url_status.setText("\u2705")  # check mark
            proj_dir = Path("downloads") / (folder or "NewProject")
            self.dst_edit.setText(str(proj_dir))
        else:
            self.url_status.setText("\u274c")  # red cross

    def _start_download(self) -> None:
        """Trigger download using parameters from the form."""

        url = self.url_edit.text().strip()
        if not url:
            return
        # Only pass dates if the fields are not blank
        date_from = None
        if self.from_edit.text().strip():
            date_from = self.from_edit.date().toString("yyyyMMdd")
        date_to = None
        if self.to_edit.text().strip():
            date_to = self.to_edit.date().toString("yyyyMMdd")
        dst = Path(self.dst_edit.text().strip())
        download_batch(url, date_from, date_to, dst)


class MainWindow(QMainWindow):
    """Main application window with placeholder tabs."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("YT-AutoScribe")

        tabs = QTabWidget()
        tabs.addTab(DownloaderWidget(), "Download")
        tabs.addTab(QWidget(), "Transcribe")  # placeholders for future panes
        tabs.addTab(QWidget(), "Subtitles")
        self.setCentralWidget(tabs)


def run_gui() -> None:
    """Run the Qt event loop with the main window."""

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
