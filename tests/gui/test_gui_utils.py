from PySide6.QtCore import QItemSelectionModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QTableWidget,
    QWidget,
)
from pytestqt.qtbot import QtBot  # pyright: ignore[reportMissingTypeStubs]

from music_modify.gui.utils import clearLayout, getSelectedRows


# noinspection PyTypeChecker
def test_getSelectedRows(qtbot: QtBot):
    table = QTableWidget(4, 2)
    qtbot.addWidget(table)
    table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    table.selectRow(2)
    assert getSelectedRows(table) == [2]

    model = table.model()
    selection_model = table.selectionModel()
    selection_model.clearSelection()
    selection_model.select(
        model.index(1, 0),
        QItemSelectionModel.SelectionFlag.Select
        | QItemSelectionModel.SelectionFlag.Rows,
    )
    selection_model.select(
        model.index(3, 0),
        QItemSelectionModel.SelectionFlag.Select
        | QItemSelectionModel.SelectionFlag.Rows,
    )
    assert getSelectedRows(table) == [1, 3]

    list_widget = QListWidget()
    for i in range(5):
        list_widget.insertItem(i, "")
    qtbot.addWidget(list_widget)
    list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
    list_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    model = list_widget.model()
    selection_model = list_widget.selectionModel()
    selection_model.select(
        model.index(2, 0),
        QItemSelectionModel.SelectionFlag.Select
        | QItemSelectionModel.SelectionFlag.Rows,
    )
    assert getSelectedRows(list_widget) == [2]
    selection_model.clearSelection()
    selection_model.select(
        model.index(1, 0),
        QItemSelectionModel.SelectionFlag.Select
        | QItemSelectionModel.SelectionFlag.Rows,
    )
    selection_model.select(
        model.index(3, 0),
        QItemSelectionModel.SelectionFlag.Select
        | QItemSelectionModel.SelectionFlag.Rows,
    )
    assert getSelectedRows(table) == [1, 3]


def test_clearLayout(qtbot: QtBot):
    widget1 = QWidget()
    layout1 = QHBoxLayout()
    widget2 = QLineEdit("This is some text")
    layout1.addWidget(widget2)
    widget1.setLayout(layout1)
    qtbot.addWidget(widget1)
    qtbot.addWidget(widget2)
    layout_to_check = widget1.layout()
    assert layout_to_check is not None
    clearLayout(layout_to_check)
    assert layout_to_check.count() == 0
