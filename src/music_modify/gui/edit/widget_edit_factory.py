"""Module that defines an EditWidgetFactory.

This class is used to generate widgets for editing metadata,
based on the format of the data.
"""

import logging
from typing import ClassVar, TypedDict

from PySide6.QtWidgets import QWidget

from music_modify.core.enums import EditorType
from music_modify.custom_types.tag_value import (
    AbstractTagValue,
    PairedTextTagValue,
    TagValueFactory,
    TextTagValue,
)

from .widget_edit_abstract import EditAbstractWidget
from .widget_edit_line import EditLineWidget
from .widget_edit_list import EditListWidget
from .widget_edit_table import EditTableWidget

logger = logging.getLogger(__name__)


class EditWidgetFactory:
    """Creates widgets displayed on an EditDialog."""

    editor_types: ClassVar[dict[str, EditorType]] = {}

    @classmethod
    def createWidget(
        cls,
        id3_key: str,
        current_value: AbstractTagValue | None,
        parent: QWidget | None = None,
    ) -> EditAbstractWidget | None:
        """Creates the required widget based on the tag and data format.

        Args:
            id3_key: Key used to access and set the tag in an ID3 object.
            editor_type: Fallback type used if there is ambiguity based on the data.
            current_value: Value that should be sotred and displayed in the widget.
            parent: Widget that the created widget should be owned by.

        It uses the type of `current_value` and the internals if available.
        If `current_value` is None, it falls back to generating an AbstractTagValue
        for a specific id3 key.

        This allows the correct widget to be based on the data,
        in cases where (for example) the `editor_type` is said to be single text,
        but the tag has multiple values, which would work better in a list.

        If `current_value` stores a list containing one string, it is possible
        that the widget to be created is either a line widget or a list widget.
        So it uses the editor type to determine which,
        and falls back to line if uncertain.
        """
        editor_type = cls.editor_types.get(id3_key, EditorType.Automatic)
        created_widget: EditAbstractWidget | None = None
        if current_value is None:
            current_value = TagValueFactory.createTagValue(
                value_input=None, id3_key=id3_key
            )

        class _WidgetArgs(TypedDict):
            initial_value: AbstractTagValue | None
            parent: QWidget | None

        widget_args: _WidgetArgs = {"initial_value": current_value, "parent": parent}
        match current_value:
            case TextTagValue():
                if (
                    len(current_value.value) > 1
                    or editor_type == EditorType.MultipleText
                ):
                    created_widget = EditListWidget(**widget_args)
                else:
                    created_widget = EditLineWidget(**widget_args)
            case PairedTextTagValue():
                created_widget = EditTableWidget(**widget_args)
            case None:
                logger.warning(
                    f"Unable to find a valid AbstractTagValue to make a widget for {id3_key}."
                )
                created_widget = None
            case _:
                logger.info(
                    f"TagValue instance {type(current_value)} is valid, "
                    + "but no widget for this type exists yet."
                )
                created_widget = None
        return created_widget


# TODO: Should we have a "blank" widget for the values we don't support/know
