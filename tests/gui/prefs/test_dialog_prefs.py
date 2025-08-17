from typing import TYPE_CHECKING, cast, override
from unittest.mock import MagicMock

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialogButtonBox, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.prefs.dialog_prefs import PrefsDialog
from music_modify.gui.prefs.dialog_prefs_abstract import PrefsAbstractDialog
from music_modify.gui.prefs.dialog_prefs_split import PrefsSplitDialog
from music_modify.gui.prefs.dialog_prefs_tag import PrefsTagDialog

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any


class MockAbstractChildDialog(PrefsAbstractDialog):
    """A mock dialog for testing the generic behaviour of openChildDialog."""

    settings_updated: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setModal: Callable[[bool, Any], None] = MagicMock()
        self.show: Callable[..., None] = MagicMock()

    @override
    def setupUi(self, dialog: PrefsAbstractDialog, /) -> None:
        # noinspection PyTypeChecker
        self.button_box: QDialogButtonBox | None = QDialogButtonBox(
            QDialogButtonBox.StandardButton.RestoreDefaults
            | QDialogButtonBox.StandardButton.Reset,
        )

    @override
    def updateSettings(self) -> None:
        pass

    @override
    def restoreDefaults(self) -> None:
        pass

    @override
    def resetSettings(self) -> None:
        pass


# noinspection PyUnresolvedReferences
def test_PrefsDialog_openChildDialog_logic(qtbot: QtBot) -> None:
    child_dialog = MockAbstractChildDialog()
    qtbot.addWidget(child_dialog)
    child_dialog_class: type[PrefsAbstractDialog] = cast(
        type[PrefsAbstractDialog],
        MagicMock(return_value=child_dialog),
    )

    parent_dialog = PrefsDialog()
    qtbot.addWidget(parent_dialog)

    mock_parent_settings_updated = MagicMock()
    parent_dialog.settings_updated.connect(mock_parent_settings_updated)

    parent_dialog.openChildDialog(child_dialog_class)

    child_dialog_class.assert_called_once_with(parent_dialog)  # pyright: ignore[reportAttributeAccessIssue]
    child_dialog.setModal.assert_called_once_with(True)  # noqa: FBT003  # pyright: ignore[reportFunctionMemberAccess]
    child_dialog.show.assert_called_once()  # pyright: ignore[reportFunctionMemberAccess]

    child_dialog.settings_updated.emit()
    mock_parent_settings_updated.assert_called_once()


def test_PrefsDialog_buttonEditTags_opensTagDialog(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tag_dialog_instance = MagicMock(spec=PrefsTagDialog)
    tag_dialog_class = MagicMock(return_value=tag_dialog_instance)

    monkeypatch.setattr(
        "music_modify.gui.prefs.dialog_prefs.PrefsTagDialog",
        tag_dialog_class,
    )

    dialog = PrefsDialog()
    qtbot.addWidget(dialog)

    dialog.button_edit_tags.click()

    tag_dialog_class.assert_called_once_with(dialog)
    tag_dialog_instance.setModal.assert_called_once_with(True)  # noqa: FBT003
    tag_dialog_instance.show.assert_called_once()


def test_PrefsDialog_buttonEditTags_opensSplitDialog(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    split_dialog_instance = MagicMock(spec=PrefsSplitDialog)
    split_dialog_class = MagicMock(return_value=split_dialog_instance)

    monkeypatch.setattr(
        "music_modify.gui.prefs.dialog_prefs.PrefsSplitDialog",
        split_dialog_class,
    )

    dialog = PrefsDialog()
    qtbot.addWidget(dialog)

    dialog.button_edit_split.click()

    split_dialog_class.assert_called_once_with(dialog)
    split_dialog_instance.setModal.assert_called_once_with(True)  # noqa: FBT003
    split_dialog_instance.show.assert_called_once()
