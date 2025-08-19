from PySide6.QtCore import QItemSelectionModel, QSortFilterProxyModel, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLineEdit,
    QListView,
    QListWidget,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)
from pytestqt.qtbot import QtBot

from music_modify.gui.utils import clearLayout, getSelectedRows


# noinspection PyTypeChecker
def test_getSelectedRows(qtbot: QtBot) -> None:
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


def test_getSelectedRows_with_proxy_model(qtbot: QtBot) -> None:
    source_model = QStandardItemModel(4, 1)
    for i in range(4):
        source_model.setItem(i, 0, QStandardItem(f"Item {i}"))

    proxy_model = QSortFilterProxyModel()
    proxy_model.setSourceModel(source_model)
    proxy_model.sort(0, Qt.SortOrder.DescendingOrder)

    list_view = QListView()
    list_view.setModel(proxy_model)
    qtbot.addWidget(list_view)

    list_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
    list_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    selection_model = list_view.selectionModel()
    selection_model.select(
        proxy_model.index(0, 0),  # Should be source row 3 after sorting
        QItemSelectionModel.SelectionFlag.Select
        | QItemSelectionModel.SelectionFlag.Rows,
    )

    selection_model = list_view.selectionModel()
    selection_model.select(
        proxy_model.index(2, 0),  # Should be source row 1 after sorting
        QItemSelectionModel.SelectionFlag.Select
        | QItemSelectionModel.SelectionFlag.Rows,
    )

    selected_source_rows = getSelectedRows(list_view)
    assert sorted(selected_source_rows) == [1, 3]


def test_clearLayout(qtbot: QtBot) -> None:
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


def test_clearLayout_recursive(qtbot: QtBot) -> None:
    parent_widget = QWidget()
    qtbot.addWidget(parent_widget)
    parent_layout = QVBoxLayout()
    parent_widget.setLayout(parent_layout)

    first_layout = QHBoxLayout()
    second_layout = QHBoxLayout()

    parent_layout.addLayout(first_layout)
    parent_layout.addLayout(second_layout)

    first_inner_layout_one = QVBoxLayout()
    first_inner_layout_two = QVBoxLayout()
    first_layout.addLayout(first_inner_layout_one)
    first_layout.addLayout(first_inner_layout_two)

    second_inner_layout_one = QVBoxLayout()
    second_inner_layout_two = QVBoxLayout()
    second_layout.addLayout(second_inner_layout_one)
    second_layout.addLayout(second_inner_layout_two)

    assert parent_layout.count() == 2  # noqa: PLR2004
    assert first_layout.count() == 2  # noqa: PLR2004
    assert second_layout.count() == 2  # noqa: PLR2004

    clearLayout(parent_layout)

    assert parent_layout.count() == 0
    # The other layouts might still exist, and might not,
    # so they can't be checked.
    # But they won't be accessible where they were previously used.
