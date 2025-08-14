"""Module that defines a PrefsAbstractDialog.

This is an abstract class for defining the shared functionality
of all preference dialogs.
"""

from abc import ABC, abstractmethod
import logging
from typing import Self

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QWidget

from music_modify.gui.meta import ABCQMeta

logger = logging.getLogger(__name__)


class PrefsAbstractDialog(QDialog, ABC, metaclass=ABCQMeta):
    """Defines the required functionality for all child preference dialogs."""

    settings_updated: Signal = Signal()
    "Signal that is emitted whenever any setting is changed."

    @abstractmethod
    def setupUi(self, dialog: Self, /) -> None:
        """Set up the display of the dialog."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Creates a dialog for managing preferences.

        Args:
            parent: The widget that the dialog should be displayed on.
        """
        self.button_box: QDialogButtonBox | None = None
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._setButtonBoxConnections()
        self.accepted.connect(self.updateSettings)

    def _setButtonBoxConnections(self) -> None:
        """Creates connections between button box signals and slots."""
        if not self.button_box:
            warning = "Button Box not found or invalid after calling setupUi()."
            logger.warning(warning)
            QMessageBox.warning(self, "Missing attributes", warning)
            return
        self.button_box.button(
            QDialogButtonBox.StandardButton.RestoreDefaults,
        ).clicked.connect(self.restoreDefaults)

        self.button_box.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(
            self.resetSettings,
        )

    @abstractmethod
    def updateSettings(self) -> None:
        """Changes the values in the settings file to match the ones set in the dialog.

        A slot that should be called from the parent widget when the dialog is accepted.
        """

    @abstractmethod
    def restoreDefaults(self) -> None:
        """Change the settings back to the original default values."""

    @abstractmethod
    def resetSettings(self) -> None:
        """Reset the settings to the values they had when the dialog opened."""
