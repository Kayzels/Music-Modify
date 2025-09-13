"""Module that defines the main dialog that is used to change the program settings."""

import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from music_modify.prefs import Settings

from .dialog_prefs_abstract import PrefsAbstractDialog
from .dialog_prefs_split import PrefsSplitDialog
from .dialog_prefs_tag import PrefsTagDialog

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PrefsDialog(QDialog):
    """A dialog that allows the user to change the settings the program uses."""

    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        """Create a PrefsDialog.

        Args:
            settings: Settings object to read from and update.
            parent: The widget that the dialog should be displayed on.
        """
        super().__init__(parent)
        self.setupUi()

        self._settings: Settings = settings

        self.button_edit_tags.clicked.connect(
            lambda: self.openChildDialog(PrefsTagDialog),
        )
        self.button_edit_split.clicked.connect(
            lambda: self.openChildDialog(PrefsSplitDialog),
        )

    def openChildDialog(self, dialog_type: type[PrefsAbstractDialog]) -> None:
        """Opens a dialog of the specified type to edit those specific setting groups.

        Args:
            dialog_type: The specific type of child dialog that should be opened.
        """
        dialog = dialog_type(self._settings, self)
        dialog.setModal(True)

        dialog.show()

    def setupUi(self) -> None:
        """Set up the interface for the dialog."""
        self.resize(360, 140)

        vertical_layout = QVBoxLayout(self)
        vertical_layout.setContentsMargins(10, 0, 10, 0)
        horizontal_layout = QHBoxLayout()

        self.button_edit_tags = QPushButton("Edit Tags...", parent=self)
        self.button_edit_tags.setToolTip("The tags shown in the main table.")
        horizontal_layout.addWidget(self.button_edit_tags)

        self.button_edit_split = QPushButton("Edit Split Characters...", parent=self)
        self.button_edit_split.setToolTip(
            "The characters used to display and enter items with multiple values."
        )
        horizontal_layout.addWidget(self.button_edit_split)

        vertical_layout.addLayout(horizontal_layout)

        button_box = QDialogButtonBox(
            self,
            orientation=Qt.Orientation.Horizontal,
            standardButtons=QDialogButtonBox.StandardButton.Close,
        )

        vertical_layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.setWindowTitle("Preferences")
