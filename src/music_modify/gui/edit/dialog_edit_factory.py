from PySide6.QtWidgets import QWidget

from music_modify.models.song_repository import SongRepository

from .bulk.dialog_edit_bulk import EditBulkDialog
from .dialog_edit import EditDialog
from .dialog_edit_abstract import EditAbstractDialog


class EditDialogFactory:
    def __init__(self, parent: QWidget, repository: SongRepository) -> None:
        self.parent: QWidget = parent
        self.repository: SongRepository = repository

    def get(self, rows: list[int], bulk: bool = False) -> EditAbstractDialog:
        if bulk:
            return EditBulkDialog(self.parent, self.repository, rows)
        return EditDialog(self.parent, self.repository, rows)
