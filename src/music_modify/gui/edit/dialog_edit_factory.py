"""Module that defines the factory class for creating
different types of Edit dialogs."""

from PySide6.QtWidgets import QWidget

from music_modify.models.song_repository import SongRepository

from .bulk.dialog_edit_bulk import EditBulkDialog
from .dialog_edit import EditDialog
from .dialog_edit_abstract import EditAbstractDialog


class EditDialogFactory:
    """Factory class that creates a different type of Edit dialog,
    depending on whether there are multiple files being edited, or not."""

    def __init__(self, parent: QWidget, repository: SongRepository) -> None:
        """
        Args:
            parent: The widget the new widget should be created on.
            repository: The list of songs the app is managing.
        """
        self.parent: QWidget = parent
        self.repository: SongRepository = repository
        "The list of songs that the app is managing"

    def get(self, rows: list[int], *, bulk: bool = False) -> EditAbstractDialog:
        """Generates a dialog based on whether multiple files should be edited,
        and populates it with the song metadata that should be editable.

        Args:
            rows: List of indexes in the repository for the songs to edit
            bulk (optional): Whether the songs should be edited in bulk or individually.
                Default False.

        Returns:
            A dialog for editing the metadata, of the correct form.
        """
        if bulk:
            return EditBulkDialog(self.parent, self.repository, rows)
        return EditDialog(self.parent, self.repository, rows)
