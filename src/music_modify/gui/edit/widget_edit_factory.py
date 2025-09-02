"""Module that defines an EditWidgetFactory.

This class is used to generate widgets for editing metadata,
based on the format of the data.
"""

import copy
from typing import cast

from PySide6.QtWidgets import QLineEdit, QListWidget, QWidget

from music_modify.custom_types.aliases import (
    SongEditData,
    SongListData,
    SongTableData,
)
from music_modify.custom_types.enums import EditorType
from music_modify.custom_types.songtag import SongTag

from .widget_edit_abstract import EditAbstractWidget
from .widget_edit_line import EditLineWidget
from .widget_edit_list import EditListWidget
from .widget_edit_table import EditTableWidget
from .widget_table_drag import DragTableWidget

type EditAbstractWidgetType = (
    EditAbstractWidget[SongListData, QListWidget]
    | EditAbstractWidget[SongTableData, DragTableWidget]
    | EditAbstractWidget[str, QLineEdit]
)


class EditWidgetFactory:
    """Creates widgets displayed on an EditDialog."""

    # Having a class here is probably overkill.
    # But it makes it neater when calling, and keeps it in scope.

    # noinspection PyTypeHints
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
        match tag.editor_type:
            case EditorType.PeopleValue:
                data = cast(
                    SongTableData | None,
                    copy.deepcopy(data) if data is not None else None,
                )
                return EditTableWidget(parent, data)
            case EditorType.MultipleText:
                if isinstance(data, str):
                    data = [data]
                data = cast(SongListData | None, data)
                data = data.copy() if data is not None else None
                return EditListWidget(parent, data)
            case EditorType.SingleText:
                data = cast(str | None, data)
                return EditLineWidget(parent, data)
            case _:
                raise ValueError(
                    f"editor_type had an unsupported value: {tag.editor_type}"
                )
