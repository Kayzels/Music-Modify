"""Module that managed an EditorTypeDelegate.

This delegate is used for displaying a QComboBox for EditorType for tags.
"""

from typing import cast, override

from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QWidget,
)

from music_modify.core.enums import EditorType


class EditorTypeDelegate(QStyledItemDelegate):
    """A delegate for the EditorType column that provides a QComboBox."""

    @override
    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
        /,
    ) -> QWidget:
        """Creates the QComboBox editor for the EditorType column."""
        editor = QComboBox(parent)
        for editor_type in EditorType:
            editor.addItem(editor_type.value)
        return editor

    @override
    def setEditorData(
        self, editor: QWidget, index: QModelIndex | QPersistentModelIndex, /
    ) -> None:
        combo_box = cast(QComboBox, editor)
        current_editor_type: EditorType = index.data(Qt.ItemDataRole.EditRole)

        for i in range(combo_box.count()):
            if combo_box.itemText(i) == current_editor_type.value:
                combo_box.setCurrentIndex(i)
                break

    @override
    def setModelData(
        self,
        editor: QWidget,
        model: QAbstractItemModel,
        index: QModelIndex | QPersistentModelIndex,
        /,
    ) -> None:
        combo_box = cast(QComboBox, editor)

        model.setData(index, combo_box.currentText(), Qt.ItemDataRole.EditRole)
