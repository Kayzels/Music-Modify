"""Tests for AboutDialog."""

import datetime
import logging
import platform
from unittest.mock import MagicMock

import mutagen
import PySide6
from PySide6.QtWidgets import QApplication, QDialogButtonBox, QLayout, QTextEdit
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.about.dialog_about import AboutDialog


def test_AboutDialog_generateText_no_instance(
    caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that AboutDialog issues warning when there is no QApplication instance."""

    def mock_qapplication_instance() -> None:
        return None

    monkeypatch.setattr(QApplication, "instance", mock_qapplication_instance)

    with caplog.at_level(logging.WARNING):
        result = AboutDialog.generateText()

        assert result == ""
        assert "Application instance was None when calling generateText" in caplog.text
        assert caplog.records[0].levelname == "WARNING"


def test_AboutDialog_generateText_valid_instance(
    monkeypatch: pytest.MonkeyPatch,
    app_info: tuple[str, str],
) -> None:
    """Test that generateText creates the correct HTML when app info is valid."""
    mock_app_name, mock_app_version = app_info
    mock_python_version = "3.10.0"
    mock_pyside_version = "6.5.0"
    mock_mutagen_version = "1.50"

    monkeypatch.setattr(platform, "python_version", lambda: mock_python_version)
    monkeypatch.setattr(PySide6, "__version__", mock_pyside_version)
    monkeypatch.setattr(mutagen, "version_string", mock_mutagen_version)

    fake_datetime_year = 2077
    fake_now = datetime.datetime(fake_datetime_year, 1, 1)
    mock_datetime_class = MagicMock(wraps=datetime.datetime)
    mock_datetime_class.now.return_value = fake_now

    monkeypatch.setattr(
        "music_modify.gui.about.dialog_about.datetime", mock_datetime_class
    )

    expected_html_parts = [
        f"<h1>{mock_app_name}</h1>",
        f"<p>Version {mock_app_version}</p>",
        "A music tag editor written using PySide6 and Qt.",
        f"<p>Copyright © {fake_datetime_year} Kyzan Hartwig</p>",
        "<h2>Tools Used</h2>",
        f"<li>Python {mock_python_version}</li>",
        f"<li>PySide {mock_pyside_version}</li>",
        f"<li>Qt {mock_pyside_version}</li>",
        f"<li>mutagen {mock_mutagen_version}</li>",
    ]

    result_html = AboutDialog.generateText()

    for part in expected_html_parts:
        assert part in result_html

    assert "<!DOCTYPE HTML PUBLIC" in result_html
    assert "<html>" in result_html
    assert "</html>" in result_html
    assert "<body>" in result_html
    assert "</body>" in result_html


def test_AboutDialog_setupUi(qtbot: QtBot) -> None:
    """Test that setupUi works properly for AboutDialog."""
    dialog = AboutDialog()
    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == "About Music Modify"

    layout = dialog.layout()
    assert layout is not None
    assert isinstance(layout, QLayout)

    text_edit = dialog.findChild(QTextEdit)
    assert text_edit is not None
    assert not text_edit.isUndoRedoEnabled()
    assert text_edit.isReadOnly()

    button_box = dialog.findChild(QDialogButtonBox)
    assert button_box is not None
    assert QDialogButtonBox.StandardButton.Close in button_box.standardButtons()
