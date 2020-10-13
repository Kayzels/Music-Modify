"""Module for widgets used to indicate the progress of an action or job.
    """

from typing import List, Optional, TYPE_CHECKING

from PyQt5.QtWidgets import QWidget

from gui.widget_progress_action import Ui_actionProgressWidget
from gui.widget_progress_job import Ui_jobProgressWidget
from gui.widget_progress_subaction import Ui_subactionProgressWidget

from actions import Action
from utils import util_functions as util_f

if TYPE_CHECKING:
    from progress.progress_window import ProgressWindow


class SubactionProgressWidget(QWidget, Ui_subactionProgressWidget):
    """Widget that shows the progress of the subactions related to an action.
        """
    def __init__(self,
                 parent: QWidget,
                 job_index: int,
                 action_index: int,
                 subaction_index: int,
                 subaction_name: str):
        """Constructor for Subaction Progress Widget.

            Parameters
            ----------
            parent : QWidget -
                The Widget the progress widget should show in.\n
            job_index : int
                The number of the job this subaction is associated with.\n
            action_index : int -
                The index of the action this subaction is associated with.\n
            subaction_index : int -
                The location of this subaction in the current action.\n
            subaction_name : str -
                The name of this subaction.
            """
        QWidget.__init__(self, parent)
        self.setupUi(self)

        util_f.refresh_widget(self)

        self.subactionName.setText(subaction_name)
        self.job_index = job_index
        self.action_index = action_index
        self.subaction_index = subaction_index


class ActionProgressWidget(QWidget, Ui_actionProgressWidget):
    """Widget used to indicate the progress of a specific action.
        """
    def __init__(self,
                 parent: QWidget,
                 action: Action,
                 job_index: int,
                 action_index: int):
        """Constructor for Action Progress Widget.

            Parameters
            ----------
            parent : QWidget -
                Widget that should contain the ActionProgressWidget.\n
            action : Action -
                The action that is represented here.\n
            job_index : int -
                The number of the job which the action is associated with.\n
            action_index : int -
                The index of this particular action in the list
                associated with the job.
            """
        QWidget.__init__(self, parent)
        self.setupUi(self)

        util_f.refresh_widget(self)

        self.action_index = action_index
        self.job_index = job_index
        self.songCount_Main.setText(f"{len(action.songs)}")
        self.actionInfo_Main.setText(f"{action.action}")

        self.set_start_state()

        if action.tags:
            self.tagsSummary.show()
            self.tagInfo_Main.setText(f"{action.tags_display}")

        if action.new_values:
            self.valuesSummary.show()
            self.valueCount_Main.setText(f"{len(action.new_values)}")
            if action.custom_values_name:
                self.valuesCustomName_Main.show()
                self.valuesCustomName_Main\
                    .setText(f"{action.custom_values_name}")

        if action.custom_songs_name:
            self.songsCustomName_Main\
                .setText(f"{action.custom_songs_name}")

        if action.response:
            self.discogsSummary.show()
            self.discogsReleaseID_Main.setText(f"{action.discogs_release_id}")
        else:
            self.actionProgressBar.setMaximum(len(action.songs))

        if action.subaction_signals is not None:
            subaction_names = ["Track Extra Artists",
                               "Global Extra Artists",
                               "Label Download",
                               "Genre Download"]
            for index, name in enumerate(subaction_names):
                self.create_subaction_widget(index, name)
            self.displayActionPushButton.toggled\
                .connect(self.subactionsHeadingWidget.setVisible)
            self.displayActionPushButton.toggled\
                .connect(self.display_subactions)
            self.subactionsHeadingWidget.show()
        else:
            self.subactionsHeadingWidget.hide()
            self.subactionsScrollArea.hide()

    def set_start_state(self):
        """Set what the action widget looks like before any data is set.
            """
        self.tagsSummary.hide()
        self.valuesSummary.hide()
        self.discogsSummary.hide()

        self.songsCustomName_Main.hide()
        self.valuesCustomName_Main.hide()

        self.subactionsScrollArea.hide()
        self.subactionsHeadingWidget.hide()

    def create_subaction_widget(self,
                                subaction_index: int,
                                subaction_name: str):
        """Add a subaction widget to the action being shown.

            Parameters
            ----------
            subaction_index : int -
                The location of the subaction in the subactions list.\n
            subaction_name : str -
                The name of the subaction.
            """
        scroll_widget = self.subactionsScrollAreaWidgetContents
        subaction_progress_widget = SubactionProgressWidget(scroll_widget,
                                                            self.job_index,
                                                            self.action_index,
                                                            subaction_index,
                                                            subaction_name)
        scroll_widget.layout().insertWidget(subaction_index,
                                            subaction_progress_widget)

    def display_subactions(self, toggled: bool):
        """Toggle whether the list of subactions should be shown.

            Parameters
            ----------
            toggled : bool
                Whether the list should be shown or not.
            """
        if not toggled:
            self.displaySubactionsPushButton.setChecked(False)
        self.subactionsHeadingWidget.setVisible(toggled)


class JobProgressWidget(QWidget, Ui_jobProgressWidget):
    """Widget that shows a list of actions associated with a certain job.
        """
    def __init__(self,
                 parent: QWidget,
                 job: List[Action],
                 job_index: int,
                 parent_window: Optional['ProgressWindow'] = None
                 ):
        """Constructor for the JobProgressWidget

            Parameters
            ----------
            parent : QWidget -
                The widget that should contain this widget.\n
            job : List[Action] -
                List of actions that should be performed.\n
            job_index : int -
                Where this widget should be located in the list.
            """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setObjectName(f"JobProgressWidget_{job_index}")

        self.parent_window = parent_window

        self.job_index = job_index
        self.job_count = len(job)
        self.jobCount.setText(f"{self.job_count}")
        self.jobProgressBar.setMaximum(self.job_count)

        self.removeJobButton.clicked.connect(self.remove_this_job)
        self.removeJobButton.setEnabled(False)
        self.removeJobButton.hide()

        for action_index, action in enumerate(job):
            self.create_action_progress_widget(action, action_index)

    def create_action_progress_widget(self, action: Action,
                                      action_index: int):
        """Add an action widget to this widget's scroll area

            Parameters
            ----------
            action : Action -
                The action that should be performed.\n
            action_index : int -
                Where this action should be located in the scroll area.
            """
        scroll_widget = self.actionsScrollAreaWidgetContents
        action_progress_widget = ActionProgressWidget(scroll_widget,
                                                      action,
                                                      self.job_index,
                                                      action_index)
        scroll_widget.layout().insertWidget(action_index,
                                            action_progress_widget)

    def remove_this_job(self):
        """Remove the job being displayed from the progress widget.
            """
        print("Remove This Job clicked.")
        if self.parent_window is None:
            return
        util_f.remove_all_widgets(self.layout())
        self.parentWidget().layout().removeWidget(self)
        self.parent_window.jobsShownCount\
            .setText(f"{self.parentWidget().layout().count() - 1}")
        active_jobs = self.parent_window.jobs_threadpool.activeThreadCount()
        self.parent_window.activeJobsCount.setText(f"{active_jobs}")
        self.deleteLater()
