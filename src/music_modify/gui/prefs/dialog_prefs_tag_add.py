"""Module that defines the dialog that allows a user to add a new tag."""

import logging
from typing import TypedDict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from music_modify.models.tag_model import TagModel

logger = logging.getLogger(__name__)


class _TagDict(TypedDict):
    id3_key: str
    display_name: str
    show_in_table: bool


class PrefsTagAddDialog(QDialog):
    """Dialog that allows a user to add a new tag to the list of tags."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Creates a PrefsTagAddDialog.

        Args:
            parent: The widget that this dialog should be displayed on.
        """
        super().__init__(parent)
        self.setupUi()

    def _getValidTag(self, model: TagModel) -> _TagDict | None:
        """Gets the details for a tag, if that tag isn't already defined.

        If the tag already exists, returns `None`.

        Args:
            model: The model that defines all the tags that already exist

        Returns:
            If valid, a tuple of the form `(id3_key, display_name, show_in_table)`
            Else `None`.
        """
        id3_key = self.id3_line_edit.text().strip()
        display_name = self.display_name_line_edit.text().strip()
        show_in_table = self.show_checkbox.isChecked()
        if not id3_key or not display_name:
            message = (
                "Tried to create a tag without display name or key.\n"
                f"ID3 Key: {id3_key}\n"
                f"Display Name: {display_name}\n"
                f"Show in Table: {show_in_table}"
            )
            logger.warning(message)
            QMessageBox.warning(self, "Missing Info", message)
            return None
        if any(
            tag.id3_key == id3_key or tag.display_name == display_name
            for tag in model.tags
        ):
            message = (
                "Tag with this key or display name already exists.\n"
                f"ID3 Key: {id3_key}\n"
                f"Display Name: {display_name}\n"
                f"Show in Table: {show_in_table}\n"
                "You can edit the existing display name, "
                "or remove the tag if you want a different key "
                "with the same display name."
            )
            logger.warning(message)
            QMessageBox.warning(self, "Tag Exists", message)
            return None
        return _TagDict(
            id3_key=id3_key,
            display_name=display_name,
            show_in_table=show_in_table,
        )

    def addToModel(self, model: TagModel) -> None:
        """Adds the created tag to the model, if it is valid.

        Args:
            model: The model that defines the currently existing tags.
        """
        tag = self._getValidTag(model)
        if tag is None:
            return
        model.addTag(**tag)

    def setupUi(self) -> None:
        """Create the interface for the dialog."""
        self.resize(300, 140)
        self.setWindowTitle("Add Tag")

        vertical_layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.id3_line_edit = QLineEdit(parent=self)
        form_layout.addRow("ID3 Key", self.id3_line_edit)

        self.display_name_line_edit = QLineEdit(self)
        form_layout.addRow("Display Name", self.display_name_line_edit)

        self.show_checkbox = QCheckBox("Show in Table")
        form_layout.addRow(self.show_checkbox)

        vertical_layout.addLayout(form_layout)

        button_box = QDialogButtonBox(
            self,
            orientation=Qt.Orientation.Horizontal,
            standardButtons=QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok,
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        vertical_layout.addWidget(button_box)
