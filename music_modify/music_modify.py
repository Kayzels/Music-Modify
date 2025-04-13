import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from music_modify.gui.window_main import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
