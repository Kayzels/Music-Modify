from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from music_modify.gui.edit.bulk.dialog_edit_bulk import EditBulkDialog
from music_modify.gui.edit.dialog_edit import EditDialog
from music_modify.gui.edit.dialog_edit_factory import EditDialogFactory
from music_modify.models.song_repository import SongRepository


def test_EditDialogFactory_get_rows_empty(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    repo = SongRepository()
    factory = EditDialogFactory(widget, repo)

    single_dialog = factory.get([])
    qtbot.addWidget(single_dialog)
    assert isinstance(single_dialog, EditDialog)

    bulk_dialog = factory.get([], bulk=True)
    qtbot.addWidget(bulk_dialog)
    assert isinstance(bulk_dialog, EditBulkDialog)


def test_EditDialogFactory_get_rows_invalid(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    repo = SongRepository()
    factory = EditDialogFactory(widget, repo)

    single_dialog = factory.get([1])
    qtbot.addWidget(single_dialog)
    assert isinstance(single_dialog, EditDialog)

    bulk_dialog = factory.get([1], bulk=True)
    qtbot.addWidget(bulk_dialog)
    assert isinstance(bulk_dialog, EditBulkDialog)


def test_EditDialogFactory_get_rows_valid_single(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    repo = SongRepository()
    factory = EditDialogFactory(widget, repo)

    for _ in range(3):
        repo.addSong()

    single_dialog = factory.get([0])
    qtbot.addWidget(single_dialog)
    assert isinstance(single_dialog, EditDialog)

    bulk_dialog = factory.get([0], bulk=True)
    qtbot.addWidget(bulk_dialog)
    assert isinstance(bulk_dialog, EditBulkDialog)


def test_EditDialogFactory_get_rows_valid_multiple(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    repo = SongRepository()
    factory = EditDialogFactory(widget, repo)

    for _ in range(3):
        repo.addSong()

    single_dialog = factory.get([0, 1])
    qtbot.addWidget(single_dialog)
    assert isinstance(single_dialog, EditDialog)

    bulk_dialog = factory.get([0, 1], bulk=True)
    qtbot.addWidget(bulk_dialog)
    assert isinstance(bulk_dialog, EditBulkDialog)
