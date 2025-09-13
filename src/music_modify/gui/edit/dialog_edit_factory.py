"""Module that defines an EditDialogFactory.

This is the factory class for creating different types of Edit dialogs.
"""

from PySide6.QtWidgets import QWidget

from music_modify.custom_types.songtag import SongTag
from music_modify.models.song_repository import SongRepository

from .bulk.dialog_edit_bulk import EditBulkDialog
from .dialog_edit import EditDialog
from .dialog_edit_abstract import EditAbstractDialog


class EditDialogFactory:
    """Factory class that creates a different type of Edit dialog.

    The dialog made depends on whether there are multiple files being edited, or not.
    """

    def __init__(self, parent: QWidget, repository: SongRepository) -> None:
        """Creates an EditDialogFactory.

        Args:
            parent: The widget the new widget should be created on.
            repository: The list of songs the app is managing.
            all_tags:
        """
        self.parent: QWidget = parent
        self.repository: SongRepository = repository
        "The list of songs that the app is managing"

    def get(
        self,
        rows: list[int],
        all_tags: list[SongTag],
        split_text_entered: str,
        *,
        bulk: bool = False,
    ) -> EditAbstractDialog:
        """Generates an EditAbstractDialog.

        The dialog generated is based on whether multiple files should be edited.

        It is populated with the song metadata that should be editable.

        Args:
            rows: List of indexes in the repository for the songs to edit
            all_tags: Tags that can be viewed and edited.
            split_text_entered: Character used to split multiple values.
            bulk (optional): Whether the songs should be edited in bulk or individually.
                Default False.

        Returns:
            A dialog for editing the metadata, of the correct form.
        """
        if bulk:
            return EditBulkDialog(
                self.parent, self.repository, rows, split_text_entered, all_tags
            )
        return EditDialog(self.parent, self.repository, rows, all_tags)
