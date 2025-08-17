from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from music_modify.gui.edit.widget_edit_line import EditLineWidget


def test_EditLineWidget_init(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    line_edit = EditLineWidget(widget, "Name")
    qtbot.addWidget(line_edit)
    assert line_edit.value == "Name"
    assert line_edit.original == "Name"


def test_EditLineWidget_init_None(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    line_edit = EditLineWidget(widget, data=None)
    qtbot.addWidget(line_edit)
    assert line_edit.value == ""
    assert line_edit.original == ""


def test_EditLineWidget_update(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    line_edit = EditLineWidget(widget, "Name")
    qtbot.addWidget(line_edit)
    assert line_edit.value == "Name"
    assert line_edit.original == "Name"
    line_edit.main_widget.setText("New Value")
    line_edit.main_widget.editingFinished.emit()
    assert line_edit.value == "New Value"
    assert line_edit.original == "Name"


def test_EditLineWidget_value_set(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    line_edit = EditLineWidget(widget, "Original")
    qtbot.addWidget(line_edit)
    assert line_edit.value == "Original"
    line_edit.value = "New Value"
    assert line_edit.value == "New Value"


def test_EditLineWidget_clear(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    line_edit = EditLineWidget(widget, "Name")
    qtbot.addWidget(line_edit)
    assert line_edit.value == "Name"
    assert line_edit.original == "Name"
    line_edit.clear()
    assert line_edit.value == ""
    assert line_edit.main_widget.text() == ""
    assert line_edit.original == "Name"


def test_EditLineWidget_reset(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    line_edit = EditLineWidget(widget, "Name")
    qtbot.addWidget(line_edit)
    assert line_edit.value == "Name"
    assert line_edit.original == "Name"
    line_edit.main_widget.setText("New Value")
    line_edit.main_widget.editingFinished.emit()
    assert line_edit.value == "New Value"
    assert line_edit.original == "Name"
    line_edit.reset()
    assert line_edit.value == "Name"
    assert line_edit.main_widget.text() == "Name"
    assert line_edit.original == "Name"
    line_edit.clear()
    assert line_edit.value == ""
    assert line_edit.main_widget.text() == ""
    assert line_edit.original == "Name"
    line_edit.reset()
    assert line_edit.value == "Name"
    assert line_edit.main_widget.text() == "Name"
