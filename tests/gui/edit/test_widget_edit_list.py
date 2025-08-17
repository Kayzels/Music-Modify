from PySide6.QtWidgets import QListWidget, QWidget
from pytestqt.qtbot import QtBot

from music_modify.gui.edit.widget_edit_list import EditListWidget
from music_modify.gui.utils import selectRows


def test_EditListWidget_init_None(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    list_widget = EditListWidget(widget, None)
    qtbot.addWidget(list_widget)
    assert list_widget.value == []
    assert list_widget.original == []
    assert isinstance(list_widget.main_widget, QListWidget)


def test_EditListWidget_init_empty(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    list_widget = EditListWidget(widget, [])
    qtbot.addWidget(list_widget)
    assert list_widget.value == []
    assert list_widget.original == []
    assert isinstance(list_widget.main_widget, QListWidget)


def test_EditListWidget_init(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    list_widget = EditListWidget(widget, ["One"])
    qtbot.addWidget(list_widget)
    assert list_widget.value == ["One"]
    assert list_widget.original == ["One"]


def test_EditListWidget_addRow_None(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    list_widget = EditListWidget(widget, None)
    qtbot.addWidget(list_widget)
    assert list_widget.main_widget.model().rowCount() == 1
    assert list_widget.add_button is not None
    list_widget.add_button.click()
    assert list_widget.main_widget.model().rowCount() == 2  # noqa: PLR2004


def test_EditListWidget_addRow_existing(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)
    assert list_widget.main_widget.model().rowCount() == len(data)
    assert list_widget.add_button is not None
    list_widget.add_button.click()
    # Ensure the row is added, but it doesn't mutate the original list
    assert list_widget.main_widget.model().rowCount() == len(data) + 1


def test_EditListWidget_moveRowUp_valid(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two"]

    selectRows(list_widget.main_widget, [1])
    assert list_widget.up_button is not None
    list_widget.up_button.click()
    assert list_widget.value == ["Two", "One"]


def test_EditListWidget_moveRowUp_top(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two"]

    selectRows(list_widget.main_widget, [0])
    assert list_widget.up_button is not None
    list_widget.up_button.click()
    assert list_widget.value == ["One", "Two"]


def test_EditListWidget_moveRowsUp_contiguous(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two", "Three"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two", "Three"]

    selectRows(list_widget.main_widget, [1, 2])
    assert list_widget.up_button is not None
    list_widget.up_button.click()
    assert list_widget.value == ["Two", "Three", "One"]


def test_EditListWidget_moveRowsUp_contiguous_with_top(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two", "Three"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two", "Three"]

    selectRows(list_widget.main_widget, [0, 1])
    assert list_widget.up_button is not None
    list_widget.up_button.click()
    assert list_widget.value == ["One", "Two", "Three"]


def test_EditListWidget_moveRowsUp_separate(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two", "Three", "Four"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two", "Three", "Four"]

    selectRows(list_widget.main_widget, [1, 3])
    assert list_widget.up_button is not None
    list_widget.up_button.click()
    assert list_widget.value == ["Two", "One", "Four", "Three"]


def test_EditListWidget_moveRowsUp_separate_with_top(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two", "Three", "Four"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two", "Three", "Four"]

    selectRows(list_widget.main_widget, [0, 2])
    assert list_widget.up_button is not None
    list_widget.up_button.click()
    assert list_widget.value == ["One", "Two", "Three", "Four"]


def test_EditListWidget_moveRows_no_selection(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two"]

    # Ensure that nothing breaks when nothing selected and trying to move rows
    assert list_widget.up_button is not None
    list_widget.up_button.click()
    assert list_widget.value == ["One", "Two"]
    assert list_widget.down_button is not None
    list_widget.down_button.click()
    assert list_widget.value == ["One", "Two"]


def test_EditListWidget_moveRowDown_valid(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two"]

    selectRows(list_widget.main_widget, [0])
    assert list_widget.down_button is not None
    list_widget.down_button.click()
    assert list_widget.value == ["Two", "One"]


def test_EditListWidget_moveRowDown_bottom(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two"]

    selectRows(list_widget.main_widget, [1])
    assert list_widget.down_button is not None
    list_widget.down_button.click()
    assert list_widget.value == ["One", "Two"]


def test_EditListWidget_moveRowsDown_contiguous(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two", "Three"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two", "Three"]

    selectRows(list_widget.main_widget, [0, 1])
    assert list_widget.down_button is not None
    list_widget.down_button.click()
    assert list_widget.value == ["Three", "One", "Two"]


def test_EditListWidget_moveRowsDown_contiguous_with_bottom(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two", "Three"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two", "Three"]

    selectRows(list_widget.main_widget, [1, 2])
    assert list_widget.down_button is not None
    list_widget.down_button.click()
    assert list_widget.value == ["One", "Two", "Three"]


def test_EditListWidget_moveRowsDown_separate(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two", "Three", "Four"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two", "Three", "Four"]

    selectRows(list_widget.main_widget, [0, 2])
    assert list_widget.down_button is not None
    list_widget.down_button.click()
    assert list_widget.value == ["Two", "One", "Four", "Three"]


def test_EditListWidget_moveRowsDown_separate_with_bottom(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two", "Three", "Four"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two", "Three", "Four"]

    selectRows(list_widget.main_widget, [1, 3])
    assert list_widget.down_button is not None
    list_widget.down_button.click()
    assert list_widget.value == ["One", "Two", "Three", "Four"]


def test_EditListWidget_removeRow(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two"]

    selectRows(list_widget.main_widget, [0])
    assert list_widget.remove_button is not None
    list_widget.remove_button.click()

    assert list_widget.value == ["Two"]
    assert list_widget.original == ["One", "Two"]

    assert list_widget.main_widget.item(0).text() == "Two"


def test_EditListWidget_removeRow_no_selection(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two"]
    assert list_widget.remove_button is not None
    list_widget.remove_button.click()
    assert list_widget.value == ["One", "Two"]


def test_EditListWidget_removeRow_single(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One"]

    selectRows(list_widget.main_widget, [0])
    assert list_widget.remove_button is not None
    list_widget.remove_button.click()

    assert list_widget.value == []
    assert list_widget.original == ["One"]

    assert list_widget.main_widget.model().rowCount() == 1
    assert list_widget.main_widget.item(0).text() == ""


def test_EditListWidget_clear(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two"]

    assert list_widget.clear_button is not None
    list_widget.clear_button.click()
    assert list_widget.value == []
    assert list_widget.original == ["One", "Two"]
    assert list_widget.main_widget.model().rowCount() == 1
    assert list_widget.main_widget.item(0).text() == ""


def test_EditListWidget_reset(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two"]
    assert list_widget.clear_button is not None
    list_widget.clear_button.click()
    assert list_widget.value == []
    assert list_widget.original == ["One", "Two"]
    assert list_widget.reset_button is not None
    list_widget.reset_button.click()
    assert list_widget.value == ["One", "Two"]


def test_EditListWidget_updateValue(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = ["One", "Two"]

    list_widget = EditListWidget(widget, data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == ["One", "Two"]
    list_widget.main_widget.item(0).setText("New")
    assert list_widget.value == ["New", "Two"]
    assert list_widget.original == ["One", "Two"]
