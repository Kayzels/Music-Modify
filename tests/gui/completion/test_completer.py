"""Tests for Completer."""

# pyright: reportPrivateUsage = false

from typing import cast
from unittest.mock import MagicMock, Mock

from PySide6.QtCore import (
    QEvent,
    QModelIndex,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTimer,
)
from PySide6.QtGui import QKeyEvent, QMouseEvent, QScreen
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QListView,
    QScrollBar,
    QStyle,
    QWidget,
)
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.enums import NavDirection
from music_modify.gui.completion._complete_model import CompleteModel
from music_modify.gui.completion._completer import Completer


def test_Completer_init_defaults(qtbot: QtBot) -> None:
    """Tests that a Completer sets default values correctly."""
    widget = QWidget()
    qtbot.addWidget(widget)
    completer = Completer(widget)
    qtbot.addWidget(completer)

    assert not completer.disable_popup
    assert completer.max_visible_items == 7
    assert completer.tab_accepts_uncompleted_text
    assert completer.focusPolicy() == Qt.FocusPolicy.NoFocus


def _createCompleter(qtbot: QtBot) -> tuple[QWidget, Completer]:
    widget = QWidget()
    qtbot.addWidget(widget)
    completer = Completer(widget)
    return widget, completer


def test_Completer_hide(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that the hide method unsets the current index and calls super hide."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "setCurrentIndex", Mock())
    monkeypatch.setattr(QListView, "hide", Mock())

    completer.hide()
    cast(Mock, completer.setCurrentIndex).assert_called_once_with(QModelIndex())
    cast(Mock, QListView.hide).assert_called_once()


def test_Completer_chooseItem_not_visible(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that chooseItem does nothing when completer not visible."""
    _, completer = _createCompleter(qtbot)

    completer.isVisible = Mock(return_value=False)
    index = MagicMock(spec=QModelIndex, isValid=Mock(return_value=True))

    monkeypatch.setattr(completer, "hide", Mock())

    with qtbot.assertNotEmitted(completer.item_selected):
        completer.chooseItem(index)

    cast(Mock, completer.hide).assert_not_called()


def test_Completer_chooseItem_visible(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that chooseItem selects an item when completer visible."""
    _, completer = _createCompleter(qtbot)

    completer.isVisible = Mock(return_value=True)
    index = MagicMock(spec=QModelIndex, isValid=Mock(return_value=True))

    monkeypatch.setattr(completer, "hide", Mock())

    mock_model = MagicMock()
    mock_model.data.return_value = "Test Item"
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))

    with qtbot.waitSignal(completer.item_selected, timeout=1000) as blocker:
        completer.chooseItem(index)
    assert blocker.args == ["Test Item"]

    cast(Mock, completer.hide).assert_called_once()
    cast(Mock, completer.model().data).assert_called_once_with(
        index, Qt.ItemDataRole.UserRole
    )


def test_Completer_setItems_not_visible(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that setItems does nothing when completer not visible."""
    _, completer = _createCompleter(qtbot)

    completer.isVisible = Mock(return_value=False)
    items: tuple[str, ...] = ("a", "b")

    mock_model = MagicMock()
    mock_model.setItems = Mock(return_value=None)
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))

    with qtbot.assertNotEmitted(completer.relayout_needed):
        completer.setItems(items)
    mock_model.setItems.assert_called_once_with(items)


def test_Completer_setItems_visible(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that setItems updates the model when completer visible."""
    _, completer = _createCompleter(qtbot)

    completer.isVisible = Mock(return_value=True)
    items: tuple[str, ...] = ("a", "b")

    mock_model = MagicMock()
    mock_model.setItems = Mock(return_value=None)
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))

    with qtbot.waitSignal(completer.relayout_needed, timeout=1000):
        completer.setItems(items)
    mock_model.setItems.assert_called_once_with(items)


def test_Completer_setCompletionPrefix_not_visible(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that setCompletionPrefix does nothing when completer not visible."""
    _, completer = _createCompleter(qtbot)

    completer.isVisible = Mock(return_value=False)
    prefix = "test"

    mock_model = MagicMock()
    mock_model.setCompletionPrefix = Mock(return_value=None)
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))

    with qtbot.assertNotEmitted(completer.relayout_needed):
        completer.setCompletionPrefix(prefix)
    mock_model.setCompletionPrefix.assert_called_once_with(prefix)


def test_Completer_setCompletionPrefix_visible(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that setCompletionPrefix sets the model prefix when completer is visible."""
    _, completer = _createCompleter(qtbot)

    completer.isVisible = Mock(return_value=True)
    prefix = "test"

    mock_model = MagicMock()
    mock_model.setCompletionPrefix = Mock(return_value=None)
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))

    with qtbot.waitSignal(completer.relayout_needed, timeout=1000):
        completer.setCompletionPrefix(prefix)
    mock_model.setCompletionPrefix.assert_called_once_with(prefix)


@pytest.mark.parametrize(
    ("direction", "expected_index"),
    [
        pytest.param(NavDirection.Next, 0, id="next_selects_first"),
        pytest.param(NavDirection.Previous, 4, id="prev_selects_last"),
    ],
)
def test_Completer_nextMatch_fromInvalid_param(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    direction: NavDirection,
    expected_index: int,
) -> None:
    """Tests that setting the match from an invalid index selects a match.

    Selects first match if Next, and last match if Previous.
    """
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(
        completer, "currentIndex", MagicMock(return_value=QModelIndex())
    )
    monkeypatch.setattr(completer, "setCurrentIndex", MagicMock())
    assert not completer.currentIndex().isValid()

    mock_model = MagicMock()
    mock_model.rowCount.return_value = 5
    mock_model.index = MagicMock()
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))

    completer.nextMatch(direction)

    mock_model.index.assert_called_once_with(expected_index)
    cast(Mock, completer.setCurrentIndex).assert_called_once()


@pytest.mark.parametrize(
    ("start_index", "direction", "expected_index"),
    [
        pytest.param(4, NavDirection.Next, 0, id="next_wraps_on_last"),
        pytest.param(0, NavDirection.Previous, 4, id="prev_wraps_on_first"),
        pytest.param(1, NavDirection.Next, 2, id="next_index"),
        pytest.param(3, NavDirection.Previous, 2, id="prev_index"),
    ],
)
def test_Completer_nextMatch_fromValid_param(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    start_index: int,
    direction: NavDirection,
    expected_index: int,
) -> None:
    """Tests that setting the match from a valid index selects a match.

    Selects first match if on last index and Next.
    Selects last match if on first index and Previous.
    Selects next match if on any index other than last and Next.
    Selects prev match if on any index other than first and Previous.
    """
    _, completer = _createCompleter(qtbot)

    mock_current_index = MagicMock(
        spec=QModelIndex, isValid=Mock(return_value=True), row=lambda: start_index
    )

    monkeypatch.setattr(completer, "currentIndex", MagicMock())
    cast(Mock, completer.currentIndex).return_value = mock_current_index
    monkeypatch.setattr(completer, "setCurrentIndex", MagicMock())

    mock_model = MagicMock()
    mock_model.rowCount.return_value = 5
    mock_model.index = MagicMock()
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))

    completer.nextMatch(direction)

    mock_model.index.assert_called_once_with(expected_index)
    cast(Mock, completer.currentIndex).assert_called_once()


def _patchScrollToItemModels(
    completer: Completer,
    monkeypatch: pytest.MonkeyPatch,
    index_info: tuple[bool | None] | None = None,
) -> tuple[MagicMock, MagicMock]:
    """Creates a mock model for complete_model and model of a completer.

    The `index_return` indicates whether a mock index should be created,
    and what it's return value should be.
    If it is set to None, a mock_index is not created.

    Returns the model created and the index.
    """
    monkeypatch.setattr(completer, "setCurrentIndex", MagicMock())

    mock_model = MagicMock()

    if index_info is not None:
        mock_index = MagicMock(
            spec=QModelIndex,
            isValid=Mock(return_value=index_info[0]),
        )
        mock_model.indexForPrefix.return_value = mock_index
    else:
        mock_model.indexForPrefix = MagicMock()
        mock_index = MagicMock()

    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))

    return mock_model, mock_index


@pytest.mark.parametrize(
    ("index_info", "item_text", "expected_prefix_call", "expected_set_index_call"),
    [
        pytest.param(None, None, False, False, id="no_text"),
        pytest.param(
            (True,),
            "test",
            True,
            True,
            id="text_found",
        ),
        pytest.param(
            (False,),
            "test",
            True,
            False,
            id="text_not_found",
        ),
        pytest.param(
            (None,),
            "test",
            True,
            False,
            id="text_none_index",
        ),
    ],
)
def test_Completer_scrollToItem_param(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    index_info: tuple[bool | None] | None,
    item_text: str | None,
    expected_prefix_call: bool,
    expected_set_index_call: bool,
) -> None:
    """Test scrollToItem in different cases."""
    _, completer = _createCompleter(qtbot)
    mock_model, mock_index = _patchScrollToItemModels(
        completer, monkeypatch, index_info
    )

    completer.scrollToItem(item_text)

    if expected_prefix_call:
        mock_model.indexForPrefix.assert_called_once_with(item_text)
    else:
        mock_model.indexForPrefix.assert_not_called()

    if expected_set_index_call:
        cast(Mock, completer.setCurrentIndex).assert_called_once_with(mock_index)
    else:
        cast(Mock, completer.setCurrentIndex).assert_not_called()


def _patchPopup(completer: Completer, monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch the attributes and calls used in all popup methods."""
    monkeypatch.setattr(completer, "setGeometry", MagicMock())
    monkeypatch.setattr(completer, "show", MagicMock())


def test_Completer_popup_disabled(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test popup when it is disabled."""
    _, completer = _createCompleter(qtbot)

    completer.disable_popup = True

    monkeypatch.setattr(completer, "parent", MagicMock())
    _patchPopup(completer, monkeypatch)

    completer.popup()

    cast(Mock, completer.parent).assert_not_called()
    cast(Mock, completer.setGeometry).assert_not_called()
    cast(Mock, completer.show).assert_not_called()


def test_Completer_popup_no_parent(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test popup when there is no parent."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "parent", MagicMock(return_value=None))
    _patchPopup(completer, monkeypatch)

    completer.popup()

    cast(Mock, completer.setGeometry).assert_not_called()
    cast(Mock, completer.show).assert_not_called()


def test_Completer_popup_basic(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test popup basic behaviour."""
    _, completer = _createCompleter(qtbot)

    completer.disable_popup = False

    monkeypatch.setattr(completer, "isVisible", MagicMock(return_value=False))

    mock_model = MagicMock()
    mock_model.rowCount.return_value = 3
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))
    monkeypatch.setattr(completer, "setCurrentIndex", MagicMock())
    monkeypatch.setattr(
        completer, "currentIndex", MagicMock(return_value=QModelIndex())
    )

    _patchPopup(completer, monkeypatch)

    completer.popup()

    cast(Mock, completer.setGeometry).assert_called_once()
    cast(Mock, completer.show).assert_called_once()
    cast(Mock, completer.setCurrentIndex).assert_called_once()


def test_Completer_selectFirst_false(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test popup display without selecting the first item."""
    _, completer = _createCompleter(qtbot)

    completer.disable_popup = False
    monkeypatch.setattr(completer, "isVisible", MagicMock(return_value=False))
    mock_model = MagicMock()
    mock_model.rowCount.return_value = 3
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))
    monkeypatch.setattr(completer, "setCurrentIndex", MagicMock())
    monkeypatch.setattr(
        completer, "currentIndex", MagicMock(return_value=QModelIndex())
    )
    monkeypatch.setattr(completer, "setGeometry", MagicMock())
    monkeypatch.setattr(completer, "show", MagicMock())

    completer.popup(select_first=False)

    cast(Mock, completer.show).assert_called_once()
    cast(Mock, completer.setCurrentIndex).assert_not_called()


def test_Completer_popup_selectFirst_alreadyValidIndex(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test popup display when a valid index is already selected."""
    _, completer = _createCompleter(qtbot)

    completer.disable_popup = False
    completer.isVisible = Mock(return_value=False)
    mock_model = MagicMock()
    mock_model.rowCount.return_value = 3
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "model", MagicMock(return_value=mock_model))
    monkeypatch.setattr(completer, "setCurrentIndex", MagicMock())
    mock_index = MagicMock(spec=QModelIndex, isValid=Mock(return_value=True))
    monkeypatch.setattr(completer, "currentIndex", MagicMock(return_value=mock_index))
    monkeypatch.setattr(completer, "show", MagicMock())

    completer.popup(select_first=True)

    cast(Mock, completer.show).assert_called_once()
    cast(Mock, completer.setCurrentIndex).assert_not_called()


def test_Completer_popup_withHorizontalScrollbar(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test popup height calculation when a horizontal scrollbar is visible."""
    _, completer = _createCompleter(qtbot)

    completer.disable_popup = False
    completer.isVisible = Mock(return_value=False)
    mock_model = MagicMock()
    mock_model.rowCount.return_value = 3

    mock_scrollbar = Mock()
    mock_scrollbar.isVisible.return_value = True
    mock_scrollbar.sizeHint.return_value.height.return_value = 10
    monkeypatch.setattr(
        completer, "horizontalScrollBar", Mock(return_value=mock_scrollbar)
    )

    monkeypatch.setattr(completer, "setGeometry", MagicMock())

    completer.popup()

    cast(Mock, completer.setGeometry).assert_called_once()


def test_Completer_mouseMoveEvent_invalidIndex(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test mouseMoveEvent when the index at the mouse position is invalid."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "indexAt", Mock(return_value=QModelIndex()))
    mock_super_event = Mock()
    monkeypatch.setattr(QListView, "mouseMoveEvent", mock_super_event)
    monkeypatch.setattr(completer, "setCurrentIndex", MagicMock())

    event = QMouseEvent(
        QEvent.Type.MouseMove,
        QPoint(0, 0),
        QPoint(0, 0),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    completer.mouseMoveEvent(event)

    cast(Mock, completer.indexAt).assert_called_once()
    cast(Mock, completer.setCurrentIndex).assert_not_called()
    mock_super_event.assert_called_once_with(event)


def test_Completer_mouseMoveEvent_valid_same_index(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test mouseMoveEvent when mouse position index is valid and same as current."""
    _, completer = _createCompleter(qtbot)

    mock_index = Mock(spec=QModelIndex, isValid=Mock(return_value=True), row=lambda: 0)
    monkeypatch.setattr(completer, "indexAt", Mock(return_value=mock_index))
    monkeypatch.setattr(completer, "currentIndex", Mock(return_value=mock_index))
    mock_super_event = Mock()
    monkeypatch.setattr(QListView, "mouseMoveEvent", mock_super_event)
    monkeypatch.setattr(completer, "setCurrentIndex", MagicMock())

    event = QMouseEvent(
        QEvent.Type.MouseMove,
        QPoint(0, 0),
        QPoint(0, 0),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    completer.mouseMoveEvent(event)

    cast(Mock, completer.indexAt).assert_called_once()
    cast(Mock, completer.setCurrentIndex).assert_not_called()
    mock_super_event.assert_called_once_with(event)


def test_Completer_mouseMoveEvent_valid_different_index(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test mouseMoveEvent with valid mouse position index, different from current."""
    _, completer = _createCompleter(qtbot)

    mock_current_index = Mock(
        spec=QModelIndex, isValid=Mock(return_value=True), row=lambda: 0
    )
    mock_new_index = Mock(
        spec=QModelIndex, isValid=Mock(return_value=True), row=lambda: 1
    )
    monkeypatch.setattr(completer, "indexAt", Mock(return_value=mock_new_index))
    monkeypatch.setattr(
        completer, "currentIndex", Mock(return_value=mock_current_index)
    )
    mock_super_event = Mock()
    monkeypatch.setattr(QListView, "mouseMoveEvent", mock_super_event)
    monkeypatch.setattr(completer, "setCurrentIndex", MagicMock())

    event = QMouseEvent(
        QEvent.Type.MouseMove,
        QPoint(0, 0),
        QPoint(0, 0),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    completer.mouseMoveEvent(event)

    cast(Mock, completer.indexAt).assert_called_once()
    cast(Mock, completer.setCurrentIndex).assert_called_once_with(mock_new_index)
    mock_super_event.assert_called_once_with(event)


def test_Completer_processKeyPress_escape(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress for the Escape key."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "hide", MagicMock())

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_Escape, Qt.KeyboardModifier.NoModifier
    )
    widget = Mock(spec=QWidget)
    result = completer._processKeyPress(completer, event, widget)

    assert result is True
    cast(Mock, completer.hide).assert_called_once()
    assert event.isAccepted()


def test_Completer_processKeyPress_alt_f4(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress for Alt+F4."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "hide", MagicMock())

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_F4, Qt.KeyboardModifier.AltModifier
    )
    widget = Mock(spec=QWidget)
    result = completer._processKeyPress(completer, event, widget)

    assert result is True
    cast(Mock, completer.hide).assert_called_once()
    assert event.isAccepted()


def test_Completer_processKeyPress_enter_validIndex(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress for Enter key with a valid current index."""
    _, completer = _createCompleter(qtbot)

    mock_index = Mock(spec=QModelIndex, isValid=Mock(return_value=True))
    monkeypatch.setattr(completer, "currentIndex", Mock(return_value=mock_index))
    monkeypatch.setattr(completer, "chooseItem", Mock())
    monkeypatch.setattr(completer, "hide", MagicMock())

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_Enter, Qt.KeyboardModifier.NoModifier
    )
    widget = Mock(spec=QWidget)
    result = completer._processKeyPress(completer, event, widget)

    assert result is True
    cast(Mock, completer.chooseItem).assert_called_once_with(mock_index)
    cast(Mock, completer.hide).assert_called_once()
    assert event.isAccepted()


def test_Completer_processKeyPress_return_invalidIndex(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress for Return key with an invalid current index."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "currentIndex", Mock(return_value=QModelIndex()))
    monkeypatch.setattr(completer, "chooseItem", Mock())
    monkeypatch.setattr(completer, "hide", MagicMock())

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_Return, Qt.KeyboardModifier.NoModifier
    )
    widget = Mock(spec=QWidget)
    result = completer._processKeyPress(completer, event, widget)

    assert result is True
    cast(Mock, completer.chooseItem).assert_not_called()
    cast(Mock, completer.hide).assert_called_once()
    assert event.isAccepted()


def test_Completer_processKeyPress_tab_validIndex(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress for Tab key with a valid current index."""
    _, completer = _createCompleter(qtbot)

    mock_index = Mock(spec=QModelIndex, isValid=Mock(return_value=True))
    monkeypatch.setattr(completer, "currentIndex", Mock(return_value=mock_index))
    monkeypatch.setattr(completer, "chooseItem", Mock())
    monkeypatch.setattr(completer, "hide", MagicMock())
    monkeypatch.setattr(completer, "nextMatch", MagicMock())

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_Tab, Qt.KeyboardModifier.NoModifier
    )
    widget = Mock(spec=QWidget)
    with qtbot.assertNotEmitted(completer.apply_current_text):
        result = completer._processKeyPress(completer, event, widget)

    assert result is True
    cast(Mock, completer.chooseItem).assert_called_once_with(mock_index)
    cast(Mock, completer.hide).assert_called_once()
    cast(Mock, completer.nextMatch).assert_not_called()
    assert event.isAccepted()


def test_Completer_processKeyPress_tab_invalidIndex_acceptsUncompleted(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress for invalid index Tab with tab_accepts_uncompleted_text."""
    _, completer = _createCompleter(qtbot)

    completer.tab_accepts_uncompleted_text = True

    monkeypatch.setattr(completer, "currentIndex", Mock(return_value=QModelIndex()))
    monkeypatch.setattr(completer, "chooseItem", Mock())
    monkeypatch.setattr(completer, "hide", MagicMock())
    monkeypatch.setattr(completer, "nextMatch", MagicMock())

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_Tab, Qt.KeyboardModifier.NoModifier
    )
    widget = Mock(spec=QWidget)
    with qtbot.waitSignal(completer.apply_current_text, timeout=1000):
        result = completer._processKeyPress(completer, event, widget)

    assert result is True
    cast(Mock, completer.chooseItem).assert_not_called()
    cast(Mock, completer.hide).assert_called_once()
    cast(Mock, completer.nextMatch).assert_not_called()
    assert event.isAccepted()


def test_Completer_processKeyPress_tab_invalidIndex_noAccept_rowCount(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test processKeyPress for invalid index Tab when not tab_accepts_uncompleted_text.

    This test tests when items exist.
    """
    _, completer = _createCompleter(qtbot)

    completer.tab_accepts_uncompleted_text = False

    mock_model = MagicMock()
    mock_model.rowCount.return_value = 1
    monkeypatch.setattr(completer, "model", Mock(return_value=mock_model))
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "currentIndex", Mock(return_value=QModelIndex()))
    monkeypatch.setattr(completer, "chooseItem", Mock())
    monkeypatch.setattr(completer, "hide", MagicMock())
    monkeypatch.setattr(completer, "nextMatch", MagicMock())

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_Tab, Qt.KeyboardModifier.NoModifier
    )
    widget = Mock(spec=QWidget)
    with qtbot.assertNotEmitted(completer.apply_current_text):
        result = completer._processKeyPress(completer, event, widget)

    assert result is True
    cast(Mock, completer.chooseItem).assert_not_called()
    cast(Mock, completer.hide).assert_not_called()
    cast(Mock, completer.nextMatch).assert_called_once()
    assert event.isAccepted()


def test_Completer_processKeyPress_tab_invalidIndex_noAccept_noRowCount(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test processKeyPress for invalid index Tab when not tab_accepts_uncompleted_text.

    This test tests when no items exist.
    """
    _, completer = _createCompleter(qtbot)

    completer.tab_accepts_uncompleted_text = False

    mock_model = MagicMock()
    mock_model.rowCount.return_value = 0
    monkeypatch.setattr(completer, "model", Mock(return_value=mock_model))
    monkeypatch.setattr(completer, "complete_model", mock_model)
    monkeypatch.setattr(completer, "currentIndex", Mock(return_value=QModelIndex()))
    monkeypatch.setattr(completer, "chooseItem", Mock())
    monkeypatch.setattr(completer, "hide", MagicMock())
    monkeypatch.setattr(completer, "nextMatch", MagicMock())

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_Tab, Qt.KeyboardModifier.NoModifier
    )
    widget = Mock(spec=QWidget)
    with qtbot.assertNotEmitted(completer.apply_current_text):
        result = completer._processKeyPress(completer, event, widget)

    assert result is True
    cast(Mock, completer.chooseItem).assert_not_called()
    cast(Mock, completer.hide).assert_not_called()
    cast(Mock, completer.nextMatch).assert_not_called()
    assert event.isAccepted()


def test_Completer_processKeyPress_pageUp(qtbot: QtBot) -> None:
    """Test _processKeyPress for PageUp key."""
    _, completer = _createCompleter(qtbot)

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_PageUp, Qt.KeyboardModifier.NoModifier
    )
    widget = Mock(spec=QWidget)
    result = completer._processKeyPress(completer, event, widget)

    assert result is False
    assert event.isAccepted()


def test_Completer_processKeyPress_up(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress for Up key."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "nextMatch", MagicMock())

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_Up, Qt.KeyboardModifier.NoModifier
    )
    widget = Mock(spec=QWidget)
    result = completer._processKeyPress(completer, event, widget)

    assert result is True
    cast(Mock, completer.nextMatch).assert_called_once_with(
        direction=NavDirection.Previous
    )
    assert event.isAccepted()


def test_Completer_processKeyPress_down(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress for Down key."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "nextMatch", MagicMock())

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier
    )
    widget = Mock(spec=QWidget)
    result = completer._processKeyPress(completer, event, widget)

    assert result is True
    cast(Mock, completer.nextMatch).assert_called_once_with(direction=NavDirection.Next)
    assert event.isAccepted()


def test_Completer_processKeyPress_forwardToWidget_focusLost(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress when forwarding event to widget and focus is lost."""
    _, completer = _createCompleter(qtbot)

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_A, Qt.KeyboardModifier.NoModifier
    )
    mock_edit_with_complete = MagicMock()
    mock_edit_with_complete.eat_focus_out = True
    mock_edit_with_complete.keyPressEvent = Mock(side_effect=lambda ev: ev.accept())
    mock_edit_with_complete.hasFocus.return_value = False
    event.accept = Mock()
    monkeypatch.setattr(completer, "hide", MagicMock())

    result = completer._processKeyPress(completer, event, mock_edit_with_complete)
    assert result is True
    assert mock_edit_with_complete.eat_focus_out is True
    mock_edit_with_complete.keyPressEvent.assert_called_once_with(event)
    cast(Mock, completer.hide).assert_called_once()
    event.accept.assert_called_once()


def test_Completer_processKeyPress_forwardToWidget_focusKept(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress when forwarding event to widget and focus is retained."""
    _, completer = _createCompleter(qtbot)

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_A, Qt.KeyboardModifier.NoModifier
    )
    mock_edit_with_complete = MagicMock()
    mock_edit_with_complete.eat_focus_out = True
    mock_edit_with_complete.keyPressEvent = Mock(side_effect=lambda ev: ev.accept())
    mock_edit_with_complete.hasFocus.return_value = True
    event.accept = Mock()
    monkeypatch.setattr(completer, "hide", MagicMock())

    result = completer._processKeyPress(completer, event, mock_edit_with_complete)

    assert result is True
    assert mock_edit_with_complete.eat_focus_out is True
    mock_edit_with_complete.keyPressEvent.assert_called_once_with(event)
    cast(Mock, completer.hide).assert_not_called()
    event.accept.assert_called_once()


def test_Completer_processKeyPress_forwardToWidget_noEatFocusOut(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress doesn't forward events to widgets without eat_focus_out."""
    _, completer = _createCompleter(qtbot)

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_A, Qt.KeyboardModifier.NoModifier
    )
    mock_widget = Mock(spec=QWidget)
    mock_widget.keyPressEvent = Mock(side_effect=lambda ev: ev.accept())
    monkeypatch.setattr(completer, "hide", MagicMock())
    event.accept = Mock()

    result = completer._processKeyPress(completer, event, mock_widget)

    assert result is False
    mock_widget.keyPressEvent.assert_not_called()
    cast(Mock, completer.hide).assert_not_called()
    event.accept.assert_not_called()


def test_Completer_processKeyPress_attributeError_eventFilterCalled(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processKeyPress when an AttributeError occurs accessing event.key()."""
    _, completer = _createCompleter(qtbot)

    mock_event = MagicMock(spec=QEvent)
    type(mock_event).key = MagicMock(
        side_effect=AttributeError("No key")
    )  # Simulate AttributeError
    mock_widget = Mock(spec=QWidget)
    mock_qobject_event_filter = Mock(return_value=False)
    monkeypatch.setattr(QObject, "eventFilter", mock_qobject_event_filter)

    result = completer._processKeyPress(completer, mock_event, mock_widget)
    assert result is False
    # The original QObject.eventFilter is called with the original watched and event
    mock_qobject_event_filter.assert_called_once_with(completer, completer, mock_event)


def test_Completer_processMouseEvent_comboBox_dropdownArrow(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processMouseEvent when clicked widget is a QComboBox; dropdown arrow."""
    _, completer = _createCompleter(qtbot)

    mock_combo_box = MagicMock(spec=QComboBox)
    mock_style = MagicMock(spec=QStyle)
    mock_style.hitTestComplexControl.return_value = QStyle.SubControl.SC_ComboBoxArrow
    mock_combo_box.style.return_value = mock_style
    mock_combo_box.mapFromGlobal.return_value = QPoint(10, 10)
    mock_combo_box.initStyleOption = Mock()

    mock_timer_single_shot = Mock()
    monkeypatch.setattr(QTimer, "singleShot", mock_timer_single_shot)

    event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPoint(0, 0),
        QPoint(0, 0),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    event.accept = Mock()

    result = completer._processMouseEvent(event, mock_combo_box)

    assert result is True
    mock_combo_box.initStyleOption.assert_called_once()
    mock_combo_box.style.assert_called_once()
    mock_style.hitTestComplexControl.assert_called_once()
    mock_timer_single_shot.assert_called_once_with(0, completer.hide)
    event.accept.assert_called_once()


def test_Completer_processMouseEvent_comboBox_notDropdownArrow(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test processMouseEvent when clicked widget is QComboBox; not dropdown arrow."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "hide", MagicMock())

    mock_combo_box = MagicMock(spec=QComboBox)
    mock_style = MagicMock(spec=QStyle)
    mock_style.hitTestComplexControl.return_value = QStyle.SubControl.SC_ComboBoxFrame
    mock_combo_box.style.return_value = mock_style
    mock_combo_box.mapFromGlobal.return_value = QPoint(10, 10)
    mock_combo_box.initStyleOption = Mock()

    mock_timer_single_shot = Mock()
    monkeypatch.setattr(QTimer, "singleShot", mock_timer_single_shot)

    event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPoint(0, 0),
        QPoint(0, 0),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    event.accept = Mock()

    result = completer._processMouseEvent(event, mock_combo_box)

    assert result is True
    mock_timer_single_shot.assert_not_called()
    cast(Mock, completer.hide).assert_called_once()
    event.accept.assert_called_once()


def test_Completer_processMouseEvent_notComboBox(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test _processMouseEvent when the clicked widget is not a QComboBox."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "hide", MagicMock())
    mock_widget = Mock(spec=QWidget)

    mock_timer_single_shot = Mock()
    monkeypatch.setattr(QTimer, "singleShot", mock_timer_single_shot)

    event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPoint(0, 0),
        QPoint(0, 0),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    event.accept = Mock()

    result = completer._processMouseEvent(event, mock_widget)

    assert result is True
    mock_timer_single_shot.assert_not_called()
    cast(Mock, completer.hide).assert_called_once()
    event.accept.assert_called_once()


def test_Completer_eventFilter_watchedNotSelf(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test eventFilter when the watched object is not the completer itself."""
    _, completer = _createCompleter(qtbot)

    mock_watched = Mock(spec=QObject)
    event = QEvent(QEvent.Type.KeyPress)
    mock_qobject_event_filter = Mock(return_value=False)
    monkeypatch.setattr(QObject, "eventFilter", mock_qobject_event_filter)

    result = completer.eventFilter(mock_watched, event)
    assert result is False
    mock_qobject_event_filter.assert_called_once_with(completer, mock_watched, event)


def test_Completer_eventFilter_keyPress(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test eventFilter handling a KeyPress event for the completer."""
    _, completer = _createCompleter(qtbot)

    mock_processKeyPress = Mock(return_value=True)
    monkeypatch.setattr(completer, "_processKeyPress", mock_processKeyPress)

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_A, Qt.KeyboardModifier.NoModifier
    )
    parent_widget = completer.parent()

    result = completer.eventFilter(completer, event)
    assert result is True
    mock_processKeyPress.assert_called_once_with(completer, event, parent_widget)


def test_Completer_eventFilter_mouseButtonPress_outside(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test eventFilter handling MouseButtonPress outside completer's rectangle."""
    _, completer = _createCompleter(qtbot)

    completer.rect = Mock(return_value=Mock(contains=Mock(return_value=False)))
    completer.mapFromGlobal = Mock(return_value=QPoint(100, 100))

    mock_processMouseEvent = Mock(return_value=True)
    monkeypatch.setattr(completer, "_processMouseEvent", mock_processMouseEvent)

    event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPoint(0, 0),
        QPoint(0, 0),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    parent_widget = completer.parent()

    result = completer.eventFilter(completer, event)
    assert result is True
    mock_processMouseEvent.assert_called_once_with(event, parent_widget)


def test_Completer_eventFilter_mouseButtonPress_inside(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test eventFilter handling a MouseButtonPress inside completer's rectangle."""
    _, completer = _createCompleter(qtbot)

    completer.rect = Mock(return_value=Mock(contains=Mock(return_value=True)))
    completer.mapFromGlobal = Mock(return_value=QPoint(10, 10))

    mock_processMouseEvent = Mock(return_value=True)
    monkeypatch.setattr(completer, "_processMouseEvent", mock_processMouseEvent)

    event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPoint(0, 0),
        QPoint(0, 0),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )

    result = completer.eventFilter(completer, event)
    assert result is False
    mock_processMouseEvent.assert_not_called()


def test_Completer_eventFilter_inputMethod(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test eventFilter handling an InputMethod event."""
    _, completer = _createCompleter(qtbot)

    mock_qapplication_sendEvent = Mock()
    monkeypatch.setattr(QApplication, "sendEvent", mock_qapplication_sendEvent)

    event = QEvent(QEvent.Type.InputMethod)
    parent_widget = completer.parent()

    result = completer.eventFilter(completer, event)
    assert result is False
    mock_qapplication_sendEvent.assert_called_once_with(parent_widget, event)


def test_Completer_eventFilter_shortcutOverride(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test eventFilter handling a ShortcutOverride event."""
    _, completer = _createCompleter(qtbot)

    mock_qapplication_sendEvent = Mock()
    monkeypatch.setattr(QApplication, "sendEvent", mock_qapplication_sendEvent)

    event = QEvent(QEvent.Type.ShortcutOverride)
    parent_widget = completer.parent()

    result = completer.eventFilter(completer, event)
    assert result is False
    mock_qapplication_sendEvent.assert_called_once_with(parent_widget, event)


def test_Completer_eventFilter_noParentWidget(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test eventFilter when parent() returns None."""
    _, completer = _createCompleter(qtbot)

    monkeypatch.setattr(completer, "parent", Mock(return_value=None))
    event = QEvent(QEvent.Type.KeyPress)
    result = completer.eventFilter(completer, event)
    assert result is False


def _setupCompleterEnvironment(
    completer: Completer,
    monkeypatch: pytest.MonkeyPatch,
    *,
    widget_height: int,
    widget_width: int,
    map_to_global_pos_x: int,
    map_to_global_pos_y: int,
    screen_x: int,
    screen_width: int,
    screen_top: int,
    screen_bottom: int,
    size_hint_for_row: int = 20,
    model_row_count: int = 10,
    minimum_height: int = 50,
    horizontal_scrollbar_visible: bool = False,
    horizontal_scrollbar_height: int = 17,
) -> MagicMock:
    """Set up mocks for the Completer's environment to control geometry calculations."""
    mock_screen_geometry = MagicMock(spec=QRect)
    mock_screen_geometry.x.return_value = screen_x
    mock_screen_geometry.width.return_value = screen_width
    mock_screen_geometry.top.return_value = screen_top
    mock_screen_geometry.bottom.return_value = screen_bottom

    mock_screen = MagicMock(spec=QScreen)
    mock_screen.availableGeometry.return_value = mock_screen_geometry

    mock_widget = MagicMock(spec=QWidget)
    mock_widget.height.return_value = widget_height
    mock_widget.width.return_value = widget_width
    mock_widget.screen.return_value = mock_screen

    current_x = map_to_global_pos_x
    current_y = map_to_global_pos_y

    def get_x_mock() -> int:
        return current_x

    def set_x_mock(new_x: int) -> None:
        nonlocal current_x
        current_x = new_x

    def get_y_mock() -> int:
        return current_y

    def set_y_mock(new_y: int) -> None:
        nonlocal current_y
        current_y = new_y

    mock_pos = MagicMock(spec=QPoint)
    mock_pos.x.side_effect = get_x_mock
    mock_pos.y.side_effect = get_y_mock
    mock_pos.setX.side_effect = set_x_mock
    mock_pos.setY.side_effect = set_y_mock
    mock_widget.mapToGlobal.return_value = mock_pos

    monkeypatch.setattr(completer, "parent", lambda: mock_widget)
    monkeypatch.setattr(completer, "setCurrentIndex", MagicMock())
    monkeypatch.setattr(
        completer, "sizeHintForRow", MagicMock(return_value=size_hint_for_row)
    )
    monkeypatch.setattr(
        completer, "minimumHeight", MagicMock(return_value=minimum_height)
    )

    mock_horizontal_scollbar = None
    if horizontal_scrollbar_visible:
        mock_horizontal_scollbar_hint = MagicMock(spec=QSize)
        mock_horizontal_scollbar_hint.height.return_value = horizontal_scrollbar_height
        mock_horizontal_scollbar = MagicMock(spec=QScrollBar)
        mock_horizontal_scollbar.isVisible.return_value = True
        mock_horizontal_scollbar.sizeHint.return_value = mock_horizontal_scollbar_hint
    monkeypatch.setattr(
        completer,
        "horizontalScrollBar",
        MagicMock(return_value=mock_horizontal_scollbar),
    )

    mock_model = MagicMock(spec=CompleteModel)
    mock_model.rowCount.return_value = model_row_count
    mock_model.index.return_value = MagicMock(isValid=lambda: True)
    monkeypatch.setattr(completer, "model", lambda: mock_model)
    monkeypatch.setattr(completer, "complete_model", mock_model)

    mock_current_index = MagicMock(isValid=lambda: False)
    monkeypatch.setattr(
        completer, "currentIndex", MagicMock(return_value=mock_current_index)
    )

    monkeypatch.setattr(completer, "isVisible", MagicMock(return_value=False))

    return mock_pos


def test_Completer_popup_setGeometry_normal(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test the geometry is set correctly when not near an edge."""
    _, completer = _createCompleter(qtbot)

    _setupCompleterEnvironment(
        completer,
        monkeypatch,
        widget_height=30,
        widget_width=150,
        map_to_global_pos_x=100,
        map_to_global_pos_y=200,
        screen_x=0,
        screen_width=1920,
        screen_top=0,
        screen_bottom=1080,
    )

    monkeypatch.setattr(completer, "setGeometry", MagicMock())
    monkeypatch.setattr(completer, "show", MagicMock())

    completer.popup()

    # Expected: x=100, y=200, width=150, height=(20*min(7,10)+3)+3 = 146
    cast(Mock, completer.setGeometry).assert_called_once_with(100, 200, 150, 146)
    cast(Mock, completer.show).assert_called_once()


def test_Completer_popup_setGeometry_right_edge(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test geometry when the popup extends beyond the right edge of the screen."""
    _, completer = _createCompleter(qtbot)

    _setupCompleterEnvironment(
        completer,
        monkeypatch,
        widget_height=30,
        widget_width=150,
        map_to_global_pos_x=700,  # pos.x()
        map_to_global_pos_y=200,
        screen_x=0,
        screen_width=800,  # screen_x + screen_width = 800
        screen_top=0,
        screen_bottom=1080,
    )

    monkeypatch.setattr(completer, "setGeometry", MagicMock())
    monkeypatch.setattr(completer, "show", MagicMock())

    completer.popup()

    # Initial: pos.x()=700, width=150. pos.x() + width = 850. screen_width = 800.
    # 850 > 800 is True.
    # New x = screen.x() + screen.width() - width = 0 + 800 - 150 = 650
    # Expected: x=650, y=200, width=150, height=146
    cast(Mock, completer.setGeometry).assert_called_once_with(650, 200, 150, 146)
    cast(Mock, completer.show).assert_called_once()


def test_Completer_popup_setGeometry_left_edge(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test geometry when the popup starts to the left of the screen."""
    _, completer = _createCompleter(qtbot)

    _setupCompleterEnvironment(
        completer,
        monkeypatch,
        widget_height=30,
        widget_width=150,
        map_to_global_pos_x=50,  # pos.x()
        map_to_global_pos_y=200,
        screen_x=100,  # screen.x()
        screen_width=800,
        screen_top=0,
        screen_bottom=1080,
    )

    monkeypatch.setattr(completer, "setGeometry", MagicMock())
    monkeypatch.setattr(completer, "show", MagicMock())

    completer.popup()

    # Initial: pos.x()=50. screen.x()=100.
    # 50 < 100 is True.
    # New x = screen.x() = 100
    # Expected: x=100, y=200, width=150, height=146
    cast(Mock, completer.setGeometry).assert_called_once_with(100, 200, 150, 146)
    cast(Mock, completer.show).assert_called_once()


def test_Completer_popup_setGeometry_height_constrained_below(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test geometry when height > bottom but top <= bottom."""
    _, completer = _createCompleter(qtbot)

    _setupCompleterEnvironment(
        completer,
        monkeypatch,
        widget_height=1000,  # real_height = 1000
        widget_width=150,
        map_to_global_pos_x=100,
        map_to_global_pos_y=1030,  # pos.y()
        screen_x=0,
        screen_width=1920,
        screen_top=0,
        screen_bottom=1080,  # screen.bottom()
    )

    monkeypatch.setattr(completer, "setGeometry", MagicMock())
    monkeypatch.setattr(completer, "show", MagicMock())

    completer.popup()

    # Calculated height = 146
    # bottom = screen.bottom() - pos.y() = 1080 - 1030 = 50
    # top = pos.y() - real_height - screen.top() + 2 = 1030 - 1000 - 0 + 2 = 32
    # Condition: height (146) > bottom (50) is True.
    # height = min(max(top, bottom), height) = min(max(32, 50), 146) = min(50, 146) = 50
    # Condition: top (32) > bottom (50) is False. No change to pos.y().
    # Expected: x=100, y=1030, width=150, height=50
    cast(Mock, completer.setGeometry).assert_called_once_with(100, 1030, 150, 50)
    cast(Mock, completer.show).assert_called_once()


def test_Completer_popup_setGeometry_height_constrained_above(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test geometry when height > bottom and top > bottom."""
    _, completer = _createCompleter(qtbot)
    mock_pos = _setupCompleterEnvironment(
        completer,
        monkeypatch,
        widget_height=30,  # real_height = 30
        widget_width=150,
        map_to_global_pos_x=100,
        map_to_global_pos_y=1030,  # pos.y()
        screen_x=0,
        screen_width=1920,
        screen_top=0,
        screen_bottom=1080,  # screen.bottom()
    )

    monkeypatch.setattr(completer, "setGeometry", MagicMock())
    monkeypatch.setattr(completer, "show", MagicMock())

    completer.popup()

    # Calculated height = 146
    # bottom = screen.bottom() - pos.y() = 1080 - 1030 = 50
    # top = pos.y() - real_height - screen.top() + 2 = 1030 - 30 - 0 + 2 = 1002
    # Condition: height (146) > bottom (50) is True.
    # height = min(max(top, bottom), height) = min(max(1002, 50), 146)
    #        = min(1002, 146) = 146
    # Condition: top (1002) > bottom (50) is True.
    # pos.setY(pos.y() - height - real_height + 2) = 1030 - 146 - 30 + 2 = 856
    # Expected: x=100, y=856, width=150, height=146
    cast(Mock, completer.setGeometry).assert_called_once_with(100, 856, 150, 146)
    cast(Mock, completer.show).assert_called_once()
    assert mock_pos.y() == 856
