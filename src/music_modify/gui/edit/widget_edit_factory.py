"""Module that defines an EditWidgetFactory.

This class is used to generate widgets for editing metadata,
based on the format of the data.
"""

import copy
from typing import TypeVar, cast

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

ValueT = TypeVar("ValueT", bound=SongEditData)

EditAbstractWidgetType = (
    EditAbstractWidget[SongListData]
    | EditAbstractWidget[SongTableData]
    | EditAbstractWidget[str]
)


class EditWidgetFactory:
    """Creates widgets displayed on an EditDialog."""

    # Having a class here is probably overkill.
    # But it makes it neater when calling, and keeps it in scope.

    @staticmethod
    def createWidget(
        parent: QWidget,
        tag: SongTag,
        data: SongEditData | None,
    ) -> EditAbstractWidgetType:
        """Creates the required widget based on the tag and data format.

        Args:
            parent: Widget that the created widget should be owned by.
            tag: Holds the format that the data should take, and other information.
            data: The actual value that the tag currently stores.
        """
        if tag.frame_type == TagType.People:
            # Is a people tag, so table with current data
            data = cast(
                SongTableData | None,
                copy.deepcopy(data) if data is not None else None,
            )
            return EditTableWidget(parent, data)
        if tag.allow_multiple:
            # Allow multiple is true, so list with current data

            # Send a copy otherwise when checking if a value is changed,
            # it will always be false, because it's comparing the two
            # changed values
            data = cast(SongListData | None, data)
            data = data.copy() if data is not None else None
            return EditListWidget(parent, data)
        # Only allows a single value, which can be a string, ID3TimeStamp or None.
        # Show in LineEdit.
        data = cast(str | None, data)
        return EditLineWidget(parent, data)
