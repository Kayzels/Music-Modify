import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from music_modify.gui import Ui_MainWindow
from music_modify.models import SongTableModel, SongRepository
from typing import Final


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]

        self.songs_repository: Final[SongRepository] = SongRepository()
        self.songs_model: Final[SongTableModel] = SongTableModel(self.songs_repository)
        self.files_table_view.setModel(self.songs_model)
        self.files_table_view.resizeColumnsToContents()


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Kayzels")
    app.setApplicationName("Music Modify")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
