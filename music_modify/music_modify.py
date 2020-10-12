"""Main part of the app. This creates a main window that allows users to
    add and drag files into the program, and then choose to create a job
    with these music files.
"""
# region Python Core Module Imports
import datetime
import os
from pathlib import Path
import sys
import time
from typing import Optional, List, Union
# endregion
# region PyQt5 Imports
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QCloseEvent, QDragEnterEvent, QDragMoveEvent,\
    QDropEvent
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow,\
    QProgressDialog, QWidget
# endregion
# region Ui Imports
from gui.dialog_about import Ui_Dialog
from gui.window_main import Ui_MainWindow
# endregion
# region Project Imports
from jobs import JobDialog
from models import SongTableModel
from progress import ProgressWindow
from songs import Song
from utils import util_functions as util_f
# endregion


class AboutDialog(QDialog, Ui_Dialog):
    """Dialog that shows the information about the app.
        """
    def __init__(self, parent: Optional[QWidget] = None):
        """Constructor for the about dialog.

            Parameters
            ----------
            parent : QWidget, optional -
                The widget which the dialog should be shown above.
                By default None.
            """
        QDialog.__init__(self, parent)
        self.setupUi(self)


class MainWindow (QMainWindow, Ui_MainWindow):
    """Main Window for the Music Modify App
        """

    def __init__(self, *args, **kwargs):
        """Constructor for Main Window
            """
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.selection: List[QModelIndex] = []
        self.progress_window = ProgressWindow(self)
        # self.job_index: int = 0

        self.original_close_event = self.closeEvent  # type: ignore
        self.closeEvent = self._window_closed  # pylint: disable=invalid-name

        # region Drag Drop
        self.filesTableView.setAcceptDrops(True)
        self.filesTableView.dragEnterEvent = self.table_drag_events
        self.filesTableView.dragMoveEvent = self.table_drag_events
        self.filesTableView.dropEvent = self.table_drop_event
        # endregion

        # region Model
        self.songs_model = SongTableModel([])
        self.filesTableView.setModel(self.songs_model)
        # endregion

        # region Add Files Signals
        self.addFilesButton.clicked.connect(self.actionAdd_Files.trigger)
        self.actionAdd_Files.triggered.connect(lambda: self.open_add_dialog
                                               (QFileDialog.ExistingFiles))

        self.addFolderButton.clicked.connect(self.actionAdd_Folder.trigger)
        self.actionAdd_Folder.triggered.connect(lambda: self.open_add_dialog
                                                (QFileDialog.Directory))
        # endregion

        # region Clear Files Signals
        self.clearFilesButton.clicked.connect(self.actionClear_Files.trigger)
        self.actionClear_Files.triggered.connect(self.clear_files)
        # endregion

        # region Selection Signals
        self.selectAllFilesButton.clicked.connect(self.filesTableView
                                                  .selectAll)
        self.selectNoFilesButton.clicked.connect(self.filesTableView
                                                 .clearSelection)

        self.removeSelectedButton.clicked.connect(self.remove_selected_files)
        self.filesTableView.selectionModel().selectionChanged\
            .connect(self.get_selection)
        # endregion

        # region Jobs Signals
        self.actionCurrent_Jobs.toggled.connect(self.toggle_job_window)
        self.actionCurrent_Jobs.setChecked(True)
        self.actionCurrent_Jobs.setChecked(False)

        self.jobPushButton.clicked.connect(self.actionCreate_New_Job.trigger)
        self.actionCreate_New_Job.triggered.connect(self.create_new_job)
        # endregion

        self.actionAbout.triggered.connect(self.show_about_dialog)

        self.set_default_state()

    # region Set States
    def set_default_state(self):
        """Sets the state for the app when there are no files present.
            """
        self.actionCurrent_Jobs.setChecked(False)
        self.set_selection_state(False)
        self.set_files_state(False)
        self.set_create_jobs_state(False)

    def set_selection_state(self, enabled: bool):
        """Sets whether files can be selected or not.
            Affects the buttons related to selection.

            Parameters
            ----------
            enabled : bool -
                Whether selection is enabled or not.
            """
        self.actionSelect_All.setEnabled(enabled)
        self.selectAllFilesButton.setEnabled(enabled)

        self.actionSelect_None.setEnabled(enabled)
        self.selectNoFilesButton.setEnabled(enabled)

        self.actionRemove_Selected_Files.setEnabled(enabled)
        self.removeSelectedButton.setEnabled(enabled)

    def set_files_state(self, enabled: bool):
        """Sets whether actions related to files are enabled.

            Parameters
            ----------
            enabled : bool -
                Whether file actions are possible or not.
            """
        self.clearFilesButton.setEnabled(enabled)
        self.actionClear_Files.setEnabled(enabled)

        self.refreshButton.setEnabled(enabled)
        self.actionRefresh_Files.setEnabled(enabled)

        self.set_selection_state(enabled)

        self.filesTableView.horizontalHeader().\
            setStretchLastSection(not enabled)

    def set_create_jobs_state(self, enabled: bool):
        """Sets whether a new job can be created or not.

            Parameters
            ----------
            enabled : bool -
                Whether job creation is enabled.
            """
        self.jobPushButton.setEnabled(enabled)
        self.actionCreate_New_Job.setEnabled(enabled)
    # endregion

    # region Add Files
    def open_add_dialog(self, file_mode: QFileDialog.FileMode):
        """Opens a File Dialog that allows a user to add files.

            Parameters
            ----------
            file_mode : QFileDialog.FileMode -
                Whether files or folders are shown in the dialog
            """
        files_dialog = QFileDialog(self)
        files_dialog.setFileMode(file_mode)
        if file_mode == QFileDialog.ExistingFiles:
            files_dialog.setNameFilter("MP3 Files (*.mp3)")
        if files_dialog.exec_():
            if file_mode == QFileDialog.ExistingFiles:
                file_names = files_dialog.selectedFiles()
                self.add_files(file_names)
            elif file_mode == QFileDialog.Directory:
                folder = files_dialog.selectedFiles()[0]
                files_in_folder = self.get_folder_files(folder)
                self.add_files(files_in_folder)

    @util_f.timing
    def add_files(self, files: List[str]):
        """Add files to the song model.

            Parameters
            ----------
            files : List[str] -
                List of mp3 file locations to be added.
            """
        if files:
            self.set_files_state(True)
        util_f.refresh_widget(self.filesTableView)
        start_time = time.time()
        progress_dialog = QProgressDialog("Adding Files...",
                                          "Cancel",
                                          0,
                                          len(files),
                                          parent=self,
                                          flags=Qt.WindowFlags())
        progress_dialog.setModal(True)
        progress_dialog.setMinimumDuration(2)
        progress_dialog.setWindowTitle("Add Files")
        for index, file in enumerate(files):
            progress_dialog.setValue(index)
            self.songs_model.songs.append(Song(file))
            self.songs_model.layoutChanged.emit()
            time_taken_seconds = time.time() - start_time
            time_taken = util_f.format_time(
                datetime.timedelta(seconds=time_taken_seconds))
            estimated_time = (time_taken_seconds/(index + 1)) * len(files)
            eta_delta = util_f.format_time(
                datetime.timedelta(seconds=estimated_time))
            label_text = (f"{index}/{len(files)}\n"
                          f"Time Taken: {time_taken}\n"
                          f"ETA: {eta_delta}")
            progress_dialog.setLabelText(label_text)
            if progress_dialog.wasCanceled():
                break
        progress_dialog.setValue(len(files))
        util_f.update_table_view(self.filesTableView)

    def get_folder_files(self, folder: str) -> List[str]:
        """Gets the mp3 files within the given folder.

            Parameters
            ----------
            folder : str -
                Folder that is selected.

            Returns
            -------
            List[str] -
                List of mp3 files in this folder
            """
        songs = []
        progress_dialog = QProgressDialog("Adding Folders...",
                                          "Cancel",
                                          0,
                                          1,
                                          parent=self,
                                          flags=Qt.WindowFlags())
        for folder_name, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".mp3"):
                    songs.append(str(Path(folder_name, file)))
                    progress_dialog.setLabelText(f"{len(songs)} found.")
            if progress_dialog.wasCanceled():
                break
        progress_dialog.setValue(1)
        # ? unknown length of files that will be added.
        # ? set progress_dialog to be done.
        return songs

    def add_folders(self, folders: List[str]):
        """Add many folders to the song model.

            Parameters
            ----------
            folders : List[str] -
                List of folders to add.
            """
        files: List[str] = []
        for folder in folders:
            files.extend(self.get_folder_files(folder))
        self.add_files(files)
    # endregion

    # region Drag Drop
    def table_drag_events(self,
                          event: Union[QDragEnterEvent, QDragMoveEvent]):
        """Determines which drag events the table view accepts.

            Parameters
            ----------
            event : Union[QDragEnterEvent, QDragMoveEvent]) -
                Type of drag events
            """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            print("Unsupported Mimedata: " + str(event.mimeData()))

    @util_f.timing
    def table_drop_event(self, event: QDropEvent):
        """Processes the mimedata dropped on the tableview.

            Information
            -----------
            If the mimedata is not a list of urls, rejects.\n
            Determines whether the url is a file or folder,
                and then adds to the table.

            Parameters
            ----------
            event : QDropEvent -
                event called when data is dropped.
            """
        files = []
        folders = []
        for url in event.mimeData().urls():
            if url.toLocalFile().endswith(".mp3"):
                event.acceptProposedAction()
                files.append(url.toLocalFile())
            elif os.path.isdir(url.toLocalFile()):
                event.acceptProposedAction()
                folders.append(url.toLocalFile())
        if files:
            self.add_files(files)
        if folders:
            self.add_folders(folders)
    # endregion

    # region Clear Files
    def clear_files(self):
        """Removes all songs from the song model.
            """
        self.songs_model.layoutAboutToBeChanged.emit()
        self.songs_model.songs.clear()
        self.songs_model.layoutChanged.emit()
        self.filesTableView.clearSelection()
        self.set_files_state(False)

    # endregion

    # region Selection
    def get_selection(self, *_):
        """Saves the indexes of the selected rows to an attribute.
            """
        self.selection = self.filesTableView.selectionModel().selectedRows()
        selected_length = len(self.selection)
        self.mainStatusBar.showMessage(f"{selected_length} files selected.")
        if selected_length > 0:
            self.set_create_jobs_state(True)

    def remove_selected_files(self):
        """Removes the files at the indexes in the selection attribute.
            """
        if len(self.selection) == len(self.songs_model.songs):
            self.clear_files()
            return
        for index in self.selection:
            row = index.row()
            self.songs_model.layoutAboutToBeChanged.emit()
            del self.songs_model.songs[row]
            self.songs_model.layoutChanged.emit()
        self.filesTableView.clearSelection()
    # endregion Selection

    # region Jobs
    def toggle_job_window(self, toggled: bool):
        """Toggle the associated JobWindow

            Parameters
            ----------
            toggled : bool -
                Whether the window should be displayed.
            """
        self.progress_window.setVisible(toggled)

    def create_new_job(self):
        """Creates a job that will be performed on the songs
            """
        job_dialog = JobDialog(self, self.songs_model, self.selection)
        if job_dialog.exec_():
            created_actions = job_dialog.created_actions
            self.progress_window.create_new_job(created_actions)
            # created_job: List[Action] = []
            # for index, created_action in enumerate(created_actions):
            #     action = Action(created_action, self.job_index, index)
            #     action.signals.action_started\
            #         .connect(self.progress_window.set_action_length)
            #     action.signals.action_progress\
            #         .connect(self.progress_window.update_action_progress)
            #     action.signals.action_finished\
            #         .connect(self.progress_window.update_action_complete)
            #     if action.subaction_signals is not None:
            #         action.subaction_signals.subaction_started\
            #             .connect(self.progress_window.set_subaction_length)
            #         action.subaction_signals.subaction_progress\
            #             .connect(self.progress_window
            #                      .update_subaction_progress)
            #         action.subaction_signals.subaction_finished\
            #             .connect(self.progress_window
            #                      .update_subaction_complete)
            #     created_job.append(action)

            # self.add_to_current_jobs(created_job)

    # def add_to_current_jobs(self, created_job: List[Action]):
    #     """Add the list of actions sent to the jobs window,
    #         and then perform the actions in the order created.

    #         Parameters
    #         ----------
    #         created_job : List[Action] -
    #             List of actions that should be performed.
    #         """
    #     job = Job(created_job, self.job_index)
    #     job_progress_widget = JobProgressWidget(self.progress_window
    #                                             .jobsScrollAreaWidgetContents,
    #                                             created_job,
    #                                             self.job_index,
    #                                             self.progress_window)
    #     scroll_layout = self.progress_window\
    #         .jobsScrollAreaWidgetContents.layout()
    #     index_to_add = scroll_layout.count() - 1
    #     scroll_layout.insertWidget(index_to_add, job_progress_widget)
    #     self.progress_window.jobsShownCount\
    #         .setText(f"{scroll_layout.count() - 1}")

    #     job.signals.job_progress.connect(self.progress_window
    #                                      .update_job_progress)
    #     job.signals.job_finished.connect(self.progress_window
    #                                      .update_job_complete)

    #     self.job_index = self.job_index + 1
    #     self.progress_window.add_new_job(job)

    # endregion

    def _window_closed(self, event: QCloseEvent):
        """Reimplements the close Event of thie window,
            to alert the progress window this window has been closed.
            Sets the action related to showing this window to unset.

            Parameters
            ----------
            event : QCloseEvent -
                Event sent when this window is closed.
            """
        self.progress_window.actionShow_Main_Window.setChecked(False)
        self.original_close_event(event)

    def show_about_dialog(self):
        """Show a summary of the info about the app.
            """
        about_dialog = AboutDialog(self)
        about_dialog.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
