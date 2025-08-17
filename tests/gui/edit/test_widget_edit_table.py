from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from music_modify.gui.edit.widget_edit_table import EditTableWidget
from music_modify.gui.edit.widget_table_drag import DragTableWidget
from music_modify.gui.utils import selectRows


def test_EditTableWidget_init_data_None_labels_None(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    table_widget = EditTableWidget(widget, None)
    qtbot.addWidget(table_widget)

    assert table_widget.value == []
    assert table_widget.original == []
    assert table_widget.labels == ["Role", "Person"]
    assert isinstance(table_widget.main_widget, DragTableWidget)
    assert table_widget.main_widget.columnCount() == 2  # noqa: PLR2004


def test_EditTableWidget_init_data_None_labels_set(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    table_widget = EditTableWidget(widget, data=None, labels=["One", "Two"])
    qtbot.addWidget(table_widget)

    assert table_widget.value == []
    assert table_widget.original == []
    assert table_widget.labels == ["One", "Two"]
    assert isinstance(table_widget.main_widget, DragTableWidget)
    assert table_widget.main_widget.columnCount() == 2  # noqa: PLR2004


def test_EditTableWidget_init_data_set_labels_None(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    table_widget = EditTableWidget(widget, data=[["Some Role", "Some Name"]])
    qtbot.addWidget(table_widget)

    assert table_widget.value == [["Some Role", "Some Name"]]
    assert table_widget.original == [["Some Role", "Some Name"]]
    assert table_widget.labels == ["Role", "Person"]
    assert isinstance(table_widget.main_widget, DragTableWidget)
    assert table_widget.main_widget.columnCount() == 2  # noqa: PLR2004


def test_EditTableWidget_init_data_empty_labels_None(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    table_widget = EditTableWidget(widget, data=[])
    qtbot.addWidget(table_widget)

    assert table_widget.value == []
    assert table_widget.original == []
    assert table_widget.labels == ["Role", "Person"]
    assert isinstance(table_widget.main_widget, DragTableWidget)
    assert table_widget.main_widget.columnCount() == 2  # noqa: PLR2004


def test_EditTableWidget_init_data_set_labels_set(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    table_widget = EditTableWidget(
        widget, data=[["Some Role", "Some Name"]], labels=["One", "Two"]
    )
    qtbot.addWidget(table_widget)

    assert table_widget.value == [["Some Role", "Some Name"]]
    assert table_widget.original == [["Some Role", "Some Name"]]
    assert table_widget.labels == ["One", "Two"]
    assert isinstance(table_widget.main_widget, DragTableWidget)
    assert table_widget.main_widget.columnCount() == 2  # noqa: PLR2004


def test_EditTableWidget_addRow_None(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    table_widget = EditTableWidget(widget, None)
    qtbot.addWidget(table_widget)

    # Always have at least one row for editing
    assert table_widget.main_widget.rowCount() == 1
    assert table_widget.add_button is not None
    table_widget.add_button.click()
    assert table_widget.main_widget.rowCount() == 2  # noqa: PLR2004


def test_EditTableWidget_addRow_existing(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [["Some Role", "Some Person"]]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)
    assert table_widget.main_widget.model().rowCount() == len(data)
    assert table_widget.add_button is not None
    table_widget.add_button.click()
    # Ensure the row is added, but it doesn't mutate the original list
    assert table_widget.main_widget.model().rowCount() == len(data) + 1


def test_EditTableWidget_moveRowUp_valid(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [["First Role", "First Person"], ["Second Role", "Second Person"]]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]

    selectRows(table_widget.main_widget, [1])
    assert table_widget.up_button is not None
    table_widget.up_button.click()
    assert table_widget.value == [
        ["Second Role", "Second Person"],
        ["First Role", "First Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]


def test_EditTableWidget_moveRowUp_top(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [["First Role", "First Person"], ["Second Role", "Second Person"]]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]

    selectRows(table_widget.main_widget, [0])
    assert table_widget.up_button is not None
    table_widget.up_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]


def test_EditTableWidget_moveRowsUp_contiguous(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    selectRows(table_widget.main_widget, [1, 2])
    assert table_widget.up_button is not None
    table_widget.up_button.click()
    assert table_widget.value == [
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["First Role", "First Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]


def test_EditTableWidget_moveRowsUp_contiguous_with_top(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    selectRows(table_widget.main_widget, [0, 1])
    assert table_widget.up_button is not None
    table_widget.up_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]


def test_EditTableWidget_moveRowsUp_separate(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]

    selectRows(table_widget.main_widget, [1, 3])
    assert table_widget.up_button is not None
    table_widget.up_button.click()
    assert table_widget.value == [
        ["Second Role", "Second Person"],
        ["First Role", "First Person"],
        ["Fourth Role", "Fourth Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]


def test_EditTableWidget_moveRowsUp_separate_with_top(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]

    selectRows(table_widget.main_widget, [0, 2])
    assert table_widget.up_button is not None
    table_widget.up_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]


def test_EditTableWidget_moveRows_no_selection(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    # Ensure that nothing breaks when nothing selected and trying to move rows
    assert table_widget.up_button is not None
    table_widget.up_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.down_button is not None
    table_widget.down_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]


def test_EditTableWidget_moveRowDown_valid(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [["First Role", "First Person"], ["Second Role", "Second Person"]]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]

    selectRows(table_widget.main_widget, [0])
    assert table_widget.down_button is not None
    table_widget.down_button.click()
    assert table_widget.value == [
        ["Second Role", "Second Person"],
        ["First Role", "First Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]


def test_EditTableWidget_moveRowDown_bottom(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [["First Role", "First Person"], ["Second Role", "Second Person"]]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]

    selectRows(table_widget.main_widget, [1])
    assert table_widget.down_button is not None
    table_widget.down_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]


def test_EditTableWidget_moveRowsDown_contiguous(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    selectRows(table_widget.main_widget, [0, 1])
    assert table_widget.down_button is not None
    table_widget.down_button.click()
    assert table_widget.value == [
        ["Third Role", "Third Person"],
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]


def test_EditTableWidget_moveRowsDown_contiguous_with_bottom(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    selectRows(table_widget.main_widget, [1, 2])
    assert table_widget.down_button is not None
    table_widget.down_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]


def test_EditTableWidget_moveRowsDown_separate(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]

    selectRows(table_widget.main_widget, [0, 2])
    assert table_widget.down_button is not None
    table_widget.down_button.click()
    assert table_widget.value == [
        ["Second Role", "Second Person"],
        ["First Role", "First Person"],
        ["Fourth Role", "Fourth Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]


def test_EditTableWidget_moveRowsDown_separate_with_bottom(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]

    table_widget = EditTableWidget(widget, data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]

    selectRows(table_widget.main_widget, [1, 3])
    assert table_widget.down_button is not None
    table_widget.down_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Fourth Role", "Fourth Person"],
    ]


def test_EditTableWidget_removeRow(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [["First Role", "First Person"], ["Second Role", "Second Person"]]
    table_widget = EditTableWidget(widget, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]

    selectRows(table_widget.main_widget, [0])
    assert table_widget.remove_button is not None
    table_widget.remove_button.click()

    assert table_widget.value == [["Second Role", "Second Person"]]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]
    first_item = table_widget.main_widget.item(0, 0)
    assert first_item is not None
    assert first_item.text() == "Second Role"

    second_item = table_widget.main_widget.item(0, 1)
    assert second_item is not None
    assert second_item.text() == "Second Person"


def test_EditTableWidget_removeRow_no_selection(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [["First Role", "First Person"], ["Second Role", "Second Person"]]
    table_widget = EditTableWidget(widget, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]

    assert table_widget.remove_button is not None
    table_widget.remove_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]


def test_EditTableWidget_removeRow_single(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [["First Role", "First Person"]]
    table_widget = EditTableWidget(widget, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
    ]

    selectRows(table_widget.main_widget, [0])
    assert table_widget.remove_button is not None
    table_widget.remove_button.click()

    assert table_widget.value == []
    assert table_widget.original == [["First Role", "First Person"]]

    assert table_widget.main_widget.rowCount() == 1
    first_item = table_widget.main_widget.item(0, 0)
    assert first_item is not None
    assert first_item.text() == ""
    second_item = table_widget.main_widget.item(0, 1)
    assert second_item is not None
    assert second_item.text() == ""


def test_EditTableWidget_clear(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [["First Role", "First Person"], ["Second Role", "Second Person"]]
    table_widget = EditTableWidget(widget, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]

    assert table_widget.clear_button is not None
    table_widget.clear_button.click()
    assert table_widget.value == []
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]


def test_EditTableWidget_reset(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    table_widget = EditTableWidget(widget, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.clear_button is not None
    table_widget.clear_button.click()
    assert table_widget.value == []
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.reset_button is not None
    table_widget.reset_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]


def test_EditTableWidget_update_existing(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    table_widget = EditTableWidget(widget, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    first_row_person = table_widget.main_widget.item(0, 1)
    assert first_row_person is not None
    first_row_person.setText("New Person")
    assert table_widget.value == [
        ["First Role", "New Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    first_row_role = table_widget.main_widget.item(0, 0)
    assert first_row_role is not None
    first_row_role.setText("New Role")
    assert table_widget.value == [
        ["New Role", "New Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    second_row_role = table_widget.main_widget.item(1, 0)
    assert second_row_role is not None
    second_row_role.setText("New Role")
    assert table_widget.value == [
        ["New Role", "New Person"],
        ["New Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]


def test_EditTableWidget_update_add_new(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    table_widget = EditTableWidget(widget, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    assert table_widget.add_button is not None
    table_widget.add_button.click()
    assert table_widget.main_widget.rowCount() == 4  # noqa: PLR2004
    last_row_role = table_widget.main_widget.item(3, 0)
    assert last_row_role is not None
    last_row_role.setText("Extra Role")
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    last_row_person = table_widget.main_widget.item(3, 1)
    assert last_row_person is not None
    last_row_person.setText("Extra Person")
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Extra Role", "Extra Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
