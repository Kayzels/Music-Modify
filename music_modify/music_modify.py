import datetime
import os
from os import PathLike
from pathlib import Path
import sys
import time
from typing import Final, cast

from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QProgressDialog,
)
from PySide6.QtCore import QModelIndex, QSortFilterProxyModel
from music_modify.gui import Ui_MainWindow
from music_modify.models import SongTableModel, SongRepository
from music_modify.utils import formatTime, updateTableView


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]

        self.songs_repository: Final[SongRepository] = SongRepository()
        self.songs_model: Final[SongTableModel] = SongTableModel(self.songs_repository)
        self.files_table_view.setModel(self.songs_model)
        self.files_table_view.resizeColumnsToContents()
        self.files_table_view.selectionModel().selectionChanged.connect(
            self.updateStatusbarSelectionMessage
        )
        self.files_table_view.selectionModel().selectionChanged.connect(
            self.setSelectionActionState
        )
        self.songs_repository.songs_updated.connect(
            lambda: updateTableView(self.files_table_view, self.songs_repository)
        )
        self.songs_repository.songs_updated.connect(self.setFileActionState)

        # Drag and Drop
        self.files_table_view.setAcceptDrops(True)
        self.files_table_view.dropEvent = self.processTableDropEvents
        self.files_table_view.dragEnterEvent = self.processTableDragEvent
        self.files_table_view.dragMoveEvent = self.processTableDragEvent

        # Actions
        self.action_add_files.triggered.connect(
            lambda: self.openAddDialog(QFileDialog.FileMode.ExistingFiles)
        )
        self.action_add_folder.triggered.connect(
            lambda: self.openAddDialog(QFileDialog.FileMode.Directory)
        )
        self.action_clear_files.triggered.connect(self.clearFiles)
        self.action_remove_selected.triggered.connect(self.removeSelectedFiles)

        self.setActionState()

    def setActionState(self):
        self.setFileActionState()
        self.setSelectionActionState()

    def setSelectionActionState(self):
        self.action_select_all.setEnabled(len(self.songs_repository) > 0)

        has_selection = self.getSelectionLength() > 0
        self.action_select_none.setEnabled(has_selection)
        self.action_remove_selected.setEnabled(has_selection)

    def setFileActionState(self):
        self.action_clear_files.setEnabled(len(self.songs_repository) > 0)
        self.setSelectionActionState()

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
        # self.action_clear_files.setEnabled(len(self.songs_repository) > 0)
        # # if len(self.songs_repository) > 0:
        # #     self.setFilesState(True)

    def processTableDragEvent(self, event: QDragEnterEvent | QDragMoveEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            print(f"Unsupported mimedata: {event.mimeData()}")

    def processTableDropEvents(self, event: QDropEvent):
        """Processes the mimedata dropped on the tableview.

        Information
        ___________
        If the mimedata is not a list of urls, rejects.
        Determines whether the url is a file or folder,
        and then adds to the table."""
        files: list[str] | list[os.PathLike[str]] = []
        folders: list[str] | list[os.PathLike[str]] = []
        for url in event.mimeData().urls():
            if url.toLocalFile().endswith(".mp3"):
                event.acceptProposedAction()
                files.append(url.toLocalFile())
            elif os.path.isdir(url.toLocalFile()):
                event.acceptProposedAction()
                folders.append(url.toLocalFile())
        if files:
            self.addFiles(files)
        if folders:
            new_files: list[str] | list[os.PathLike[str]] = []
            for folder in folders:
                new_files.extend(self.getFolderFiles(folder))
            self.addFiles(new_files)

    def clearFiles(self):
        self.songs_model.layoutAboutToBeChanged.emit()
        self.songs_repository.clearFiles()
        self.files_table_view.clearSelection()
        self.action_clear_files.setEnabled(False)

    def getSelectionLength(self) -> int:
        return len(self.files_table_view.selectionModel().selectedRows())

    def updateStatusbarSelectionMessage(self):
        selected_length = self.getSelectionLength()
        if selected_length > 0:
            self.statusbar.showMessage(
                f"{selected_length} file{'s' if selected_length > 1 else ''} selected."
            )
        else:
            self.statusbar.showMessage("")

    def removeSelectedFiles(self):
        """Removes the files at the indexes provided by the selectionModel"""
        selectionLength = self.getSelectionLength()
        if selectionLength == 0:
            # NOTE: This should never need to be checked:
            # the button is disabled when there's no selection
            # But keeping the check here in case
            return
        if selectionLength == len(self.songs_repository):
            self.songs_repository.clearFiles()
        selection: list[QModelIndex] = (
            self.files_table_view.selectionModel().selectedRows()
        )

        # NOTE: Map to source model if filtering or sorting using a Proxy model is used
        source_indexes: list[QModelIndex] = [
            cast(QSortFilterProxyModel, self.files_table_view.model()).mapToSource(
                index
            )
            if isinstance(self.files_table_view.model(), QSortFilterProxyModel)
            else index
            for index in selection
        ]

        self.songs_repository.removeSongs([index.row() for index in source_indexes])

        self.files_table_view.clearSelection()


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Kayzels")
    app.setApplicationName("Music Modify")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
