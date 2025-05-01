# pyright: reportImplicitAbstractClass=false
from abc import ABCMeta, abstractmethod
import logging

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QWidget, QDialog


logger = logging.getLogger(__name__)


# There is a metaclass conflict between ABC and PySide6.
# So we need to create a metaclass that inherits both.
class ABCQMeta(ABCMeta, type(QObject)):
    pass


class PrefsAbstractDialog(QDialog, metaclass=ABCQMeta):
    settings_updated: Signal = Signal()

    def __init__(self, parent: QWidget | None = None):
        QDialog.__init__(self, parent)

    @abstractmethod
    def updateSettings(self) -> None:
        """A slot that should be called from the parent widget when the dialog is accepted.
        Changes the values in the settings file to match the ones set in the dialog.
        """
        pass

    @abstractmethod
    def restoreDefaults(self) -> None:
        """Change the settings back to the original default values."""
        pass

    @abstractmethod
    def resetSettings(self) -> None:
        """Reset the settings to the values they had when the dialog opened."""
        pass
