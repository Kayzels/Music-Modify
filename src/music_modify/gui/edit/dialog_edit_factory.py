"""Module that defines an EditDialogFactory.

This is the factory class for creating different types of Edit dialogs.
"""

from typing import ClassVar, TypedDict

from PySide6.QtWidgets import QWidget

from music_modify.custom_types import TagInfo
from music_modify.models.song_repository import SongRepository

from .bulk.dialog_edit_bulk import EditBulkDialog
from .dialog_edit import EditDialog
from .dialog_edit_abstract import EditAbstractDialog


class EditDialogFactory:
    """Factory class that creates a different type of Edit dialog.

    The dialog made depends on whether there are multiple files being edited, or not.
    """

    parent: QWidget | None = None
    "The widget the new widget should be created on."
    repository: SongRepository = SongRepository()
    "The list of songs the app is managing."
    all_tags: ClassVar[list[TagInfo]]
    "Tags that can be viewed and edited."

    @classmethod
    def setDetails(
        cls, parent: QWidget, repository: SongRepository, all_tags: list[TagInfo]
    ) -> None:
        """Set the parent and repository variables for the factory."""
        cls.parent = parent
        cls.repository = repository
        cls.all_tags = all_tags

    @classmethod
    def get(
        cls,
        rows: list[int],
        *,
        bulk: bool = False,
    ) -> EditAbstractDialog:
        """Generates an EditAbstractDialog.

        The dialog generated is based on whether multiple files should be edited.

        It is populated with the song metadata that should be editable.

        Args:
            rows: List of indexes in the repository for the songs to edit
            bulk (optional): Whether the songs should be edited in bulk or individually.
                Default False.

        Returns:
            A dialog for editing the metadata, of the correct form.
        """

        class _DialogArgs(TypedDict):
            repository: SongRepository
            rows: list[int]
            all_tags: list[TagInfo]
            parent: QWidget | None

        dialog_args: _DialogArgs = {
            "repository": cls.repository,
            "rows": rows,
            "all_tags": cls.all_tags,
            "parent": cls.parent,
        }

        if bulk:
            return EditBulkDialog(**dialog_args)
        return EditDialog(**dialog_args)
