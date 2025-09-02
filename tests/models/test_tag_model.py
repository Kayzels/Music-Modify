"""Tests for TagModel."""

from typing import Literal

from PySide6.QtCore import Qt
import pytest

from music_modify.custom_types import TagInfo
from music_modify.custom_types.enums import EditorType
from music_modify.models.tag_model import TAG_MODEL_COLUMNS, TagModel
from music_modify.utils.string_utils import tableHeader


@pytest.fixture
def tags() -> list[TagInfo]:
    """Fixture that creates a list of TagInfo."""
    return [
        TagInfo(
            id3_key="TIT2",
            display_name="Title",
            show_in_table=True,
            editor_type=EditorType.Automatic,
        ),
        TagInfo(
            id3_key="TPE2",
            display_name="Artist",
            show_in_table=False,
            editor_type=EditorType.Automatic,
        ),
    ]


@pytest.fixture
def model(tags: list[TagInfo]) -> TagModel:
    """Fixture that creates a tag model."""
    return TagModel(tags)


def test_TagModel_rowCount_columnCount(model: TagModel, tags: list[TagInfo]) -> None:
    """Test that the number of rows and columns for a TagModel is correct."""
    assert model.rowCount() == len(tags)
    assert model.columnCount() == len(TAG_MODEL_COLUMNS)
    assert model.tags == tags


def test_TagModel_headerData(model: TagModel) -> None:
    """Test that the vertical and horizontal header values are correct.

    Horizontal headers should have the TagInfo labels.
    Vertical headers should return None.
    Headers for invalid indexes and roles should return None.
    """
    for col in range(len(TAG_MODEL_COLUMNS)):
        check_val: str = tableHeader(TAG_MODEL_COLUMNS[col])
        assert (
            model.headerData(
                section=col,
                orientation=Qt.Orientation.Horizontal,
                role=Qt.ItemDataRole.DisplayRole,
            )
            == check_val
        )
    assert (
        model.headerData(
            section=0,
            orientation=Qt.Orientation.Vertical,
            role=Qt.ItemDataRole.DisplayRole,
        )
        is None
    )
    assert (
        model.headerData(
            section=0,
            orientation=Qt.Orientation.Horizontal,
            role=Qt.ItemDataRole.EditRole,
        )
        is None
    )
    assert (
        model.headerData(
            section=-1,
            orientation=Qt.Orientation.Horizontal,
            role=Qt.ItemDataRole.DisplayRole,
        )
        is None
    )
    assert (
        model.headerData(
            section=len(TAG_MODEL_COLUMNS),
            orientation=Qt.Orientation.Horizontal,
            role=Qt.ItemDataRole.DisplayRole,
        )
        is None
    )


def test_TagModel_data(model: TagModel, tags: list[TagInfo]) -> None:
    """Test that the data values for tags are found and displayed correctly."""
    # Only need to test one row, no need to iterate through tags
    for i in range(len(TAG_MODEL_COLUMNS)):
        index = model.index(0, i)
        field = TAG_MODEL_COLUMNS[i]
        role: Literal[Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.CheckStateRole] = (
            Qt.ItemDataRole.DisplayRole
            if field != "show_in_table"
            else Qt.ItemDataRole.CheckStateRole
        )
        actual_data = model.data(index, role)
        if field == "show_in_table":
            assert actual_data == Qt.CheckState.Checked
        elif field == "editor_type":
            assert actual_data == getattr(tags[0], field).value
        else:
            assert actual_data == getattr(tags[0], field)

        edit_role = Qt.ItemDataRole.EditRole
        if field != "show_in_table":
            actual_edit_data = model.data(index, edit_role)
            if field == "editor_type":
                assert actual_edit_data == EditorType.Automatic
            else:
                assert actual_edit_data == getattr(tags[0], field)

    invalid_index = model.index(len(tags), 0)
    assert model.data(invalid_index, Qt.ItemDataRole.DisplayRole) is None


def test_TagModel_setData(model: TagModel) -> None:
    """Test that data can be added to the TagModel."""
    # Check setting strings first
    cols = [i for i, column in enumerate(TAG_MODEL_COLUMNS) if column == "id3_key"]
    if len(cols) != 1:
        # Failed to find the right column, so something is wrong
        pytest.fail("Zero or more than one columns found.")
    id3_index = model.index(0, cols[0])
    id3_val = "TRCK"
    assert model.setData(id3_index, id3_val, Qt.ItemDataRole.EditRole)
    assert model.tags == [
        TagInfo(id3_key="TRCK", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
    ]

    # Check setting check val
    cols = [
        i for i, column in enumerate(TAG_MODEL_COLUMNS) if column == "show_in_table"
    ]
    if len(cols) != 1:
        pytest.fail("Zero or more than one columns found.")
    check_index = model.index(0, cols[0])
    check_val: int = Qt.CheckState.Unchecked.value
    assert model.setData(check_index, check_val, Qt.ItemDataRole.CheckStateRole)
    assert model.tags == [
        TagInfo(id3_key="TRCK", display_name="Title", show_in_table=False),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
    ]

    # Check setting editor_type
    cols = [i for i, column in enumerate(TAG_MODEL_COLUMNS) if column == "editor_type"]
    if len(cols) != 1:
        pytest.fail("Zero or more than one columns found.")
    editor_index = model.index(0, cols[0])
    editor_val = EditorType.MultipleText.value
    assert model.setData(editor_index, editor_val, Qt.ItemDataRole.EditRole)
    assert model.tags[0] == TagInfo(
        id3_key="TRCK",
        display_name="Title",
        show_in_table=False,
        editor_type=EditorType.MultipleText,
    )
    invalid_val = "Invalid text"
    assert model.setData(editor_index, invalid_val, Qt.ItemDataRole.EditRole) is False
    assert model.tags[0] == TagInfo(
        id3_key="TRCK",
        display_name="Title",
        show_in_table=False,
        editor_type=EditorType.MultipleText,
    )

    # Invalid index
    assert model.setData(model.index(-1, -1), 1) is False

    # Empty input
    assert model.setData(model.index(0, 0), "", Qt.ItemDataRole.EditRole) is False

    # Value already exists
    assert model.setData(model.index(0, 0), "TPE2", Qt.ItemDataRole.EditRole) is False
    assert model.setData(model.index(0, 0), "TRCK", Qt.ItemDataRole.EditRole)

    # Invalid role
    assert (
        model.setData(model.index(0, 0), "TRCK", Qt.ItemDataRole.DisplayRole) is False
    )


def test_TagModel_addTag(model: TagModel) -> None:
    """Test creating a new tag for the model."""
    model.addTag(id3_key="TRCK", display_name="Track", show_in_table=True)
    assert model.tags == [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
        TagInfo(id3_key="TRCK", display_name="Track", show_in_table=True),
    ]


def test_TagModel_removeTag(model: TagModel) -> None:
    """Test removing a tag from the model."""
    model.removeTag(1)
    assert model.tags == [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
    ]


def test_moveTag(model: TagModel) -> None:
    """Test moving tags up and down in the model."""
    model.moveTag(0, 1)
    tags = [
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
    ]

    # Invalid source row
    model.moveTag(-1, 0)
    assert model.tags == tags
    # Invalid destination row
    model.moveTag(0, -1)
    assert model.tags == tags
    # Invalid source and destination row
    model.moveTag(-1, model.rowCount())
    assert model.tags == tags
    # Invalid source row
    model.moveTag(model.rowCount(), 0)
    assert model.tags == tags

    model.moveTag(0, 1)
    assert model.tags == [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
    ]


def test_TagModel_flags(model: TagModel) -> None:
    """Test that flags are set correctly based on index."""
    # Invalid index
    assert model.flags(model.index(-1, -1)) == Qt.ItemFlag.NoItemFlags

    for col_idx, field in enumerate(TAG_MODEL_COLUMNS):
        index = model.index(0, col_idx)
        current_flags = model.flags(index)

        if field == "show_in_table":
            assert current_flags & Qt.ItemFlag.ItemIsUserCheckable
            assert current_flags & Qt.ItemFlag.ItemIsEnabled
            assert not (current_flags & Qt.ItemFlag.ItemIsEditable)
        else:
            assert current_flags & Qt.ItemFlag.ItemIsEditable
            assert current_flags & Qt.ItemFlag.ItemIsEnabled
            assert not (current_flags & Qt.ItemFlag.ItemIsUserCheckable)
