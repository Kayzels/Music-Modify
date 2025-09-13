"""Tests for PrefsDialog."""

# pyright: reportUnusedParameter = false

from typing import TYPE_CHECKING, cast, override
from unittest.mock import MagicMock

from PySide6.QtWidgets import QVBoxLayout, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.prefs.dialog_prefs import PrefsDialog
from music_modify.gui.prefs.dialog_prefs_abstract import PrefsAbstractDialog
from music_modify.gui.prefs.dialog_prefs_split import PrefsSplitDialog
from music_modify.gui.prefs.dialog_prefs_tag import PrefsTagDialog
from music_modify.prefs import Settings

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any


class _MockAbstractChildDialog(PrefsAbstractDialog):
    """A mock dialog for testing the generic behaviour of openChildDialog."""

    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        super().__init__(settings, parent)
        self.setModal: Callable[[bool, Any], None] = MagicMock()
        self.show: Callable[..., None] = MagicMock()

    @override
    def setupUi(self) -> None:
        self.setLayout(QVBoxLayout())

    @override
    def updateSettings(self) -> None:
        pass

    @override
    def restoreDefaults(self) -> None:
        pass

    @override
    def resetSettings(self) -> None:
        pass


def test_PrefsDialog_openChildDialog(
    qtbot: QtBot, app_info: tuple[str, str, str]
) -> None:
    """Test that a child dialog is created."""
    settings = Settings()
    settings.configureForApplication()

    child_dialog = _MockAbstractChildDialog(settings)
    qtbot.addWidget(child_dialog)
    child_dialog_class: type[PrefsAbstractDialog] = cast(
        type[PrefsAbstractDialog],
        MagicMock(return_value=child_dialog),
    )

    parent_dialog = PrefsDialog(settings)
    qtbot.addWidget(parent_dialog)

    parent_dialog.openChildDialog(child_dialog_class)

    cast(MagicMock, child_dialog_class).assert_called_once_with(settings, parent_dialog)
    cast(MagicMock, child_dialog.setModal).assert_called_once_with(True)
    cast(MagicMock, child_dialog.show).assert_called_once()


def test_PrefsDialog_buttonEditTags_opensTagDialog(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, app_info: tuple[str, str, str]
) -> None:
    """Test that clicking Edit Tags button opens a PrefsTagDialog."""
    tag_dialog_instance = MagicMock(spec=PrefsTagDialog)
    tag_dialog_class = MagicMock(return_value=tag_dialog_instance)

    settings = Settings()
    settings.configureForApplication()

    monkeypatch.setattr(
        "music_modify.gui.prefs.dialog_prefs.PrefsTagDialog",
        tag_dialog_class,
    )

    dialog = PrefsDialog(settings)
    qtbot.addWidget(dialog)

    dialog.button_edit_tags.click()

    tag_dialog_class.assert_called_once_with(settings, dialog)
    tag_dialog_instance.setModal.assert_called_once_with(True)
    tag_dialog_instance.show.assert_called_once()


def test_PrefsDialog_buttonEditTags_opensSplitDialog(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, app_info: tuple[str, str, str]
) -> None:
    """Test that clicking Edit Split button opens a PrefsSplitDialog."""
    split_dialog_instance = MagicMock(spec=PrefsSplitDialog)
    split_dialog_class = MagicMock(return_value=split_dialog_instance)

    settings = Settings()
    settings.configureForApplication()

    monkeypatch.setattr(
        "music_modify.gui.prefs.dialog_prefs.PrefsSplitDialog",
        split_dialog_class,
    )

    dialog = PrefsDialog(settings)
    qtbot.addWidget(dialog)

    dialog.button_edit_split.click()

    split_dialog_class.assert_called_once_with(settings, dialog)
    split_dialog_instance.setModal.assert_called_once_with(True)
    split_dialog_instance.show.assert_called_once()
