"""Signals that are emitted for jobs and actions.
"""
from PyQt5.QtCore import pyqtSignal, QObject


class JobSignals(QObject):
    """The signals emitted for jobs - started, progress, finished.
        """
    job_started = pyqtSignal(int)  # ? int is job_number
    job_progress = pyqtSignal(int, int)  # ? int1 is job_number, int2 progress
    job_finished = pyqtSignal(int)  # ? int is job_number


class ActionSignals(QObject):
    """The signals emitted for actions - started, progress, finished.
        """
    action_started = pyqtSignal(int, int, int)
    # ? job index, action index, length
    action_progress = pyqtSignal(int, int, int)
    # ? job index, action index, progress
    action_finished = pyqtSignal(int, int)
    # ? job index, action index


class SubactionSignals (QObject):
    """The signals emitted for subactions - started, progress, finished.
        """
    subaction_started = pyqtSignal(int, int, int, int)
    # ? job index, action index, subaction index, length
    subaction_progress = pyqtSignal(int, int, int, int)
    # ? job index, action index, subaction index, progress
    subaction_finished = pyqtSignal(int, int, int)
    # ? job index, action index, subaction index
