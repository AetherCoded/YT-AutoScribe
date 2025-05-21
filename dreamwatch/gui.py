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
)

from .downloader import download_batch


class DownloaderWidget(QWidget):
    """UI for downloading YouTube audio."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        url_row = QHBoxLayout()
        url_row.addWidget(QLabel("Playlist/URL:"))
        self.url_edit = QLineEdit()
        url_row.addWidget(self.url_edit)
        layout.addLayout(url_row)

        date_row = QHBoxLayout()
        date_row.addWidget(QLabel("From:"))
        self.from_edit = QLineEdit()
        date_row.addWidget(self.from_edit)
        date_row.addWidget(QLabel("To:"))
        self.to_edit = QLineEdit()
        date_row.addWidget(self.to_edit)
        layout.addLayout(date_row)

        dst_row = QHBoxLayout()
        dst_row.addWidget(QLabel("Destination:"))
        self.dst_edit = QLineEdit(str(Path("downloads")))
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

    def _start_download(self) -> None:
        """Trigger download using parameters from the form."""

        url = self.url_edit.text().strip()
        if not url:
            return
        date_from = self.from_edit.text().strip()
        date_to = self.to_edit.text().strip()
        dst = Path(self.dst_edit.text().strip())
        download_batch(url, date_from or None, date_to or None, dst)


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
