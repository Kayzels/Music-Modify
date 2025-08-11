from abc import abstractmethod, ABC
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QWidget

from music_modify.gui.meta import ABCQMeta
from music_modify.models.song_repository import SongRepository


class EditAbstractDialog(QDialog, ABC, metaclass=ABCQMeta):
    info_updated: Signal = Signal()

    def __init__(self, parent: QWidget, repository: SongRepository, rows: list[int]):
        super().__init__(parent)

        self.setModal(True)

        self.repository: SongRepository = repository
        self.rows: list[int] = rows

    def setupUi(self) -> None:
        self.main_layout: QVBoxLayout = QVBoxLayout(self)

        self._setupSongInfo()
        self._setupButtons()

        self.setLayout(self.main_layout)

    @abstractmethod
    def _setupSongInfo(self) -> None:
        pass

    @abstractmethod
    def updateSongInfo(self) -> None:
        pass

    def _setupButtons(self) -> None:
        self.button_box: QDialogButtonBox = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        # noinspection PyTypeChecker
        self.button_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply
        )

        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(
            self.reject
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(
            self.accept
        )

        # Update the song, but keep the dialog open
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self.updateSongInfo
        )

        self.main_layout.addWidget(self.button_box)
