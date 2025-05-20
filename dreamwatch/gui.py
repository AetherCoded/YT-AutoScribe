from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget


def run_gui():
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("YT-AutoScribe")
    window.show()
    app.exec()
