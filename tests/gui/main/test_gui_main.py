from os import PathLike

from pytestqt.qtbot import QtBot

from music_modify.gui import MainWindow

NUM_TEST_SONGS = 3


def test_getFolderFiles(qtbot: QtBot, asset_folder: PathLike[str]) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    files = window.getFolderFiles(asset_folder)
    assert len(files) == NUM_TEST_SONGS


def test_addFiles(qtbot: QtBot, song_paths: list[PathLike[str]]) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == NUM_TEST_SONGS


def test_clearFiles(qtbot: QtBot, song_paths: list[PathLike[str]]) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == NUM_TEST_SONGS
    window.clearFiles()
    assert window.files_table_view.model().rowCount() == 0


def test_clearFiles_Action(qtbot: QtBot, song_paths: list[PathLike[str]]) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == NUM_TEST_SONGS
    window.action_clear_files.trigger()
    assert window.files_table_view.model().rowCount() == 0


def test_setFileActionState(qtbot: QtBot, song_paths: list[PathLike[str]]) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert not window.action_clear_files.isEnabled()
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == NUM_TEST_SONGS
    assert window.action_clear_files.isEnabled()
    window.action_clear_files.trigger()
    assert window.files_table_view.model().rowCount() == 0
    assert not window.action_clear_files.isEnabled()


def test_setSelectionActionState(qtbot: QtBot, song_paths: list[PathLike[str]]) -> None:
    window = MainWindow()
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


def test_selectAll_Action(qtbot: QtBot, song_paths: list[PathLike[str]]) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == NUM_TEST_SONGS
    window.action_select_all.trigger()
    assert window.getSelectionLength() == NUM_TEST_SONGS


def test_selectNone_Action(qtbot: QtBot, song_paths: list[PathLike[str]]) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == NUM_TEST_SONGS
    window.action_select_all.trigger()
    assert window.getSelectionLength() == NUM_TEST_SONGS
    window.action_select_none.trigger()
    assert window.getSelectionLength() == 0


def test_removeSelectedFiles(qtbot: QtBot, song_paths: list[PathLike[str]]) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == NUM_TEST_SONGS
    window.files_table_view.selectRow(1)
    assert window.getSelectionLength() == 1
    window.removeSelectedFiles()
    assert window.files_table_view.model().rowCount() == NUM_TEST_SONGS - 1
    assert window.getSelectionLength() == 0
    assert not window.action_select_none.isEnabled()


def test_removeSelectedFiles_Action(
    qtbot: QtBot,
    song_paths: list[PathLike[str]],
) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.addFiles(song_paths)
    assert window.files_table_view.model().rowCount() == NUM_TEST_SONGS
    window.files_table_view.selectRow(1)
    assert window.getSelectionLength() == 1
    window.action_remove_selected.trigger()
    assert window.files_table_view.model().rowCount() == NUM_TEST_SONGS - 1
    assert window.getSelectionLength() == 0
    assert not window.action_select_none.isEnabled()


def test_updateStatusbarMessage(qtbot: QtBot, song_paths: list[PathLike[str]]) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.statusLabel.text() == ""
    window.addFiles(song_paths)
    assert window.statusLabel.text() == f"[{NUM_TEST_SONGS} songs]"
    window.files_table_view.selectRow(1)
    assert window.statusLabel.text() == f"[{NUM_TEST_SONGS} songs, 1 selected]"
    window.action_select_none.trigger()
    assert window.statusLabel.text() == f"[{NUM_TEST_SONGS} songs]"
    window.action_clear_files.trigger()
    assert window.statusLabel.text() == ""
