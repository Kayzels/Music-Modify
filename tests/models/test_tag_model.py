import pytest
from PySide6.QtCore import Qt

from music_modify.custom_types import TagInfo
from music_modify.models.tag_model import TagModel, TAG_MODEL_COLUMNS
from music_modify.utils.string_utils import tableHeader


@pytest.fixture
def tags() -> list[TagInfo]:
    return [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
    ]


@pytest.fixture
def model(tags: list[TagInfo]) -> TagModel:
    return TagModel(tags)


def test_size(model: TagModel, tags: list[TagInfo]):
    assert model.rowCount() == len(tags)
    assert model.columnCount() == len(TAG_MODEL_COLUMNS)
    assert model.tags == tags


def test_headers(model: TagModel):
    for col in range(len(TAG_MODEL_COLUMNS)):
        check_val = tableHeader(TAG_MODEL_COLUMNS[col])
        assert (
            model.headerData(
                col, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            == check_val
        )
    assert (
        model.headerData(0, Qt.Orientation.Vertical, Qt.ItemDataRole.DisplayRole)
        is None
    )
    assert (
        model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.EditRole) is None
    )


def test_data(model: TagModel, tags: list[TagInfo]):
    # Should be title, but the index for column might change.
    # Depends on TAG_MODEL_COLUMNS

    for i in range(len(TAG_MODEL_COLUMNS)):
        # Only need to test one row, no need to iterate through tags
        index = model.index(0, i)
        field = TAG_MODEL_COLUMNS[i]
        role = (
            Qt.ItemDataRole.DisplayRole
            if field != "show_in_table"
            else Qt.ItemDataRole.CheckStateRole
        )
        assert model.data(index, role) == (
            getattr(tags[0], field)
            if field != "show_in_table"
            else Qt.CheckState.Checked
        )
    index = model.index(len(tags), 0)
    assert model.data(index, Qt.ItemDataRole.DisplayRole) is None


def test_setData(model: TagModel):
    # Check setting strings first
    cols = [i for i, column in enumerate(TAG_MODEL_COLUMNS) if column == "id3_key"]
    if len(cols) != 1:
        # Failed to find the right column, so something is wrong
        assert False
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
        assert False
    check_index = model.index(0, cols[0])
    check_val: int = Qt.CheckState.Unchecked.value
    assert model.setData(check_index, check_val, Qt.ItemDataRole.CheckStateRole)
    assert model.tags == [
        TagInfo(id3_key="TRCK", display_name="Title", show_in_table=False),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
    ]


def test_addTag(model: TagModel):
    model.addTag(id3_key="TRCK", display_name="Track", show_in_table=True)
    assert model.tags == [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
        TagInfo(id3_key="TRCK", display_name="Track", show_in_table=True),
    ]


def test_removeTag(model: TagModel):
    model.removeTag(1)
    assert model.tags == [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
    ]


def test_moveTag(model: TagModel):
    model.moveTag(0, 1)
    assert model.tags == [
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
    ]
