import logging

from PySide6.QtWidgets import QDialog, QMessageBox, QWidget

from music_modify.models.tag_model import TagModel

from .ui_dialog_prefs_tag_add import Ui_PrefsTagAddDialog

logger = logging.getLogger(__name__)


class PrefsTagAddDialog(QDialog, Ui_PrefsTagAddDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)

    def _getValidTag(self, model: TagModel) -> tuple[str, str, bool] | None:
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
                "or remove the tag if you want a different key with the same display name."
            )
            logger.warning(message)
            QMessageBox.warning(self, "Tag Exists", message)
            return None
        return id3_key, display_name, show_in_table

    def addToModel(self, model: TagModel):
        tag = self._getValidTag(model)
        if tag is None:
            return
        model.addTag(*tag)
