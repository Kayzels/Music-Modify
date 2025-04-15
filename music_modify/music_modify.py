import datetime
import os
from os import PathLike
from pathlib import Path
import sys
import time
from typing import Final

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QProgressDialog
from music_modify.gui import Ui_MainWindow
from music_modify.models import SongTableModel, SongRepository
from music_modify.utils import formatTime


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]

        self.songs_repository: Final[SongRepository] = SongRepository()
        self.songs_model: Final[SongTableModel] = SongTableModel(self.songs_repository)
        self.files_table_view.setModel(self.songs_model)
        self.files_table_view.resizeColumnsToContents()

        self.action_add_files.triggered.connect(
            lambda: self.openAddDialog(QFileDialog.FileMode.ExistingFiles)
        )
        self.action_add_folder.triggered.connect(
            lambda: self.openAddDialog(QFileDialog.FileMode.Directory)
        )

    def openAddDialog(self, file_mode: QFileDialog.FileMode):
        files_dialog = QFileDialog(self)
        files_dialog.setFileMode(file_mode)
        if file_mode == QFileDialog.FileMode.ExistingFiles:
            files_dialog.setNameFilter("MP3 Files (*.mp3)")
        if files_dialog.exec():
            if file_mode == QFileDialog.FileMode.ExistingFiles:
                file_names: list[str] = files_dialog.selectedFiles()
                self.addFiles(file_names)
            elif file_mode == QFileDialog.FileMode.Directory:
                folder = files_dialog.selectedFiles()[0]
                files_in_folder = self.getFolderFiles(folder)
                self.addFiles(files_in_folder)

    def getFolderFiles(self, folder: str | PathLike[str]) -> list[str]:
        songs: list[str] = []
        progress_dialog = QProgressDialog(
            "Adding Folders...", "Cancel", 0, 1, parent=self
        )
        for folder_name, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".mp3"):
                    songs.append(str(Path(folder_name, file)))
                    progress_dialog.setLabelText(f"{len(songs)} found.")
            if progress_dialog.wasCanceled():
                break
        progress_dialog.setValue(1)
        return songs

    def addFiles(self, files: list[str] | list[PathLike[str]]):
        start_time = time.time()
        progress_dialog = QProgressDialog(
            "Adding Files...", "Cancel", 0, len(files), parent=self
        )
        progress_dialog.setModal(True)
        progress_dialog.setMinimumDuration(2)
        progress_dialog.setWindowTitle("Add Files")
        for index, file in enumerate(files):
            progress_dialog.setValue(index)
            self.songs_repository.addFile(file)
            time_taken_seconds: float = time.time() - start_time
            time_taken: str = formatTime(datetime.timedelta(seconds=time_taken_seconds))
            estimated_time: float = (time_taken_seconds / (index + 1)) * len(files)
            eta_delta: str = formatTime(datetime.timedelta(seconds=estimated_time))
            label_text: str = (
                f"{index}/{len(files)}\nTime Taken: {time_taken}\nETA: {eta_delta}"
            )
            progress_dialog.setLabelText(label_text)
            if progress_dialog.wasCanceled():
                break
        progress_dialog.setValue(len(files))


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Kayzels")
    app.setApplicationName("Music Modify")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
