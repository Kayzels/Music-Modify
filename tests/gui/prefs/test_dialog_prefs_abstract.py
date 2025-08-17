from typing import override
from unittest.mock import MagicMock

from PySide6.QtWidgets import QMessageBox
import pytest
from pytestqt.qtbot import QtBot

import music_modify.gui.prefs.dialog_prefs_abstract as abstract_prefs_dialog_module


def test_prefsAbstractDialog_missingButtonBox(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Mock QMessageBox.warning to prevent a real dialog from appearing
    mock_qmessagebox_warning = MagicMock()
    monkeypatch.setattr(QMessageBox, "warning", mock_qmessagebox_warning)

    # Mock the logger's warning method
    mock_logger_warning = MagicMock()
    monkeypatch.setattr(
        abstract_prefs_dialog_module.logger,
        "warning",
        mock_logger_warning,
    )

    class TestDialogWithoutButtonBox(abstract_prefs_dialog_module.PrefsAbstractDialog):
        """A temporary dialog class that deliberately does not set button_box."""

        @override
        def setupUi(
            self,
            dialog: abstract_prefs_dialog_module.PrefsAbstractDialog,
            /,
        ) -> None:
            pass

        @override
        def updateSettings(self) -> None:
            pass

        @override
        def restoreDefaults(self) -> None:
            pass

        @override
        def resetSettings(self) -> None:
            pass

    test_dialog = TestDialogWithoutButtonBox()
    qtbot.addWidget(test_dialog)

    expected_warning = "Button Box not found or invalid after calling setupUi()."

    # Assert QMessageBox.warning called with the expected arguments.
    mock_qmessagebox_warning.assert_called_once_with(
        test_dialog,
        "Missing attributes",
        expected_warning,
    )

    # Assert logger's warning method called with the expected arguments.
    mock_logger_warning.assert_called_once_with(expected_warning)
