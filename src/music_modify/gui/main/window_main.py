"""Module that defines the main user interface."""

from collections.abc import Callable
from dataclasses import dataclass
import datetime
import logging
import os
from os import PathLike
from pathlib import Path
import time
from typing import Final, final

from PySide6.QtCore import QPoint, QRect, Qt, Slot
from PySide6.QtGui import QAction, QDragEnterEvent, QDragMoveEvent, QDropEvent, QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDialog,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QProgressDialog,
    QStatusBar,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types.tag_value import AbstractTagValue
from music_modify.gui.about import AboutDialog
from music_modify.gui.completion import EditWithComplete
from music_modify.gui.edit import EditDialogFactory
from music_modify.gui.edit.bulk import EditBulkAbstractWidget
from music_modify.gui.edit.widget_edit_factory import EditWidgetFactory
from music_modify.gui.prefs import PrefsDialog
from music_modify.gui.utils import getSelectedRows, updateTableView
from music_modify.models import SongRepository, SongTableModel
from music_modify.prefs import Settings
from music_modify.utils import formatTime

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main interface window for managing song metadata."""

    def __init__(self, settings: Settings) -> None:
        """Creates the main user interface."""
        super().__init__()
        self._setupUi()

        self._settings = settings

        # Create separate QLabel widgets instead of using the statbusbar default ones,
        # so that they're not overridden when a QStatusTipEvent happens.
        self.versionMessage: QLabel = QLabel(self)
        "Label that contains the text for the current app version"
        self.statusbar.addWidget(self.versionMessage)
        self.statusLabel: QLabel = QLabel(self)
        "Label that contains information about how many songs are present and selected"
        self.statusbar.addWidget(self.statusLabel)

        @Slot(str)
        def updateJoinCharacter(character: str) -> None:
            AbstractTagValue.join_character = character
            self.refreshTableData()

        @Slot(str)
        def updateSplitEnterCharacter(character: str) -> None:
            EditWithComplete.updateJoinCharacter(character)
            EditBulkAbstractWidget.split_text_entered = character

        @Slot()
        def updateWidgetEditorTypes() -> None:
            EditWidgetFactory.editor_types = {
                info.id3_key: info.editor_type for info in self._settings.info_tags
            }

        @Slot()
        def updateFactoryTags() -> None:
            EditDialogFactory.all_tags = self._settings.info_tags

        self.songs_repository: Final[SongRepository] = SongRepository()
        "Repository that stores the songs being managed"
        self.songs_model: Final[SongTableModel] = SongTableModel(
            self.songs_repository, self._settings.table_tags
        )
        "Model that links between the song repository and the display of the metadata"

        self._settings.tags_updated.connect(self.refreshTableLayout)
        self._settings.tags_updated.connect(updateWidgetEditorTypes)
        self._settings.tags_updated.connect(updateFactoryTags)
        self._settings.split_values_display_changed.connect(updateJoinCharacter)
        self._settings.split_text_entered_changed.connect(updateSplitEnterCharacter)

        EditDialogFactory.setDetails(
            parent=self,
            repository=self.songs_repository,
            all_tags=self._settings.info_tags,
        )

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
            lambda: updateTableView(
                self.files_table_view, self.songs_repository, self._settings.table_tags
            ),
        )
        self.files_table_view.customContextMenuRequested.connect(
            self.showCustomContextMenu,
        )

        self._createActions()

        self.songs_repository.songs_updated.connect(self.setFileActionState)
        self.songs_repository.songs_updated.connect(self.updateStatusbarMessage)

        self.setActionState()
        self.updateStatusbarMessage()

        self.addStatusbarAppMessage()

        updateJoinCharacter(self._settings.split_values_display)
        updateSplitEnterCharacter(self._settings.split_text_entered)
        updateWidgetEditorTypes()

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
            # noinspection PyTypeChecker
            self.songs_repository.add(file)
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
            local_url = url.toLocalFile()
            if local_url.endswith(".mp3"):
                event.acceptProposedAction()
                files.append(local_url)
            elif Path(local_url).is_dir():
                event.acceptProposedAction()
                folders.append(local_url)
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
        self.songs_repository.clear()
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
            self.songs_repository.clear()
            return

        rows = getSelectedRows(self.files_table_view)

        self.songs_repository.removeAtIndexes(rows)
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
        prefs_dialog = PrefsDialog(parent=self, settings=self._settings)
        prefs_dialog.show()

    def refreshTableLayout(self) -> None:
        """Update the display of the table."""
        self.songs_model.layoutAboutToBeChanged.emit()
        self.songs_model.updateTableTags(self._settings.table_tags)
        self.songs_repository.refreshDisplay()
        self.songs_model.layoutChanged.emit()
        updateTableView(
            self.files_table_view, self.songs_repository, self._settings.table_tags
        )

    @Slot(list)
    def refreshTableData(self, rows: list[int] | None = None) -> None:
        """Update the data for each item in the table."""
        self.songs_model.refreshData(rows)
        updateTableView(
            self.files_table_view, self.songs_repository, self._settings.table_tags
        )

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

        dialog = EditDialogFactory.get(rows, bulk=bulk)

        @Slot(QDialog.DialogCode)
        def processDialogResult(result: QDialog.DialogCode) -> None:
            logger.debug("Called process dialog result for edit dialog")
            if result == QDialog.DialogCode.Accepted:
                dialog.updateSongInfo()

        dialog.info_updated.connect(self.refreshTableData)
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

    def _createActions(self) -> None:
        """Create the possible actions.

        Should be called after the UI is created, and all widgets and members defined.
        """

        @dataclass
        class _ActionInfo:
            name: str
            icon: QIcon.ThemeIcon | None = None
            func: Callable[..., None] | None = None

        actions: tuple[_ActionInfo, ...] = (
            _ActionInfo(
                "Add Files",
                QIcon.ThemeIcon.DocumentNew,
                lambda: self.openAddDialog(QFileDialog.FileMode.ExistingFiles),
            ),
            _ActionInfo(
                "Add Folder",
                QIcon.ThemeIcon.FolderNew,
                lambda: self.openAddDialog(QFileDialog.FileMode.Directory),
            ),
            _ActionInfo("Clear Files", QIcon.ThemeIcon.ListRemove, self.clearFiles),
            _ActionInfo(
                "Select All",
                QIcon.ThemeIcon.EditSelectAll,
                self.files_table_view.selectAll,
            ),
            _ActionInfo("Preferences...", None, self.showPrefsDialog),
            _ActionInfo("Select None", None, self.files_table_view.clearSelection),
            _ActionInfo(
                "About Music Modify...", QIcon.ThemeIcon.HelpAbout, self.showAboutDialog
            ),
            _ActionInfo(
                "Remove Selected", QIcon.ThemeIcon.EditDelete, self.removeSelectedFiles
            ),
            _ActionInfo("Edit individually", None, self.showEditDialog),
            _ActionInfo("Edit in bulk", None, lambda: self.showEditDialog(bulk=True)),
        )

        def createAction(info: _ActionInfo) -> QAction:
            action = QAction(info.name, self, menuRole=QAction.MenuRole.NoRole)
            if info.icon:
                action.setIcon(QIcon(QIcon.fromTheme(info.icon)))
            if info.func:
                action.triggered.connect(info.func)
            return action

        (
            self.action_add_files,
            self.action_add_folder,
            self.action_clear_files,
            self.action_select_all,
            self.action_preferences,
            self.action_select_none,
            self.action_about,
            self.action_remove_selected,
            self.action_edit_individual,
            self.action_edit_bulk,
        ) = [createAction(info) for info in actions]

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 22))

        self.menu_file, self.menu_view, self.menu_edit, self.menu_help = (
            QMenu(name, self.menubar) for name in ("File", "View", "Edit", "Help")
        )
        self.menu_edit_songs = QMenu("Edit Songs", self.menu_edit)
        self.setMenuBar(self.menubar)

        for menu_action in (
            self.menu_file,
            self.menu_edit,
            self.menu_view,
            self.menu_help,
        ):
            self.menubar.addAction(menu_action.menuAction())

        for file_action in (
            self.action_add_files,
            self.action_add_folder,
            self.action_clear_files,
            self.action_remove_selected,
        ):
            self.menu_file.addAction(file_action)
            self.tool_bar.addAction(file_action)

        for select_action in (self.action_select_all, self.action_select_none):
            self.menu_edit.addAction(select_action)

        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.menu_edit_songs.menuAction())
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.action_preferences)

        for song_action in (self.action_edit_individual, self.action_edit_bulk):
            self.menu_edit_songs.addAction(song_action)

        self.menu_help.addAction(self.action_about)

    @final
    def _setupUi(self) -> None:
        """Create the main interface."""
        self.setWindowTitle("Music Modify")
        self.resize(800, 600)

        central_widget = QWidget(self)
        vertical_layout = QVBoxLayout(central_widget)
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(central_widget)

        self.files_table_view = QTableView(central_widget)
        self.files_table_view.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
        self.files_table_view.setAlternatingRowColors(True)
        self.files_table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.files_table_view.horizontalHeader().setStretchLastSection(True)
        self.files_table_view.setShowGrid(False)
        self.files_table_view.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        # Drag and Drop
        self.files_table_view.setAcceptDrops(True)
        self.files_table_view.dropEvent = self.processTableDropEvents
        self.files_table_view.dragEnterEvent = self.processTableDragEvent
        self.files_table_view.dragMoveEvent = self.processTableDragEvent

        vertical_layout.addWidget(self.files_table_view)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.tool_bar = QToolBar(self)
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tool_bar)
