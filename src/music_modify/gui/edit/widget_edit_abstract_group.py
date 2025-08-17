"""Module that defines an EditAbstractGroupWidget.

This widget is the abstract class used for widgets
in an EditDialog that display groups of values,
rather than a single value.
"""

from abc import ABC
from typing import TYPE_CHECKING, override

from PySide6.QtWidgets import QBoxLayout, QWidget

from music_modify.custom_types.aliases import SongListData, SongTableData
from music_modify.custom_types.enums import EditButton
from music_modify.gui.meta import ABCQMeta
from music_modify.gui.mixins.row_operation_mixin import RowOperationMixin

from .widget_edit_abstract import EditAbstractWidget

if TYPE_CHECKING:
    from PySide6.QtWidgets import QToolButton


class EditAbstractGroupWidget[ValueG: SongListData | SongTableData, WidgetT: QWidget](
    EditAbstractWidget[ValueG, WidgetT],
    RowOperationMixin,
    ABC,
    metaclass=ABCQMeta,
):
    """Abstract class for widgets on an EditDialog that contain multiple items.

    These items can be displayed in lists or tables.
    """

    def __init__(self, parent: QWidget, data: ValueG | None) -> None:
        """Create an EditAbstractGroupWidget.

        Args:
            parent: The widget that this widget should be displayed on.
            data: The data to be displayed on this widget.
        """
        super().__init__(parent, data)

        self.down_button: QToolButton
        "Button used for moving rows down in the widget."
        self.up_button: QToolButton
        "Button used for moving rows up in the widget."
        self.add_button: QToolButton
        "Button that adds a row to the widget."
        self.remove_button: QToolButton
        "Button that removes the selected row from the widget."

    # noinspection PyTypeChecker
    @override
    def createButtons(
        self,
        buttons: EditButton = EditButton.Up
        | EditButton.Down
        | EditButton.Add
        | EditButton.Remove,
        direction: QBoxLayout.Direction = QBoxLayout.Direction.TopToBottom,
    ) -> QBoxLayout:
        button_layout = super().createButtons(buttons, direction)

        new_buttons = self.createOperationButtons(self, buttons)
        for new_button in new_buttons:
            button_layout.addWidget(new_button)

        return button_layout
