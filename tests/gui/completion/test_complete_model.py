"""Tests for CompleteModel."""

from PySide6.QtCore import Qt

from music_modify.gui.completion._complete_model import CompleteModel


def test_CompleteModel_init() -> None:
    """Tests that a CompleteModel sets values correctly on initialization."""
    model = CompleteModel()
    assert model.strip_completion_entries is True
    assert len(model.all_items) == 0
    assert len(model.current_items) == 0
    assert len(model.current_prefix) == 0


def test_CompleteModel_setItems() -> None:
    """Tests that CompleteModel adds items to the model correctly.

    If `strip_completion_entries` is set to False, the items should be added
    with their preceding and following whitespace kept.
    """
    model = CompleteModel()
    model2 = CompleteModel(strip_completion_entries=False)

    items: tuple[str, ...] = (
        "Word with no spaces",
        "Word with spaces at end        ",
        "   Word with spaces at start",
        "    Word with spaces at start and end    ",
    )

    model.setItems(items)
    assert model.all_items == (
        "Word with no spaces",
        "Word with spaces at end",
        "Word with spaces at start",
        "Word with spaces at start and end",
    )
    assert model.current_items == (
        "Word with no spaces",
        "Word with spaces at end",
        "Word with spaces at start",
        "Word with spaces at start and end",
    )
    assert model.current_prefix == ""

    model2.setItems(items)
    assert model2.all_items == (
        "    Word with spaces at start and end    ",
        "   Word with spaces at start",
        "Word with no spaces",
        "Word with spaces at end        ",
    )
    assert model2.current_items == (
        "    Word with spaces at start and end    ",
        "   Word with spaces at start",
        "Word with no spaces",
        "Word with spaces at end        ",
    )
    assert model2.current_prefix == ""


def test_CompleteModel_setItems_unsorted_sorts() -> None:
    """Tests that adding unsorted items sorts them internally."""
    model = CompleteModel()

    items: tuple[str, ...] = ("Zebra", "Zany", "Ancient", "Anticipate")

    model.setItems(items)
    assert model.all_items == ("Ancient", "Anticipate", "Zany", "Zebra")
    assert model.current_items == ("Ancient", "Anticipate", "Zany", "Zebra")
    assert model.current_prefix == ""


def test_CompleteModel_rowCount() -> None:
    """Tests that adding items updates the rowCount correctly."""
    model = CompleteModel()
    model2 = CompleteModel(strip_completion_entries=False)

    items: tuple[str, ...] = ("Word with no spaces", "Word with spaces        ")

    model.setItems(items)
    assert model.rowCount() == len(items)

    model2.setItems(items)
    assert model2.rowCount() == len(items)


def test_CompleteModel_setCompletionPrefix_new() -> None:
    """Tests that setting a new completion prefix updates current items."""
    model = CompleteModel()
    items: tuple[str, ...] = ("Begins", "End", "Inside")
    model.setItems(items)

    assert model.current_items == items
    assert model.all_items == items
    assert model.current_prefix == ""

    model.setCompletionPrefix("B")

    assert model.current_items == ("Begins",)
    assert model.all_items == ("Begins", "End", "Inside")
    assert model.current_prefix == "B"


def test_CompleteModel_setCompletionPrefix_cleared() -> None:
    """Tests that clearing a completion prefix resets current items to all items."""
    model = CompleteModel()
    items: tuple[str, ...] = ("Begins", "End", "Inside")
    model.setItems(items)

    assert model.current_items == items
    assert model.all_items == items
    assert model.current_prefix == ""

    model.setCompletionPrefix("B")

    assert model.current_items == ("Begins",)
    assert model.all_items == items
    assert model.current_prefix == "B"

    model.setCompletionPrefix("")
    assert model.current_items == items
    assert model.all_items == items
    assert model.current_prefix == ""


def test_CompleteModel_setCompletionPrefix_same_no_change() -> None:
    """Tests that setting the same prefix doesn't change current_items."""
    model = CompleteModel()
    items: tuple[str, ...] = ("Begins", "End", "Inside")
    model.setItems(items)

    assert model.current_items == items
    assert model.all_items == items
    assert model.current_prefix == ""

    model.setCompletionPrefix("B")

    assert model.current_items == ("Begins",)
    assert model.all_items == items
    assert model.current_prefix == "B"

    model.setCompletionPrefix("B")
    assert model.current_items == ("Begins",)
    assert model.all_items == items
    assert model.current_prefix == "B"


def test_CompleteModel_setCompletionPrefix_subset() -> None:
    """Tests that setting the prefix to a subset further filters current_items."""
    model = CompleteModel()
    items: tuple[str, ...] = ("All", "And", "Any", "Bool")
    model.setItems(items)

    assert model.current_items == items
    assert model.all_items == items
    assert model.current_prefix == ""

    model.setCompletionPrefix("A")

    assert model.current_items == ("All", "And", "Any")
    assert model.all_items == items
    assert model.current_prefix == "A"

    model.setCompletionPrefix("An")
    assert model.current_items == ("And", "Any")
    assert model.all_items == items
    assert model.current_prefix == "An"


def test_CompleteModel_indexForPrefix() -> None:
    """Tests that the index for the value containing a prefix is returned correctly."""
    model = CompleteModel()
    items: tuple[str, ...] = ("All", "And", "Any", "Bool")
    model.setItems(items)

    assert model.indexForPrefix("C") is None
    assert model.indexForPrefix("A") == model.index(0)
    assert model.indexForPrefix("An") == model.index(1)
    assert model.indexForPrefix("B") == model.index(3)
    assert model.indexForPrefix("") == model.index(0)

    model.setCompletionPrefix("An")
    assert model.indexForPrefix("Ant") is None
    assert model.indexForPrefix("B") is None


def test_CompleteModel_data() -> None:
    """Tests that data is returned correctly.

    If the index is invalid, or it is not a role being used, should be None.
    If it is a display role, spaces should be displayed with `␣`,
    otherwise they should be passed directly.
    """
    model = CompleteModel()
    model2 = CompleteModel(strip_completion_entries=False)

    items: tuple[str, ...] = ("    First", "Final", "Fix", "Fair    ")

    model.setItems(items)
    assert model.current_items == ("Fair", "Final", "First", "Fix")
    assert model.all_items == ("Fair", "Final", "First", "Fix")
    model2.setItems(items)
    assert model2.current_items == ("    First", "Fair    ", "Final", "Fix")
    assert model2.all_items == ("    First", "Fair    ", "Final", "Fix")

    assert model.data(model.index(-1)) is None
    assert model2.data(model.index(-1)) is None

    assert model.data(model.index(0), Qt.ItemDataRole.DisplayRole) == "Fair"
    assert model2.data(model.index(0), Qt.ItemDataRole.DisplayRole) == "␣␣␣␣First"
    assert model2.data(model.index(0), Qt.ItemDataRole.UserRole) == "    First"
    assert model2.data(model.index(1), Qt.ItemDataRole.DisplayRole) == "Fair␣␣␣␣"
    assert model2.data(model.index(1), Qt.ItemDataRole.UserRole) == "Fair    "

    assert model.data(model.index(0), Qt.ItemDataRole.EditRole) is None
