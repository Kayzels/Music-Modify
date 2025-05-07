# pyright: reportPrivateImportUsage=false
import copy
from typing import cast

from PySide6.QtWidgets import QWidget

from music_modify.custom_types.aliases import (
    SongGroupData,
    SongLineData,
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
        parent: QWidget, tag: SongTag, data: SongGroupData
    ) -> EditAbstractWidget:
        group: tuple[TagType, bool] = (tag.frame_type, tag.allow_multiple)
        match group:
            case (TagType.People, _):
                # Is a people tag, so table with current data
                data = cast(
                    SongTableData, copy.deepcopy(data) if data is not None else None
                )
                return EditTableWidget(parent, data)
            case (_, True):
                # Allow multiple is true, so list with current data

                # Send a copy otherwise when checking if a value is changed,
                # it will always be false, because it's comparing the two
                # changed values
                data = cast(SongListData, data.copy() if data is not None else None)
                return EditListWidget(parent, data)
            case (_, False):
                # Only allows a single value, which can be a string, ID3TimeStamp or None.
                # Show in LineEdit.
                data = cast(SongLineData, data)
                return EditLineWidget(parent, data)
