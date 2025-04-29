from PySide6.QtWidgets import QDialog, QWidget

from music_modify.custom_types import TagInfo
from music_modify.models import TagModel

from .ui_dialog_tag import Ui_TagDialog


class TagDialog(QDialog, Ui_TagDialog):
    def __init__(self, parent: QWidget | None, tags: list[TagInfo]):
        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]
        self.setWindowTitle("Edit Tags")

        self.model: TagModel = TagModel(tags)
        self.tag_table.setModel(self.model)
        self.tag_table.resizeColumnsToContents()
