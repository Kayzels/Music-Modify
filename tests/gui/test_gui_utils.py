"""Tests for utilities related to GUI."""

from PySide6.QtCore import QItemSelectionModel, QSortFilterProxyModel, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLineEdit,
    QListView,
    QListWidget,
    QScrollArea,
    QTableWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from pytestqt.qtbot import QtBot

from music_modify.gui.utils import clearLayout, createTab, getSelectedRows, selectRows


def test_getSelectedRows_no_selection(qtbot: QtBot) -> None:
    """Test that getSelectedRows returns an empty list when there is no selection."""
    table = QTableWidget(4, 2)
    qtbot.addWidget(table)
    table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    assert getSelectedRows(table) == []


# noinspection PyTypeChecker
def test_getSelectedRows_normal(qtbot: QtBot) -> None:
    """Test that getSelectedRows gets the correct row numbers from the widget."""
    table = QTableWidget(4, 2)
    qtbot.addWidget(table)
    table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    table.selectRow(2)
    assert getSelectedRows(table) == [2]

    selectRows(table, [1, 3])
    assert getSelectedRows(table) == [1, 3]

    list_widget = QListWidget()
    for i in range(5):
        list_widget.insertItem(i, "")
    qtbot.addWidget(list_widget)
    list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
    list_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    selectRows(list_widget, [2])
    assert getSelectedRows(list_widget) == [2]
    selectRows(list_widget, [1, 3])
    assert getSelectedRows(list_widget) == [1, 3]


def test_getSelectedRows_with_proxy_model(qtbot: QtBot) -> None:
    """Test that getSelectedRows gets the correct rows when a proxy model is used."""
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


def test_clearLayout_normal(qtbot: QtBot) -> None:
    """Test that clearLayout clears layouts for widgets."""
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
    """Test that clearLayout is called recursively when needed."""
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

    assert parent_layout.count() == 2
    assert first_layout.count() == 2
    assert second_layout.count() == 2

    clearLayout(parent_layout)

    assert parent_layout.count() == 0
    # The other layouts might still exist, and might not,
    # so they can't be checked.
    # But they won't be accessible where they were previously used.


def test_createTab(qtbot: QtBot) -> None:
    """Test that a tab is created correctly, and that a layout is returned."""
    tab_widget = QTabWidget()
    qtbot.addWidget(tab_widget)

    layout1 = createTab("First Tab", tab_widget, QVBoxLayout)
    layout2 = createTab("Second Tab", tab_widget, QHBoxLayout)

    assert isinstance(layout1, QVBoxLayout)
    assert isinstance(layout2, QHBoxLayout)
    assert tab_widget.count() == 2
    assert tab_widget.tabText(0) == "First Tab"
    assert tab_widget.tabText(1) == "Second Tab"
    assert isinstance(tab_widget.widget(0), QScrollArea)
    assert isinstance(tab_widget.widget(1), QScrollArea)
