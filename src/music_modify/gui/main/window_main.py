"""Module that defines the main user interface."""

import datetime
import logging
import os
from os import PathLike
from pathlib import Path
import time
from typing import Final

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMenu,
    QProgressDialog,
)

from music_modify.gui.about import AboutDialog
from music_modify.gui.edit import EditDialogFactory
from music_modify.gui.prefs import PrefsDialog
from music_modify.gui.utils import getSelectedRows, updateTableView
from music_modify.models import SongRepository, SongTableModel
from music_modify.utils import formatTime

from .ui_window_main import Ui_MainWindow

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main interface window for managing song metadata."""

    def __init__(self) -> None:
        """Creates the main user interface."""
        super().__init__()
        self.setupUi(self)

        # Create separate QLabel widgets instead of using the statbusbar default ones,
        # so that they're not overridden when a QStatusTipEvent happens.
        self.versionMessage: QLabel = QLabel(self)
        "Label that contains the text for the current app version"
        self.statusbar.addWidget(self.versionMessage)
        self.statusLabel: QLabel = QLabel(self)
        "Label that contains information about how many songs are present and selected"
        self.statusbar.addWidget(self.statusLabel)

        self.songs_repository: Final[SongRepository] = SongRepository()
        "Repository that stores the songs being managed"
        self.songs_model: Final[SongTableModel] = SongTableModel(self.songs_repository)
        "Model that links between the song repository and the display of the metadata"
        self.files_table_view.setModel(self.songs_model)
        self.files_table_view.setShowGrid(False)
        self.files_table_view.resizeColumnsToContents()
        self.files_table_view.selectionModel().selectionChanged.connect(
            self.updateStatusbarMessage,
        )
        self.files_table_view.selectionModel().selectionChanged.connect(
            self.setSelectionActionState,
        )
        self.songs_repository.songs_updated.connect(
            lambda: updateTableView(self.files_table_view, self.songs_repository),
        )
        self.songs_repository.songs_updated.connect(self.setFileActionState)
        self.songs_repository.songs_updated.connect(self.updateStatusbarMessage)
        self.files_table_view.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu,
        )
        self.files_table_view.customContextMenuRequested.connect(
            self.showCustomContextMenu,
        )

        # Drag and Drop
        self.files_table_view.setAcceptDrops(True)
        self.files_table_view.dropEvent = self.processTableDropEvents
        self.files_table_view.dragEnterEvent = self.processTableDragEvent
        self.files_table_view.dragMoveEvent = self.processTableDragEvent

        # Actions
        self.action_add_files.triggered.connect(
            lambda: self.openAddDialog(QFileDialog.FileMode.ExistingFiles),
        )
        self.action_add_folder.triggered.connect(
            lambda: self.openAddDialog(QFileDialog.FileMode.Directory),
        )
        self.action_clear_files.triggered.connect(self.clearFiles)
        self.action_remove_selected.triggered.connect(self.removeSelectedFiles)
        self.action_select_all.triggered.connect(self.files_table_view.selectAll)
        self.action_select_none.triggered.connect(self.files_table_view.clearSelection)
        self.action_about.triggered.connect(self.showAboutDialog)
        self.action_preferences.triggered.connect(self.showPrefsDialog)

        self.setActionState()
        self.updateStatusbarMessage()

        # Edit Actions
        self.dialog_factory: EditDialogFactory = EditDialogFactory(
            self,
            self.songs_repository,
        )
        "Factory for generating the right type of EditDialog, based on selection"
        self.action_edit_individual.triggered.connect(self.showEditDialog)
        self.action_edit_bulk.triggered.connect(lambda: self.showEditDialog(bulk=True))

        self.addStatusbarAppMessage()

    def setActionState(self) -> None:
        """Toggle the state of possible actions, based on program state."""
        self.setFileActionState()
        self.setSelectionActionState()

    def setSelectionActionState(self) -> None:
        """Toggle selection-related actions, based on whether any files are selected."""
        self.action_select_all.setEnabled(len(self.songs_repository) > 0)

        has_selection = self.getSelectionLength() > 0
        self.action_select_none.setEnabled(has_selection)
        self.action_remove_selected.setEnabled(has_selection)

    def setFileActionState(self) -> None:
        """Toggle actions related to files, based on whether files exist."""
        self.action_clear_files.setEnabled(len(self.songs_repository) > 0)
        self.setSelectionActionState()

    def openAddDialog(self, file_mode: QFileDialog.FileMode) -> None:
        """Display a file picker based on the file mode.

        This allows users to select the files (or folders) to edit.
        """
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
        """Gets all files that are in the folder, or child folders.

        Args:
            folder: Directory to check for files.

        """
        songs: list[str] = []
        progress_dialog = QProgressDialog(
            "Adding Folders...",
            "Cancel",
            0,
            1,
            parent=self,
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

    def addFiles(self, files: list[str] | list[PathLike[str]]) -> None:
        """Adds the specified files to the table.

        Args:
            files: List of files that should be added.

        """
        start_time = time.time()
        progress_dialog = QProgressDialog(
            "Adding Files...",
            "Cancel",
            0,
            len(files),
            parent=self,
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

    @staticmethod
    def processTableDragEvent(event: QDragEnterEvent | QDragMoveEvent) -> None:
        """Processes dragging data from the tableview, needed for dropping to work.

        Args:
            event: The drag event that should be processed.
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            logger.warning(
                f"Unsupported mimedata when drag/dropping: {event.mimeData()}",
            )

    def processTableDropEvents(self, event: QDropEvent) -> None:
        """Processes the mimedata dropped on the tableview.

        Args:
            event: The drop event that should be processed.

        Information
            If the mimedata is not a list of urls, rejects.
            Determines whether the url is a file or folder,
            and then adds to the table.
        """
        files: list[str] | list[os.PathLike[str]] = []
        folders: list[str] | list[os.PathLike[str]] = []
        for url in event.mimeData().urls():
            if url.toLocalFile().endswith(".mp3"):
                event.acceptProposedAction()
                files.append(url.toLocalFile())
            elif Path(url.toLocalFile()).is_dir():
                event.acceptProposedAction()
                folders.append(url.toLocalFile())
        if files:
            self.addFiles(files)
        if folders:
            new_files: list[str] | list[os.PathLike[str]] = []
            for folder in folders:
                new_files.extend(self.getFolderFiles(folder))
            self.addFiles(new_files)

    def clearFiles(self) -> None:
        """Remove all files from the model."""
        self.songs_model.layoutAboutToBeChanged.emit()
        self.songs_repository.clearFiles()
        self.files_table_view.clearSelection()
        self.action_clear_files.setEnabled(False)

    def getSelectionLength(self) -> int:
        """Gets the number of rows selected in the table."""
        return len(self.files_table_view.selectionModel().selectedRows())

    def updateStatusbarMessage(self) -> None:
        """Display the number of songs and selected songs inside the status bar."""
        num_songs = len(self.songs_repository)
        if num_songs == 0:
            self.statusLabel.setText("")
            return
        # Put the message inside [] so that it's distinct from the version name
        message: str = f"[{num_songs} songs"
        selected_length = self.getSelectionLength()
        if selected_length > 0:
            message += f", {selected_length} selected"
        message += "]"
        self.statusLabel.setText(message)

    def removeSelectedFiles(self) -> None:
        """Removes the files at the indexes provided by the selectionModel."""
        selection_length = self.getSelectionLength()
        if selection_length == 0:
            logger.debug("Called clear selection with a length of 0.")
            return
        if selection_length == len(self.songs_repository):
            self.songs_repository.clearFiles()
            return

        rows = getSelectedRows(self.files_table_view)

        self.songs_repository.removeSongs(rows)
        self.files_table_view.clearSelection()

    def addStatusbarAppMessage(self) -> None:
        """Add text for the version of the app to the status bar."""
        app = QApplication.instance()
        if app is None:
            return
        app_name = app.applicationName()
        app_version = app.applicationVersion()
        self.versionMessage.setText(f"{app_name} {app_version}")

    def showAboutDialog(self) -> None:
        """Show an AboutDialog."""
        about_dialog = AboutDialog(self)
        about_dialog.show()

    def showPrefsDialog(self) -> None:
        """Show a PreferencesDialog."""
        prefs_dialog = PrefsDialog(parent=self)
        prefs_dialog.show()
        prefs_dialog.settings_updated.connect(self.refreshTable)

    def refreshTable(self) -> None:
        """Update the display of the table."""
        self.songs_model.layoutAboutToBeChanged.emit()
        self.songs_repository.refreshDisplay()
        self.songs_model.layoutChanged.emit()
        updateTableView(self.files_table_view, self.songs_repository)

    def showEditDialog(self, *, bulk: bool = False) -> None:
        """Create a dialog for editing the metadata in the selected songs.

        Create a dialog that allows editing the information for each song
        in the selection, either individually with transitions between
        Next and Previous songs, or in bulk.

        Args:
            bulk: Whether the information should be edited in bulk. Default False
        """
        # Need to sort the list so that it's not shown in a random order
        rows = sorted(getSelectedRows(self.files_table_view))

        if len(rows) == 0:
            return

        dialog = self.dialog_factory.get(rows, bulk=bulk)

        def processDialogResult(result: QDialog.DialogCode) -> None:
            logger.debug("Called process dialog result for edit dialog")
            if result == QDialog.DialogCode.Accepted:
                dialog.updateSongInfo()

        dialog.info_updated.connect(self.refreshTable)
        dialog.finished.connect(processDialogResult)

        dialog.show()

    def showCustomContextMenu(self, position: QPoint) -> None:
        """Show a context menu for the selected item in the table.

        Args:
            position: The mouse position when the user right clicks.
        """
        index = self.files_table_view.indexAt(position)
        if not index.isValid():
            logger.info(f"Invalid index when calling custom context menu: {index}")
            return

        context_menu = QMenu(self)

        # If only one song selected, can only edit individually,
        # so don't show bulk, or child menu
        if self.getSelectionLength() == 1:
            context_menu.addAction(self.action_edit_individual)
        else:
            song_menu = QMenu("Edit Songs")
            song_menu.addActions(self.menu_edit_songs.actions())
            context_menu.addMenu(song_menu)

        context_menu.addAction(self.action_remove_selected)

        context_menu.popup(self.files_table_view.viewport().mapToGlobal(position))
