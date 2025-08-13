"""Module that defines an abstract dialog for editing metadata,
which defines the general functionality all child dialogs should have."""

from abc import ABC, abstractmethod

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QWidget

from music_modify.gui.meta import ABCQMeta
from music_modify.models.song_repository import SongRepository


class EditAbstractDialog(QDialog, ABC, metaclass=ABCQMeta):
    """An abstract class that defines the general functionality
    that all dialogs that are used for editing metadata should have."""

    info_updated: Signal = Signal()
    """Signal that is emitted whenever any value being displayed
    for the song is changed."""

    def __init__(
        self,
        parent: QWidget,
        repository: SongRepository,
        rows: list[int],
    ) -> None:
        super().__init__(parent)

        self.setModal(True)

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
