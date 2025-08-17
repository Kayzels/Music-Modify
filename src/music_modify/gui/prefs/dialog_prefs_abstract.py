"""Module that defines a PrefsAbstractDialog.

This is an abstract class for defining the shared functionality
of all preference dialogs.
"""

from abc import ABC, abstractmethod
import logging
from typing import final

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QWidget

from music_modify.gui.meta import ABCQMeta

logger = logging.getLogger(__name__)


class PrefsAbstractDialog(QDialog, ABC, metaclass=ABCQMeta):
    """Defines the required functionality for all child preference dialogs."""

    settings_updated: Signal = Signal()
    "Signal that is emitted whenever any setting is changed."

    @abstractmethod
    def setupUi(self) -> None:
        """Set up the display of the dialog."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Creates a dialog for managing preferences.

        Args:
            parent: The widget that the dialog should be displayed on.
        """
        QDialog.__init__(self, parent)
        self.setupUi()
        self.button_box: QDialogButtonBox = self._createButtonBox()
        self.accepted.connect(self.updateSettings)

    @final
    def _createButtonBox(self) -> QDialogButtonBox:
        layout = self.layout()
        if layout is None:
            raise Exception("Layout not set for dialog in setupUi")
        button_box = QDialogButtonBox(self)
        button_box.setOrientation(Qt.Orientation.Horizontal)
        button_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Reset
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(
            QDialogButtonBox.StandardButton.RestoreDefaults,
        ).clicked.connect(self.restoreDefaults)
        button_box.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(
            self.resetSettings,
        )
        layout.addWidget(button_box)
        return button_box

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
