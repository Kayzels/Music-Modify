# pyright: reportImplicitAbstractClass=false
from abc import ABCMeta, abstractmethod
import logging

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QDialogButtonBox, QWidget, QDialog


logger = logging.getLogger(__name__)


# There is a metaclass conflict between ABC and PySide6.
# So we need to create a metaclass that inherits both.
class ABCQMeta(ABCMeta, type(QObject)):
    pass


class PrefsAbstractDialog(QDialog, metaclass=ABCQMeta):
    settings_updated: Signal = Signal()
    button_box: QDialogButtonBox

    def __init__(self, parent: QWidget | None = None):
        QDialog.__init__(self, parent)

    def setButtonBoxConnections(self):
        """Should always be called at the end of initializing a concrete instance.
        Creates the connection between the signals from the buttons in the button box
        and the slot in the class for that button."""
        self.button_box.button(
            QDialogButtonBox.StandardButton.RestoreDefaults
        ).clicked.connect(self.restoreDefaults)

        self.button_box.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(
            self.resetSettings
        )

    @abstractmethod
    def updateSettings(self) -> None:
        """A slot that should be called from the parent widget when the dialog is accepted.
        Changes the values in the settings file to match the ones set in the dialog.
        """
        pass

    @abstractmethod
    def restoreDefaults(self) -> None:
        """Change the settings back to the original default values."""
        logger.debug("Called restore defaults in abstract")
        pass

    @abstractmethod
    def resetSettings(self) -> None:
        """Reset the settings to the values they had when the dialog opened."""
        logger.debug("Called reset settings in abstract")
        pass
