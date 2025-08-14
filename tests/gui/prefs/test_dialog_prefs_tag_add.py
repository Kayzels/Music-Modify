from PySide6.QtWidgets import QMessageBox
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types import TagInfo
from music_modify.gui.prefs.dialog_prefs_tag_add import PrefsTagAddDialog
from music_modify.models.tag_model import TagModel


@pytest.fixture
def tags() -> list[TagInfo]:
    return [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
    ]


@pytest.fixture
def model(tags: list[TagInfo]) -> TagModel:
    return TagModel(tags)


def createDialog(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> PrefsTagAddDialog:
    dialog = PrefsTagAddDialog()
    qtbot.addWidget(dialog)

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args, **kwargs: QMessageBox.StandardButton.Ok,
    )

    return dialog


def test_PrefsTagAddDialog_init(qtbot: QtBot) -> None:
    dialog = PrefsTagAddDialog()
    qtbot.addWidget(dialog)

    assert dialog.id3_line_edit.text() == ""
    assert dialog.display_name_line_edit.text() == ""
    assert not dialog.show_checkbox.isChecked()


def test_addToModel_missing_text(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    model: TagModel,
) -> None:
    dialog = createDialog(qtbot, monkeypatch)

    before_len = model.rowCount()
    dialog.addToModel(model)
    assert model.rowCount() == before_len


def test_addToModel_already_id3(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    model: TagModel,
) -> None:
    dialog = createDialog(qtbot, monkeypatch)

    dialog.id3_line_edit.setText("TIT2")
    dialog.display_name_line_edit.setText("Other Title")

    before_len = model.rowCount()
    dialog.addToModel(model)
    assert model.rowCount() == before_len


def test_addToModel_already_display(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    model: TagModel,
) -> None:
    dialog = createDialog(qtbot, monkeypatch)
    dialog.id3_line_edit.setText("TIT1")
    dialog.display_name_line_edit.setText("Title")

    before_len = model.rowCount()
    dialog.addToModel(model)
    assert model.rowCount() == before_len


def test_addToModel_new(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    model: TagModel,
) -> None:
    dialog = createDialog(qtbot, monkeypatch)
    dialog.id3_line_edit.setText("TRCK")
    dialog.display_name_line_edit.setText("Track")

    before_len = model.rowCount()
    dialog.addToModel(model)
    assert model.rowCount() == before_len + 1
    assert model.tags == [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
        TagInfo(id3_key="TRCK", display_name="Track", show_in_table=False),
    ]
