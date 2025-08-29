"""Tests for PrefsAbstractDialog."""

from typing import override

import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.prefs.dialog_prefs_abstract import PrefsAbstractDialog


def test_prefsAbstractDialog_missingLayout(qtbot: QtBot) -> None:
    """Test that if the dialog doesn't set layout, there is an exception."""

    class TestDialogWithoutLayout(PrefsAbstractDialog):
        """A temporary dialog class that deliberately does not set a layout."""

        @override
        def setupUi(self) -> None:
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

    expected_exception_message = "Layout not set for dialog in setupUi"

    w: TestDialogWithoutLayout | None = None
    with pytest.raises(Exception, match=expected_exception_message) as excinfo:
        w = TestDialogWithoutLayout()
    if w:
        qtbot.addWidget(w)

    assert str(excinfo.value) == expected_exception_message
