from PySide6.QtWidgets import QDialog, QWidget

from music_modify.custom_types.enums import TagGroup
from .ui_dialog_tag import Ui_TagDialog
from music_modify.custom_types import SongTag
from music_modify.models import TagModel


class TagDialog(QDialog, Ui_TagDialog):
    def __init__(
        self, parent: QWidget | None, tags: list[SongTag], tag_group: TagGroup
    ):
        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]
        self.setWindowTitle(tag_group.value)

        self.model: TagModel = TagModel(tags)
        self.tag_table.setModel(self.model)
        if tag_group == TagGroup.CustomTags:
            self.tag_table.resizeColumnsToContents()
