"""Module for a group of tasks (a job) that should be performed on a song.
    """
from typing import List

from PyQt5.QtCore import QRunnable

from actions import Action
from signals import JobSignals


class Job (QRunnable):
    """Worker Thread to run multiple jobs working on songs at the same time.
        """
    def __init__(self, job: List[Action], job_index: int):
        """Constructor for job. Saves arguments in order for the runner to
            know what needs to be run.

            Parameters
            ----------
            job : List[Action] -
                List of the actions to be performed.\n
            job_index : int -
                The current job number
            """
        super().__init__()
        self.job = job
        self.action_count = len(self.job)
        self.signals = JobSignals()
        self.job_index = job_index

    def run(self):
        """Runs the job that has been sent in the init.
            """
        for index, action in enumerate(self.job):
            action.perform_action()
            self.signals.job_progress.emit(self.job_index, index+1)
        self.signals.job_finished.emit(self.job_index)
