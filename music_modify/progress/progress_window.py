"""Module for the window that shows the progress of jobs.
    """
from typing import cast, List, Optional, TYPE_CHECKING, Union

from PyQt5.QtCore import QThreadPool, pyqtSlot
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow

from gui.window_progress import Ui_ProgressWindow

from progress.progress_widgets import ActionProgressWidget, JobProgressWidget,\
    SubactionProgressWidget
from jobs import Job
from actions import Action, ActionToCreate

if TYPE_CHECKING:
    from music_modify import MainWindow


class ProgressWindow(QMainWindow, Ui_ProgressWindow):
    """Window that displays a list of jobs that are being performed.
        """

    def __init__(self, main_window: 'MainWindow', *args, **kwargs):
        """Constructor for ProgressWindow.

            Parameter
            ---------
            main_window : MainWindow -
                Send in the main window, so it can be hidden and shown.
            """
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.main_window = main_window
        self.job_index = 0

        self.jobs_threadpool = QThreadPool()

        self.actionShow_Main_Window.toggled.connect(self.toggle_main_window)
        self.original_close_event = self.closeEvent  # type: ignore
        self.closeEvent = self._window_closed  # pylint: disable=invalid-name

    def toggle_main_window(self, toggled: bool):
        """Either hides or shows the main window.

            Parameters
            ----------
            toggled : bool -
                Whether the window should be shown.
            """
        if self.main_window is None:
            return
        self.main_window.setVisible(toggled)

    def _window_closed(self, event: QCloseEvent):
        """Reimplement the closeEvent method of this window.
            Toggle the action linked to this window in the
            main window to off.

            Parameters
            ----------
            event : QCloseEvent -
                The event that is sent when the window is closed.
            """
        self.main_window.actionCurrent_Jobs.setChecked(False)
        self.original_close_event(event)

    def create_new_job(self, created_actions: List[ActionToCreate]):
        """Creates a job that will be performed on the songs
            """
        created_job: List[Action] = []
        for index, created_action in enumerate(created_actions):
            action = Action(created_action, self.job_index, index)
            action.signals.action_started.connect(self.set_action_length)
            action.signals.action_progress\
                .connect(self.update_action_progress)
            action.signals.action_finished\
                .connect(self.update_action_complete)
            if action.subaction_signals is not None:
                action.subaction_signals.subaction_started\
                    .connect(self.set_subaction_length)
                action.subaction_signals.subaction_progress\
                    .connect(self.update_subaction_progress)
                action.subaction_signals.subaction_finished\
                    .connect(self.update_subaction_complete)
            created_job.append(action)

        self.add_to_current_jobs(created_job)

    def add_to_current_jobs(self, created_job: List[Action]):
        """Add the list of actions sent to the jobs window,
            and then perform the actions in the order created.

            Parameters
            ----------
            created_job : List[Action] -
                List of actions that should be performed.
            """
        job = Job(created_job, self.job_index)
        scroll_area_widget = self.jobsScrollAreaWidgetContents
        job_progress_widget = JobProgressWidget(scroll_area_widget,
                                                created_job,
                                                self.job_index,
                                                self)
        scroll_layout = self.jobsScrollAreaWidgetContents.layout()
        index_to_add = scroll_layout.count() - 1
        scroll_layout.insertWidget(index_to_add, job_progress_widget)
        self.jobsShownCount.setText(f"{index_to_add}")

        job.signals.job_progress.connect(self.update_job_progress)
        job.signals.job_finished.connect(self.update_job_complete)

        self.job_index = self.job_index + 1
        self.add_new_job(job)

    def add_new_job(self, job: Job):
        """Add a new job to the jobs being displayed, and perform the job.

            Parameters
            ----------
            job : Job -
                The Job that should be performed and displayed.
        """
        self.jobs_threadpool.start(job)
        thread_count = self.jobs_threadpool.activeThreadCount()
        self.activeJobsCount.setText(f"{thread_count}")

    # region PyQt Slots for action progress
    def _get_progress_widget(self,
                             job_index: int,
                             action_index: Optional[int] = None,
                             subaction_index: Optional[int] = None)\
            -> Union[JobProgressWidget,
                     ActionProgressWidget,
                     SubactionProgressWidget]:
        """Get the widget whose progress should be updated,
            based on the indexes sent.

            If an action index or subaction index is not sent,
            sends the main job progress widget.

            Parameters
            ----------
            job_index : int -
                The index of the job progress widget whose
                progress should be updated.\n
            action_index : Optional[int], optional -
                The index of the action progress widget
                whose progress should be updated.
                By default None.\n
            subaction_index : Optional[int], optional -
                The index of the subaction progress widget
                whose progress should be updated.
                By default None.\n

            Returns
            -------
            Union[JobProgressWidget,
            ActionProgressWidget, SubactionProgressWidget] -
                The Widget whose progress should be updated,
                based on the indexes sent.
            """
        job_widget_name = f"JobProgressWidget_{job_index}"
        job_progress_widget = self\
            .jobsScrollAreaWidgetContents.findChild(JobProgressWidget,
                                                    job_widget_name)
        job_progress_widget = cast(JobProgressWidget, job_progress_widget)
        if action_index is None:
            return job_progress_widget

        action_progress_widget = job_progress_widget\
            .actionsScrollAreaWidgetContents.layout()\
            .itemAt(action_index).widget()
        action_progress_widget = cast(ActionProgressWidget,
                                      action_progress_widget)
        if subaction_index is None:
            return action_progress_widget

        subaction_progress_widget = action_progress_widget\
            .subactionsScrollAreaWidgetContents.layout()\
            .itemAt(subaction_index).widget()
        subaction_progress_widget = cast(SubactionProgressWidget,
                                         subaction_progress_widget)
        return subaction_progress_widget

    @pyqtSlot(int, int)
    def update_job_progress(self, job_index: int, progress: int):
        """Update the progress bar of the job that is
            associated with this job index.

            Parameters
            ----------
            job_index : int -
                The index of the job that should be updated.\n
            progress : int -
                The value the progress bar should be updated to.
            """
        job_progress_widget = self._get_progress_widget(job_index)
        job_progress_widget = cast(JobProgressWidget, job_progress_widget)
        job_progress_widget.jobProgressBar.setValue(progress)

    @pyqtSlot(int)
    def update_job_complete(self, job_index: int):
        """Update the progress bar of the job progress widget to be complete,
            and allow a user to remove this job from the list.

            Parameters
            ----------
            job_index : int -
                The index of the job that should be updated.
            """
        job_progress_widget = self._get_progress_widget(job_index)
        job_progress_widget.jobProgressBar\
            .setValue(job_progress_widget.jobProgressBar.maximum())
        job_progress_widget.removeJobButton.setEnabled(True)
        job_progress_widget.removeJobButton.show()
        job_count = self.jobs_threadpool.activeThreadCount()
        self.activeJobsCount.setText(f"{job_count}")

    @pyqtSlot(int, int, int)
    def set_action_length(self,
                          job_index: int,
                          action_index: int,
                          length: int):
        """Set the maximum of the progress bar associated
            with this action to length.

            Parameters
            ----------
            job_index : int -
                The index of the job the action is associated with.\n
            action_index : int -
                The index of this action in the job list.\n
            length : int -
                The value the progress bar should set as the maximum.\n
            """
        action_progress_widget = self._get_progress_widget(job_index,
                                                           action_index)
        action_progress_widget = cast(ActionProgressWidget,
                                      action_progress_widget)
        action_progress_widget.actionProgressBar.setMaximum(length)

    @pyqtSlot(int, int, int)
    def update_action_progress(self,
                               job_index: int,
                               action_index: int,
                               progress: int):
        """Update the progress bar associated with this action
            with the progress sent.

            Parameters
            ----------
            job_index : int -
                The index of the job the action is associated with.\n
            action_index : int -
                The index of the action whose progress bar
                should be updated.\n
            progress : int -
                The value that the progress bar should be set to.
            """
        action_progress_widget = self._get_progress_widget(job_index,
                                                           action_index)
        action_progress_widget = cast(ActionProgressWidget,
                                      action_progress_widget)
        action_progress_widget.actionProgressBar.setValue(progress)

    @pyqtSlot(int, int)
    def update_action_complete(self,
                               job_index: int,
                               action_index: int):
        """Update the progress bar of the action widget to be complete.

            Parameters
            ----------
            job_index : int -
                The index of the job the action is associated with.\n
            action_index : int -
                The index of the action that should be updated.
            """
        action_progress_widget = self._get_progress_widget(job_index,
                                                           action_index)
        action_progress_widget.actionProgressBar\
            .setValue(action_progress_widget.actionProgressBar.maximum())

    @pyqtSlot(int, int, int, int)
    def set_subaction_length(self,
                             job_index: int,
                             action_index: int,
                             subaction_index: int,
                             length: int):
        """Set the max value of the progress bar linked to this subaction.

            Parameters
            ----------
            job_index : int -
                The index of the job linked to this subaction.\n
            action_index : int -
                The index of the action linked to this subaction.\n
            subaction_index : int -
                The index of this subaction in the subactions list.\n
            length : int -
                The value that should be set as the max value.\n
            """
        subaction_progress_widget = self._get_progress_widget(job_index,
                                                              action_index,
                                                              subaction_index)
        subaction_progress_widget = cast(SubactionProgressWidget,
                                         subaction_progress_widget)
        subaction_progress_widget.subactionProgressBar.setMaximum(length)

    @pyqtSlot(int, int, int, int)
    def update_subaction_progress(self,
                                  job_index: int,
                                  action_index: int,
                                  subaction_index: int,
                                  progress: int):
        """Update the progress bar linked to this subaction
            with the progress value sent.

            Parameters
            ----------
            job_index : int -
                The index of the job linked to this subaction.\n
            action_index : int -
                The index of the action linked to this subaction.\n
            subaction_index : int -
                The index of this subaction in the subactions list.\n
            progress : int -
                The value that the progress bar should be upated to.
            """
        subaction_progress_widget = self._get_progress_widget(job_index,
                                                              action_index,
                                                              subaction_index)
        subaction_progress_widget = cast(SubactionProgressWidget,
                                         subaction_progress_widget)
        subaction_progress_widget.subactionProgressBar.setValue(progress)

    @pyqtSlot(int, int, int)
    def update_subaction_complete(self,
                                  job_index: int,
                                  action_index: int,
                                  subaction_index: int):
        """Update the progress bar of this subaction to the max value.

            Parameters
            ----------
            job_index : int -
                The index of the job linked to this subaction.\n
            action_index : int -
                The index of the action linked to this subaction.\n
            subaction_index : int -
                The index of this subaction in the subactions list.
            """
        subaction_progress_widget = self._get_progress_widget(job_index,
                                                              action_index,
                                                              subaction_index)
        subaction_progress_widget = cast(SubactionProgressWidget,
                                         subaction_progress_widget)
        subaction_progress_widget.subactionProgressBar.setValue(
            subaction_progress_widget.subactionProgressBar.maximum())
    # endregion
