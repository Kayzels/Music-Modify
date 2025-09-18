"""Module that defines an EditAbstractDialog.

This dialog is used for editing metadata,
and defines the general functionality all child dialogs should have.
"""

from abc import ABC, abstractmethod

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QWidget

from music_modify.core.meta import ABCQMeta
from music_modify.models.song_repository import SongRepository


class EditAbstractDialog(QDialog, ABC, metaclass=ABCQMeta):
    """Defines the general functionality for dialogs used to edit metadata."""

    info_updated: Signal = Signal(list)
    """Signal that is emitted whenever any value being displayed
    for the song is changed. Should emit a list of the repo indexes as ints."""

    def __init__(
        self,
        repository: SongRepository,
        rows: list[int],
        parent: QWidget | None = None,
    ) -> None:
        """Creates an EditAbstractDialog.

        Args:
            parent: The widget that this dialog should be displayed on.
            repository: The list of songs that is being managed.
            rows: The indexes of the songs in the `repository` that should be edited.
        """
        super().__init__(parent)

        self.setModal(True)

        if len(rows) == 0:
            self.reject()
            return
        self.repository: SongRepository = repository
        "The list of songs that is currently being managed."
        self.rows: list[int] = rows
        "The indexes of the songs to edit, from the repository."

    def setupUi(self) -> None:
        """Sets up the basic user interface for the dialog."""
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        "The layout that all child widgets should be contained in."

        self._setupSongInfo()
        self._setupButtons()

        self.setLayout(self.main_layout)

    @abstractmethod
    def _setupSongInfo(self) -> None:
        """Set up the display of the information for the songs."""

    @abstractmethod
    def updateSongInfo(self) -> None:
        """Update the data being stored in the song(s)."""

    def _setupButtons(self) -> None:
        """Add the buttons to the interface."""
        self.button_box: QDialogButtonBox = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        # noinspection PyTypeChecker
        self.button_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply,
        )

        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(
            self.reject,
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(
            self.accept,
        )

        # Update the song, but keep the dialog open
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self.updateSongInfo,
        )

        self.main_layout.addWidget(self.button_box)
