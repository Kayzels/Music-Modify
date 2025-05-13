import copy
from typing import cast

from PySide6.QtWidgets import QWidget

from music_modify.custom_types.aliases import (
    SongEditData,
    SongListData,
    SongTableData,
)
from music_modify.custom_types.enums import TagType
from music_modify.custom_types.songtag import SongTag

from .widget_edit_abstract import EditAbstractWidget
from .widget_edit_line import EditLineWidget
from .widget_edit_list import EditListWidget
from .widget_edit_table import EditTableWidget


class EditWidgetFactory:
    # Having a class here is probably overkill.
    # But it makes it neater when calling, and keeps it in scope.

    @staticmethod
    def createWidget(
        parent: QWidget, tag: SongTag, data: SongEditData | None
    ) -> EditAbstractWidget:
        # def createWidget(
        #     parent: QWidget, tag: SongTag, data: SongGroupData
        # ) -> EditAbstractWidget:
        if tag.frame_type == TagType.People:
            # Is a people tag, so table with current data
            data = cast(
                SongTableData | None,
                copy.deepcopy(data) if data is not None else None,
            )
            return EditTableWidget(parent, data)
        elif tag.allow_multiple:
            # Allow multiple is true, so list with current data

            # Send a copy otherwise when checking if a value is changed,
            # it will always be false, because it's comparing the two
            # changed values
            data = cast(SongListData | None, data)
            data = data.copy() if data is not None else None
            return EditListWidget(parent, data)
        else:
            # Only allows a single value, which can be a string, ID3TimeStamp or None.
            # Show in LineEdit.
            data = cast(str | None, data)
            return EditLineWidget(parent, data)
