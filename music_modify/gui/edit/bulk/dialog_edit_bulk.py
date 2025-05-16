from typing import override

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from music_modify.gui.edit.dialog_edit_abstract import EditAbstractDialog
from music_modify.models.song_repository import SongRepository


class EditBulkDialog(EditAbstractDialog):
    """A dialog that allows editing the tags of multiple songs at the same time."""

    info_updated: Signal = Signal()

    def __init__(
        self, parent: QWidget, repository: SongRepository, rows: list[int]
    ) -> None:
        super().__init__(parent, repository, rows)

        self.setupUi()

    @override
    def _setupSongInfo(self) -> None:
        # TODO: Display song information and widgets
        pass

    @override
    def updateSongInfo(self) -> None:
        """Update all selected songs to have the changed data."""
        raise NotImplementedError

    @override
    def resetSongInfo(self) -> None:
        """Reset the songs to the values they had when opening the dialog."""
        raise NotImplementedError
