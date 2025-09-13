"""Tests for EditDialogFactory."""

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.songtag import SongTag
from music_modify.gui.edit.bulk.dialog_edit_bulk import EditBulkDialog
from music_modify.gui.edit.dialog_edit import EditDialog
from music_modify.gui.edit.dialog_edit_factory import EditDialogFactory
from music_modify.models.song_repository import SongRepository


@pytest.mark.parametrize(
    "bulk", [pytest.param(False, id="not_bulk"), pytest.param(True, id="bulk")]
)
def test_EditDialogFactory_get(
    qtbot: QtBot, bulk: bool, table_tags: list[SongTag]
) -> None:
    """Test that the correct dialog type is returned, based on bulk."""
    widget = QWidget()
    qtbot.addWidget(widget)
    repo = SongRepository(table_tags, table_tags, ", ")
    factory = EditDialogFactory(widget, repo)

    dialog = factory.get([], table_tags, ", ", bulk=bulk)
    expected_type = EditBulkDialog if bulk else EditDialog
    qtbot.addWidget(dialog)
    assert isinstance(dialog, expected_type)
