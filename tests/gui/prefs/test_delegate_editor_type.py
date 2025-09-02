"""Tests for EditorTypeDelegate."""

from typing import cast
from unittest.mock import MagicMock

from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide6.QtWidgets import QComboBox, QStyleOptionViewItem, QWidget
from pytestqt.qtbot import QtBot

from music_modify.custom_types.enums import EditorType
from music_modify.gui.prefs.delegate_editor_type import EditorTypeDelegate


def test_EditorTypeDelegate_createEditor(qtbot: QtBot) -> None:
    """Tests that a combo box is created for the delegate."""
    widget = QWidget()
    qtbot.addWidget(widget)
    delegate = EditorTypeDelegate()
    editor = delegate.createEditor(widget, QStyleOptionViewItem(), QModelIndex())
    assert isinstance(editor, QComboBox)
    assert editor.count() == len(EditorType)
    for i, editor_type in enumerate(EditorType):
        assert editor.itemText(i) == editor_type.value


def test_EditorTypeDelegate_setEditorData(qtbot: QtBot) -> None:
    """Tests that setEditorData gets and sets the correct value."""
    parent = QWidget()
    qtbot.addWidget(parent)

    delegate = EditorTypeDelegate()

    editor = delegate.createEditor(parent, QStyleOptionViewItem(), QModelIndex())

    mock_index = MagicMock(spec=QModelIndex)
    mock_index.data.return_value = EditorType.SingleText

    delegate.setEditorData(editor, mock_index)

    combo_box = cast(QComboBox, editor)
    assert combo_box.currentText() == EditorType.SingleText.value


def test_EditorTypeDelegate_setModelData() -> None:
    """Tests that the model data gets set correctly when setModelData is called."""
    delegate = EditorTypeDelegate()

    mock_combo_box = MagicMock(spec=QComboBox)
    selected_editor_type = EditorType.MultipleText.value
    mock_combo_box.currentText.return_value = selected_editor_type

    mock_model = MagicMock(spec=QAbstractItemModel)
    mock_model.setData = MagicMock()

    mock_index = MagicMock(spec=QModelIndex)

    delegate.setModelData(mock_combo_box, mock_model, mock_index)

    cast(MagicMock, mock_model.setData).assert_called_once_with(
        mock_index, selected_editor_type, Qt.ItemDataRole.EditRole
    )
