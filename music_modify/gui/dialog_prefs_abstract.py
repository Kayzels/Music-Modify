# pyright: reportImplicitAbstractClass=false
from abc import abstractmethod
import logging
from typing import Callable, Self

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialogButtonBox, QMessageBox, QWidget, QDialog

from .meta import ABCQMeta

logger = logging.getLogger(__name__)


# There is a metaclass conflict between ABC and PySide6.
# So we need to create a metaclass that inherits both.
# class ABCQMeta(ABCMeta, type(QObject)):
#     pass


class PrefsAbstractDialog(QDialog, metaclass=ABCQMeta):
    settings_updated: Signal = Signal()

    def __init__(self, parent: QWidget | None = None):
        QDialog.__init__(self, parent)
        if hasattr(self, "setupUi"):
            self.setupUi: Callable[[Self], None]
            self.setupUi(self)
            self._setButtonBoxConnections()
        else:
            show_on = self if parent is None else parent
            message = "Setup Ui function not found when calling abstract init"
            logger.warning(message)
            QMessageBox.warning(show_on, "Missing setupUi", message)

    def _setButtonBoxConnections(self):
        """Creates the connection between the signals from the buttons in the button box
        and the slot in the class for that button."""
        if not hasattr(self, "button_box"):
            warning = "Button Box not found or invalid after calling _setupUiCore()"
            logger.warning(warning)
            QMessageBox.warning(self, "Missing attributes", warning)
            return
        self.button_box: QDialogButtonBox
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
