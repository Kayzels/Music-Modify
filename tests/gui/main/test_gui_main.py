"""Tests for MainWindow."""

# pyright: reportUnusedParameter = false

import logging
import os
from os import PathLike
from pathlib import Path
from unittest.mock import MagicMock, call

from PySide6.QtCore import QMimeData, QPoint, QUrl
from PySide6.QtGui import QAction, QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, QMenu, QTableView
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui import MainWindow
from music_modify.prefs import Settings


def test_MainWindow_getFolderFiles(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    asset_folder: str,
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Test that getFolderFiles correctly gets the files from a path."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    files = window.getFolderFiles(asset_folder)
    assert len(files) == num_temp_songs
    assert len(files) == len(song_paths)


def test_MainWindow_addFiles(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Test that addFiles correctly adds the files to the model."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == num_temp_songs


def test_MainWindow_clearFiles(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Test that clearFiles removes the songs from the model."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == num_temp_songs
    window.clearFiles()
    assert window.files_table_view.model().rowCount() == 0


def test_MainWindow_clearFiles_Action(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Test that calling the clearFiles action clears the files."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == num_temp_songs
    window.action_clear_files.trigger()
    assert window.files_table_view.model().rowCount() == 0


def test_MainWindow_setFileActionState(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Test that the state of actions changes based on there being files or not."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    assert not window.action_clear_files.isEnabled()
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == num_temp_songs
    assert window.action_clear_files.isEnabled()
    window.action_clear_files.trigger()
    assert window.files_table_view.model().rowCount() == 0
    assert not window.action_clear_files.isEnabled()


def test_MainWindow_setSelectionActionState(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    temp_settings: Settings,
) -> None:
    """Test that the state of actions changes based on there being a selection."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.action_select_all.isEnabled()
    assert not window.action_select_none.isEnabled()
    window.action_select_all.trigger()
    assert window.action_select_none.isEnabled()
    assert window.action_remove_selected.isEnabled()
    window.action_select_none.trigger()
    assert not window.action_select_none.isEnabled()
    assert not window.action_remove_selected.isEnabled()
    window.clearFiles()
    assert not window.action_select_all.isEnabled()


def test_MainWindow_selectAll_Action(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Tests that calling the select all action selects all songs."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == num_temp_songs
    window.action_select_all.trigger()
    assert window.getSelectionLength() == num_temp_songs


def test_MainWindow_selectNone_Action(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Tests that calling the select none action clears the selection."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == num_temp_songs
    window.action_select_all.trigger()
    assert window.getSelectionLength() == num_temp_songs
    window.action_select_none.trigger()
    assert window.getSelectionLength() == 0


def test_MainWindow_removeSelectedFiles_normal(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Tests that selected files are removed when there is a selection."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == num_temp_songs
    window.files_table_view.selectRow(1)
    assert window.getSelectionLength() == 1
    window.removeSelectedFiles()
    assert window.files_table_view.model().rowCount() == num_temp_songs - 1
    assert window.getSelectionLength() == 0
    assert not window.action_select_none.isEnabled()


def test_MainWindow_removeSelectedFiles_none_selected(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    caplog: pytest.LogCaptureFixture,
    temp_settings: Settings,
) -> None:
    """Tests that removing files with none selection creates a log message."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    window.addFiles(song_paths)

    window.songs_repository.removeAtIndexes = MagicMock()
    window.files_table_view.clearSelection = MagicMock()

    assert window.files_table_view.model().rowCount() == num_temp_songs
    assert window.getSelectionLength() == 0

    with caplog.at_level(logging.DEBUG):
        window.removeSelectedFiles()

        assert "Called clear selection with a length of 0." in caplog.text
        assert caplog.records[0].levelname == "DEBUG"

    assert window.files_table_view.model().rowCount() == num_temp_songs
    window.songs_repository.removeAtIndexes.assert_not_called()
    window.files_table_view.clearSelection.assert_not_called()


def test_MainWindow_removeSelectedFiles_all_selected(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Tests that clearFiles is called if removeSelected is called with all selected."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    window.addFiles(song_paths)

    window.songs_repository.removeAtIndexes = MagicMock()
    window.songs_repository.clear = MagicMock()
    window.files_table_view.clearSelection = MagicMock()

    assert window.files_table_view.model().rowCount() == num_temp_songs
    window.files_table_view.selectAll()

    window.removeSelectedFiles()

    window.songs_repository.clear.assert_called_once()
    window.songs_repository.removeAtIndexes.assert_not_called()
    window.files_table_view.clearSelection.assert_not_called()


def test_MainWindow_removeSelectedFiles_Action(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Tests that the action for remove selected triggers the correct change."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == num_temp_songs
    window.files_table_view.selectRow(1)
    assert window.getSelectionLength() == 1
    window.action_remove_selected.trigger()
    assert window.files_table_view.model().rowCount() == num_temp_songs - 1
    assert window.getSelectionLength() == 0
    assert not window.action_select_none.isEnabled()


def test_MainWindow_updateStatusbarMessage(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
    num_temp_songs: int,
    temp_settings: Settings,
) -> None:
    """Tests that the statusbar values are updated based on state."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)
    assert window.statusLabel.text() == ""
    window.addFiles(song_paths)
    assert window.statusLabel.text() == f"[{num_temp_songs} songs]"
    window.files_table_view.selectRow(1)
    assert window.statusLabel.text() == f"[{num_temp_songs} songs, 1 selected]"
    window.action_select_none.trigger()
    assert window.statusLabel.text() == f"[{num_temp_songs} songs]"
    window.action_clear_files.trigger()
    assert window.statusLabel.text() == ""


def test_MainWindow_addFiles_progress_dialog_canceled(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    song_paths: list[PathLike[str]],
    temp_settings: Settings,
) -> None:
    """Tests cancelling adding files halfway."""
    # Create a local copy of song paths to avoid modifying the fixture.
    current_song_paths: list[PathLike[str]] = list(song_paths)

    # Ensure we have at least 3 song paths for the test scenario
    if len(current_song_paths) < 3:
        current_len = len(current_song_paths)
        new_paths = [
            Path(f"/dummy/path/song_{current_len + i}.mp3")
            for i in range(3 - current_len)
        ]
        current_song_paths.extend(new_paths)

    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_progress_dialog_cls = MagicMock()
    mock_progress_dialog_instance = mock_progress_dialog_cls.return_value

    # Simulate cancellation:
    # 1. For the first file (index 0), wasCanceled() returns False.
    # 2. For the second file (index 1), wasCanceled() returns True,
    #    which breaks the loop.
    # This means addFile will be called for the first two files.
    mock_progress_dialog_instance.wasCanceled.side_effect = [False, True]
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.QProgressDialog", mock_progress_dialog_cls
    )

    mock_add_file = MagicMock()
    monkeypatch.setattr(window.songs_repository, "add", mock_add_file)

    files_to_add = song_paths[:3]

    window.addFiles(files_to_add)

    assert mock_add_file.call_count == 2
    mock_add_file.assert_has_calls(
        [call(files_to_add[0]), call(files_to_add[1])], any_order=False
    )
    # Explicitly confirm that the third file was NOT added
    with pytest.raises(AssertionError):
        mock_add_file.assert_any_call(files_to_add[2])

    assert mock_progress_dialog_instance.wasCanceled.call_count == 2

    mock_progress_dialog_instance.setValue.assert_any_call(0)
    mock_progress_dialog_instance.setValue.assert_any_call(1)
    mock_progress_dialog_instance.setValue.assert_any_call(len(files_to_add))


def test_MainWindow_getFolderFiles_progress_dialog_canceled(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests canceling getFolderFiles halfway."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_base_folder = "/mock/base_folder"

    mock_walk_data: list[
        tuple[os.PathLike[str] | str, tuple[str, ...], tuple[str, ...]]
    ] = [
        (
            Path(mock_base_folder) / "sub1",
            ("",),
            ("song1.mp3", "song2.mp3", "non_mp3.txt"),
        ),
        (
            Path(mock_base_folder) / "sub2",
            ("",),
            ("song3.mp3", "song4.mp3"),
        ),
    ]
    monkeypatch.setattr("os.walk", lambda path: iter(mock_walk_data))

    mock_progress_dialog_cls = MagicMock()
    mock_progress_dialog_instance = mock_progress_dialog_cls.return_value

    # Simulate cancellation:
    # The first time wasCanceled() is called (after processing sub1),
    # it returns True, causing the loop to break.
    mock_progress_dialog_instance.wasCanceled.return_value = True
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.QProgressDialog", mock_progress_dialog_cls
    )

    returned_songs = window.getFolderFiles(mock_base_folder)

    expected_songs = [
        str(Path(mock_base_folder, "sub1", "song1.mp3")),
        str(Path(mock_base_folder, "sub1", "song2.mp3")),
    ]
    assert returned_songs == expected_songs
    assert len(returned_songs) == 2
    assert mock_progress_dialog_instance.wasCanceled.call_count == 1
    mock_progress_dialog_instance.setLabelText.assert_has_calls(
        [call("1 found."), call("2 found.")], any_order=False
    )


def test_MainWindow_processTableDragEvent_has_urls(
    qtbot: QtBot, temp_settings: Settings
) -> None:
    """Tests processing drag events when valid urls sent.

    The action should be accepted, and the data should be processed.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_mime_data = MagicMock(spec=QMimeData)
    mock_mime_data.hasUrls.return_value = True

    mock_event = MagicMock(spec=QDragEnterEvent)
    mock_event.mimeData.return_value = mock_mime_data

    window.processTableDragEvent(mock_event)

    mock_mime_data.hasUrls.assert_called_once()
    mock_event.acceptProposedAction.assert_called_once()


def test_MainWindow_processTableDragEvent_no_urls(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture, temp_settings: Settings
) -> None:
    """Tests processing drag events when no urls are sent.

    The action should be rejected, and a log warning should be made.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_mime_data = MagicMock(spec=QMimeData)
    mock_mime_data.hasUrls.return_value = False

    mock_event = MagicMock(spec=QDragEnterEvent)
    mock_event.mimeData.return_value = mock_mime_data

    with caplog.at_level(logging.WARNING):
        window.processTableDragEvent(mock_event)
        assert "Unsupported mimedata when drag/dropping" in caplog.text
        assert caplog.records[0].levelname == "WARNING"

    mock_mime_data.hasUrls.assert_called_once()
    mock_event.acceptProposedAction.assert_not_called()


def test_MainWindow_processTableDropEvents_drop_files(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    song_paths: list[PathLike[str]],
    temp_settings: Settings,
) -> None:
    """Tests prop events when files are dropped on a table.

    Each of the files should be added, if not already present.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_urls = []
    for path in song_paths:
        mock_url = MagicMock(spec=QUrl)
        mock_url.toLocalFile.return_value = str(path)
        mock_urls.append(mock_url)

    mock_mime_data = MagicMock(spec=QMimeData)
    mock_mime_data.urls.return_value = mock_urls

    mock_event = MagicMock(spec=QDropEvent)
    mock_event.mimeData.return_value = mock_mime_data

    mock_add_files = MagicMock()
    monkeypatch.setattr(window, "addFiles", mock_add_files)

    window.processTableDropEvents(mock_event)

    for url in mock_urls:
        url.toLocalFile.assert_called_once()
    assert mock_event.acceptProposedAction.call_count == len(song_paths)
    mock_add_files.assert_called_once_with([str(path) for path in song_paths])


def test_MainWindow_processTableDropEvents_drop_folders(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    song_paths: list[PathLike[str]],
    asset_folder: str,
    temp_settings: Settings,
) -> None:
    """Tests prop events when folders are dropped on a table.

    Each of the files in the folders should be added, if not already present.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_folder_url = MagicMock(spec=QUrl)
    mock_folder_url.toLocalFile.return_value = asset_folder

    mock_mime_data = MagicMock(spec=QMimeData)
    mock_mime_data.urls.return_value = [mock_folder_url]

    mock_event = MagicMock(spec=QDropEvent)
    mock_event.mimeData.return_value = mock_mime_data

    mock_get_folder_files = MagicMock(return_value=[str(path) for path in song_paths])
    monkeypatch.setattr(window, "getFolderFiles", mock_get_folder_files)

    mock_add_files = MagicMock()
    monkeypatch.setattr(window, "addFiles", mock_add_files)

    window.processTableDropEvents(mock_event)

    mock_folder_url.toLocalFile.assert_called_once()
    mock_event.acceptProposedAction.assert_called_once()
    mock_get_folder_files.assert_called_once_with(asset_folder)
    mock_add_files.assert_called_once_with([str(path) for path in song_paths])


def test_MainWindow_processTableDropEvents_drop_mixed_files_and_folders(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    song_path: Path,
    song_paths: list[PathLike[str]],
    asset_folder: str,
    temp_settings: Settings,
) -> None:
    """Tests dropping files and folders together on a table.

    Each of the individual files should be added, if not already present.
    Each of the files in the folders should be added, if not already present.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    # One MP3 file URL
    mock_file_url = MagicMock(spec=QUrl)
    mock_file_url.toLocalFile.return_value = str(song_path)

    # One folder URL
    mock_folder_url = MagicMock(spec=QUrl)
    mock_folder_url.toLocalFile.return_value = asset_folder

    mock_mime_data = MagicMock(spec=QMimeData)
    mock_mime_data.urls.return_value = [mock_file_url, mock_folder_url]

    mock_event = MagicMock(spec=QDropEvent)
    mock_event.mimeData.return_value = mock_mime_data

    mock_get_folder_files = MagicMock(return_value=[str(path) for path in song_paths])
    monkeypatch.setattr(window, "getFolderFiles", mock_get_folder_files)

    mock_add_files = MagicMock()
    monkeypatch.setattr(window, "addFiles", mock_add_files)

    window.processTableDropEvents(mock_event)

    mock_file_url.toLocalFile.assert_called_once()
    mock_folder_url.toLocalFile.assert_called_once()
    assert (
        mock_event.acceptProposedAction.call_count == 2
    )  # Once for file, once for folder
    mock_get_folder_files.assert_called_once_with(asset_folder)
    # addFiles should be called twice:
    # once for the initial file,
    # once for files from folder
    assert mock_add_files.call_count == 2

    mock_add_files.assert_any_call([str(path) for path in song_paths])
    mock_add_files.assert_any_call([str(song_path)])


def test_MainWindow_processTableDropEvents_unsupported_mime_data(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests drop events where the mimedata isn't valid.

    The action should be rejected, and no files or folders should be added.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_mime_data = MagicMock(spec=QMimeData)
    mock_mime_data.urls.return_value = []  # No URLs

    mock_event = MagicMock(spec=QDropEvent)
    mock_event.mimeData.return_value = mock_mime_data

    mock_add_files = MagicMock()
    monkeypatch.setattr(window, "addFiles", mock_add_files)
    mock_get_folder_files = MagicMock()
    monkeypatch.setattr(window, "getFolderFiles", mock_get_folder_files)

    window.processTableDropEvents(mock_event)

    mock_event.acceptProposedAction.assert_not_called()
    mock_add_files.assert_not_called()
    mock_get_folder_files.assert_not_called()


def test_MainWindow_addStatusbarMessage_no_app(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests that the status bar message isn't added if invalid.

    If there isn't a QApplication instance, the text shouldn't be set.
    This should _never_ happen, though.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    monkeypatch.setattr(QApplication, "instance", MagicMock(return_value=None))

    window.versionMessage.setText = MagicMock()

    window.addStatusbarAppMessage()

    window.versionMessage.setText.assert_not_called()


def test_MainWindow_showAboutDialog(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests that showAboutDialog creates and displays an AboutDialog."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_about_dialog_instance = MagicMock()
    mock_about_dialog_class = MagicMock(return_value=mock_about_dialog_instance)
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.AboutDialog", mock_about_dialog_class
    )

    window.showAboutDialog()

    mock_about_dialog_class.assert_called_once_with(window)
    mock_about_dialog_instance.show.assert_called_once()


def test_MainWindow_showPrefsDialog(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests that showPrefsDialog creates and displays an PrefsDialog."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_prefs_dialog_instance = MagicMock()
    mock_prefs_dialog_class = MagicMock(return_value=mock_prefs_dialog_instance)
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.PrefsDialog", mock_prefs_dialog_class
    )

    mock_refresh_table = MagicMock()
    monkeypatch.setattr(window, "refreshTableLayout", mock_refresh_table)

    window.showPrefsDialog()

    mock_prefs_dialog_class.assert_called_once_with(
        parent=window, settings=temp_settings
    )
    mock_prefs_dialog_instance.show.assert_called_once()


def test_MainWindow_refreshTable(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests that refreshTable updates the repo, model, and view."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    window.songs_repository.refreshDisplay = MagicMock()

    mock_update_table_view = MagicMock()
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.updateTableView", mock_update_table_view
    )

    with qtbot.waitSignals(
        [window.songs_model.layoutAboutToBeChanged, window.songs_model.layoutChanged]
    ):
        window.refreshTable()

    window.songs_repository.refreshDisplay.assert_called_once()
    mock_update_table_view.assert_called_once_with(
        window.files_table_view, window.songs_repository, temp_settings.table_tags
    )


def test_MainWindow_showEditDialog_no_selection(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests that an EditDialog is not created if there is no selection."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_get_selected_rows = MagicMock(return_value=[])
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.getSelectedRows", mock_get_selected_rows
    )

    mock_dialog_factory_get = MagicMock()
    monkeypatch.setattr(window.dialog_factory, "get", mock_dialog_factory_get)

    window.showEditDialog()

    mock_get_selected_rows.assert_called_once_with(window.files_table_view)
    mock_dialog_factory_get.assert_not_called()


def test_MainWindow_showEditDialog_individual_edit_accepted(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests creating an EditDialog for multiple songs, but editing individually.

    Tests that the signals for the dialog are connected correctly,
    and that information gets updated when the dialog is accepted.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    selected_rows = [0, 2, 1]  # Unsorted
    expected_sorted_rows = [0, 1, 2]

    mock_get_selected_rows = MagicMock(return_value=selected_rows)
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.getSelectedRows", mock_get_selected_rows
    )

    mock_edit_dialog_instance = MagicMock()
    mock_edit_dialog_instance.info_updated.connect = MagicMock()
    mock_edit_dialog_instance.finished.connect = MagicMock()
    mock_edit_dialog_instance.updateSongInfo = MagicMock()
    mock_edit_dialog_instance.show = MagicMock()

    mock_dialog_factory_get = MagicMock(return_value=mock_edit_dialog_instance)
    monkeypatch.setattr(window.dialog_factory, "get", mock_dialog_factory_get)

    window.showEditDialog(bulk=False)

    mock_get_selected_rows.assert_called_once_with(window.files_table_view)
    mock_dialog_factory_get.assert_called_once_with(
        expected_sorted_rows,
        temp_settings.all_tags,
        temp_settings.split_text_entered,
        bulk=False,
    )

    # Verify the info_updated signal is connected to the window's refreshTable method
    mock_edit_dialog_instance.info_updated.connect.assert_called_once_with(
        window.refreshTable
    )

    # Verify the finished signal is connected to a callable (processDialogResult)
    mock_edit_dialog_instance.finished.connect.assert_called_once()
    mock_edit_dialog_instance.show.assert_called_once()

    # Get the callable passed to dialog.finished.connect and simulate acceptance
    process_result = mock_edit_dialog_instance.finished.connect.call_args[0][0]
    process_result(QDialog.DialogCode.Accepted)
    mock_edit_dialog_instance.updateSongInfo.assert_called_once()


def test_MainWindow_showEditDialog_individual_edit_rejected(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests creating an EditDialog for multiple songs, but editing individually.

    Tests that the signals for the dialog are connected correctly,
    and that information does not get updated when the dialog is rejected.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    selected_rows = [0]

    mock_get_selected_rows = MagicMock(return_value=selected_rows)
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.getSelectedRows", mock_get_selected_rows
    )

    mock_edit_dialog_instance = MagicMock()
    mock_edit_dialog_instance.info_updated.connect = MagicMock()
    mock_edit_dialog_instance.finished.connect = MagicMock()
    mock_edit_dialog_instance.updateSongInfo = MagicMock()
    mock_edit_dialog_instance.show = MagicMock()

    mock_dialog_factory_get = MagicMock(return_value=mock_edit_dialog_instance)
    monkeypatch.setattr(window.dialog_factory, "get", mock_dialog_factory_get)

    window.showEditDialog(bulk=False)

    mock_get_selected_rows.assert_called_once_with(window.files_table_view)
    mock_dialog_factory_get.assert_called_once_with(
        selected_rows,
        temp_settings.all_tags,
        temp_settings.split_text_entered,
        bulk=False,
    )
    mock_edit_dialog_instance.info_updated.connect.assert_called_once_with(
        window.refreshTable
    )
    mock_edit_dialog_instance.finished.connect.assert_called_once()
    mock_edit_dialog_instance.show.assert_called_once()

    # Get the callable passed to dialog.finished.connect and simulate rejection
    process_result = mock_edit_dialog_instance.finished.connect.call_args[0][0]
    process_result(QDialog.DialogCode.Rejected)
    mock_edit_dialog_instance.updateSongInfo.assert_not_called()


def test_MainWindow_showEditDialog_bulk_edit_accepted(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests creating an EditDialog for multiple songs, edited in bulk.

    Tests that the signals for the dialog are connected correctly,
    and that information gets updated when the dialog is accepted.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    selected_rows = [0, 1]

    mock_get_selected_rows = MagicMock(return_value=selected_rows)
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.getSelectedRows", mock_get_selected_rows
    )

    mock_edit_dialog_instance = MagicMock()
    mock_edit_dialog_instance.info_updated.connect = MagicMock()
    mock_edit_dialog_instance.finished.connect = MagicMock()
    mock_edit_dialog_instance.updateSongInfo = MagicMock()
    mock_edit_dialog_instance.show = MagicMock()

    mock_dialog_factory_get = MagicMock(return_value=mock_edit_dialog_instance)
    monkeypatch.setattr(window.dialog_factory, "get", mock_dialog_factory_get)

    window.showEditDialog(bulk=True)

    mock_get_selected_rows.assert_called_once_with(window.files_table_view)
    mock_dialog_factory_get.assert_called_once_with(
        selected_rows,
        temp_settings.all_tags,
        temp_settings.split_text_entered,
        bulk=True,
    )
    mock_edit_dialog_instance.info_updated.connect.assert_called_once_with(
        window.refreshTable
    )
    mock_edit_dialog_instance.finished.connect.assert_called_once()
    mock_edit_dialog_instance.show.assert_called_once()

    # Get the callable passed to dialog.finished.connect and simulate acceptance
    process_result = mock_edit_dialog_instance.finished.connect.call_args[0][0]
    process_result(QDialog.DialogCode.Accepted)
    mock_edit_dialog_instance.updateSongInfo.assert_called_once()


def _getMockQFileDialogClass(mock_instance: MagicMock) -> MagicMock:
    """Creates a mock QFileDialog.

    This is needed so that the enums can still be checked correctly.
    """
    mock_class = MagicMock(return_value=mock_instance)
    mock_class.FileMode = QFileDialog.FileMode
    mock_class.DialogCode = QDialog.DialogCode
    return mock_class


def test_MainWindow_openAddDialog_existing_files(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    song_paths: list[PathLike[str]],
    temp_settings: Settings,
) -> None:
    """Test that openAddDialog processes files and calls add correctly."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_file_dialog_instance = MagicMock()
    mock_file_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
    mock_file_dialog_instance.selectedFiles.return_value = song_paths

    mock_qfile_dialog_class = _getMockQFileDialogClass(mock_file_dialog_instance)
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.QFileDialog", mock_qfile_dialog_class
    )

    mock_add_files = MagicMock()
    monkeypatch.setattr(window, "addFiles", mock_add_files)

    window.openAddDialog(QFileDialog.FileMode.ExistingFiles)

    mock_qfile_dialog_class.assert_called_once_with(window)
    mock_file_dialog_instance.setFileMode.assert_called_once_with(
        QFileDialog.FileMode.ExistingFiles
    )
    mock_file_dialog_instance.setNameFilter.assert_called_once_with("MP3 Files (*.mp3)")
    mock_file_dialog_instance.exec.assert_called_once()
    mock_file_dialog_instance.selectedFiles.assert_called_once()
    mock_add_files.assert_called_once_with(song_paths)


def test_MainWindow_openAddDialog_directory_mode(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    song_paths: list[PathLike[str]],
    asset_folder: str,
    temp_settings: Settings,
) -> None:
    """Test that openAddDialog processes folders and calls add correctly."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_file_dialog_instance = MagicMock()
    mock_file_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
    mock_file_dialog_instance.selectedFiles.return_value = [asset_folder]

    mock_qfile_dialog_class = _getMockQFileDialogClass(mock_file_dialog_instance)
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.QFileDialog", mock_qfile_dialog_class
    )

    mock_get_folder_files = MagicMock(return_value=song_paths)
    monkeypatch.setattr(window, "getFolderFiles", mock_get_folder_files)

    mock_add_files = MagicMock()
    monkeypatch.setattr(window, "addFiles", mock_add_files)

    window.openAddDialog(QFileDialog.FileMode.Directory)

    mock_qfile_dialog_class.assert_called_once_with(window)
    mock_file_dialog_instance.setFileMode.assert_called_once_with(
        QFileDialog.FileMode.Directory
    )
    mock_file_dialog_instance.setNameFilter.assert_not_called()
    mock_file_dialog_instance.exec.assert_called_once()
    mock_file_dialog_instance.selectedFiles.assert_called_once()
    mock_get_folder_files.assert_called_once_with(asset_folder)
    mock_add_files.assert_called_once_with(song_paths)


def test_MainWindow_openAddDialog_cancelled(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests that files aren't added if the AddDialog is cancelled."""
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_file_dialog_instance = MagicMock()
    mock_file_dialog_instance.exec.return_value = QDialog.DialogCode.Rejected

    mock_qfile_dialog_class = _getMockQFileDialogClass(mock_file_dialog_instance)
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.QFileDialog", mock_qfile_dialog_class
    )

    mock_add_files = MagicMock()
    monkeypatch.setattr(window, "addFiles", mock_add_files)
    mock_get_folder_files = MagicMock()
    monkeypatch.setattr(window, "getFolderFiles", mock_get_folder_files)

    window.openAddDialog(QFileDialog.FileMode.ExistingFiles)

    mock_qfile_dialog_class.assert_called_once_with(window)
    mock_file_dialog_instance.exec.assert_called_once()
    mock_file_dialog_instance.selectedFiles.assert_not_called()
    mock_add_files.assert_not_called()
    mock_get_folder_files.assert_not_called()


class _MockQMenu(MagicMock):
    """Mock class for QMenu, to test action and submenu creation."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        super().__init__(*args, **kwargs)
        self.added_actions_list: list[QAction] = []
        self.added_menus_list: list[QMenu] = []
        self.popup = MagicMock()

    def addAction(self, action: QAction) -> MagicMock:
        self.added_actions_list.append(action)
        return MagicMock(spec=QAction)

    def addActions(self, actions_list: list[QAction]) -> None:
        for action in actions_list:
            self.addAction(action)

    def addMenu(self, menu: QMenu) -> MagicMock:
        self.added_menus_list.append(menu)
        return MagicMock(spec=QAction)


def test_MainWindow_showCustomContextMenu_invalid_index(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    temp_settings: Settings,
) -> None:
    """Tests that a custom context menu isn't created for an invalid index.

    This is the case when the click isn't on an item in the table.

    This should be logged.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_index = MagicMock()
    mock_index.isValid.return_value = False
    window.files_table_view.indexAt = MagicMock(return_value=mock_index)

    # Mock QMenu constructor to ensure it's not called
    mock_qmenu_constructor = MagicMock(side_effect=_MockQMenu)
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.QMenu", mock_qmenu_constructor
    )

    position = QPoint(50, 50)

    with caplog.at_level(logging.INFO):
        window.showCustomContextMenu(position)

    window.files_table_view.indexAt.assert_called_once_with(position)
    mock_index.isValid.assert_called_once()
    mock_qmenu_constructor.assert_not_called()
    assert "Invalid index when calling custom context menu" in caplog.text
    assert caplog.records[0].levelname == "INFO"


def test_MainWindow_showCustomContextMenu_single_selection(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests creating a custom context menu with only one item selected.

    The menu should be created, but there should be no option for bulk editing.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_index = MagicMock()
    mock_index.isValid.return_value = True
    window.files_table_view.indexAt = MagicMock(return_value=mock_index)

    window.getSelectionLength = MagicMock(return_value=1)

    mock_context_menu = _MockQMenu()
    mock_qmenu_constructor = MagicMock(return_value=mock_context_menu)
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.QMenu", mock_qmenu_constructor
    )

    global_position = QPoint(100, 100)
    window.files_table_view.viewport().mapToGlobal = MagicMock(
        return_value=global_position
    )

    position = QPoint(50, 50)
    window.showCustomContextMenu(position)

    window.files_table_view.indexAt.assert_called_once_with(position)
    mock_index.isValid.assert_called_once()
    window.getSelectionLength.assert_called_once()

    mock_qmenu_constructor.assert_called_once_with(window)
    assert mock_context_menu.added_actions_list == [
        window.action_edit_individual,
        window.action_remove_selected,
    ]
    assert not mock_context_menu.added_menus_list

    mock_context_menu.popup.assert_called_once_with(global_position)


def test_MainWindow_showCustomContextMenu_multiple_selection(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests creating a custom context menu with multiple items selected.

    The menu should be created, and there should be options for bulk editing
    and individual editing.
    """
    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_index = MagicMock()
    mock_index.isValid.return_value = True
    window.files_table_view.indexAt = MagicMock(return_value=mock_index)

    window.getSelectionLength = MagicMock(return_value=5)

    mock_context_menu = _MockQMenu()
    mock_song_menu = _MockQMenu()

    # Configure side_effect for QMenu constructor to return mock_context_menu
    # for the first call, and mock_song_menu for the second call.
    mock_qmenu_constructor = MagicMock(side_effect=[mock_context_menu, mock_song_menu])
    monkeypatch.setattr(
        "music_modify.gui.main.window_main.QMenu", mock_qmenu_constructor
    )

    global_position = QPoint(100, 100)
    window.files_table_view.viewport().mapToGlobal = MagicMock(
        return_value=global_position
    )

    position = QPoint(50, 50)
    window.showCustomContextMenu(position)

    window.files_table_view.indexAt.assert_called_once_with(position)
    mock_index.isValid.assert_called_once()
    window.getSelectionLength.assert_called_once()

    # Verify QMenu constructors were called correctly
    assert mock_qmenu_constructor.call_count == 2
    mock_qmenu_constructor.assert_has_calls(
        [
            call(window),  # For the main context_menu
            call("Edit Songs"),  # For the song_menu sub-menu
        ]
    )

    # Check that actions from menu_edit_songs are added to the mock_song_menu
    expected_song_menu_actions = [
        window.action_edit_individual,
        window.action_edit_bulk,
    ]
    assert mock_song_menu.added_actions_list == expected_song_menu_actions

    # Check that the song_menu was added as a sub-menu to the context_menu
    assert mock_context_menu.added_menus_list == [mock_song_menu]
    # Check that action_remove_selected is directly in the main context menu
    assert mock_context_menu.added_actions_list == [window.action_remove_selected]

    mock_context_menu.popup.assert_called_once_with(global_position)


def test_MainWindow_action_triggers(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, temp_settings: Settings
) -> None:
    """Tests that the actions are linked to the correct slots."""
    # These two need to be done before the class is created,
    # because the connections are made in init to files_table_view,
    # so mocking those after won't test the one called from the signal
    mock_select_all = MagicMock()
    mock_select_none = MagicMock()

    monkeypatch.setattr(QTableView, "selectAll", mock_select_all)
    monkeypatch.setattr(QTableView, "clearSelection", mock_select_none)

    window = MainWindow(temp_settings)
    qtbot.addWidget(window)

    mock_open_add_dialog = MagicMock()
    mock_clear_files = MagicMock()
    mock_show_prefs_dialog = MagicMock()
    mock_show_about_dialog = MagicMock()
    mock_remove_selected_files = MagicMock()
    mock_show_edit_dialog = MagicMock()

    monkeypatch.setattr(window, "openAddDialog", mock_open_add_dialog)
    monkeypatch.setattr(window, "clearFiles", mock_clear_files)
    monkeypatch.setattr(window, "showPrefsDialog", mock_show_prefs_dialog)
    monkeypatch.setattr(window, "showAboutDialog", mock_show_about_dialog)
    monkeypatch.setattr(window, "removeSelectedFiles", mock_remove_selected_files)
    monkeypatch.setattr(window, "showEditDialog", mock_show_edit_dialog)

    # Test Select All
    window.action_select_all.setEnabled(True)
    window.action_select_all.trigger()
    mock_select_all.assert_called_once()

    # Test Select None
    window.action_select_none.setEnabled(True)
    window.action_select_none.trigger()
    mock_select_none.assert_called_once()

    # Adding folders and files use lambdas that needs to be manually patched.
    # Trigger the action and then verify the mock for openAddDialog.

    # Test Add Files
    window.action_add_files.trigger()
    mock_open_add_dialog.assert_called_once_with(QFileDialog.FileMode.ExistingFiles)
    mock_open_add_dialog.reset_mock()

    # Test Add Folder
    window.action_add_folder.trigger()
    mock_open_add_dialog.assert_called_once_with(QFileDialog.FileMode.Directory)
    mock_open_add_dialog.reset_mock()

    # Test Clear Files
    window.action_clear_files.setEnabled(True)
    window.action_clear_files.trigger()
    mock_clear_files.assert_called_once()

    # Test Preferences
    window.action_preferences.trigger()
    mock_show_prefs_dialog.assert_called_once()

    # Test About Music Modify
    window.action_about.trigger()
    mock_show_about_dialog.assert_called_once()

    # Test Remove Selected
    window.action_remove_selected.setEnabled(True)
    window.action_remove_selected.trigger()
    mock_remove_selected_files.assert_called_once()

    # Test Edit individually
    window.action_edit_individual.setEnabled(True)
    window.action_edit_individual.trigger()
    mock_show_edit_dialog.assert_called_once_with()  # default bulk=False

    # Test Edit in bulk
    window.action_edit_bulk.setEnabled(True)
    window.action_edit_bulk.trigger()
    mock_show_edit_dialog.assert_called_with(bulk=True)
