"""Module that defines a dialog that displays a way for remapping a name in all tags."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)


class DialogRemap(QDialog):
    """Dialog that displays a way for remapping a name in all tags."""

    def __init__(self, /, parent: QWidget | None = None) -> None:
        """Creates a dialog for remapping names in all tags."""
        super().__init__(parent)
        self.setModal(True)
        self.setupUi()

    def setupUi(self) -> None:
        """Sets up the basic user interface for the dialog."""
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.addRow("Original Name", QLineEdit(self))
        form_layout.addRow("New Name", QLineEdit(self))

        main_layout.addLayout(form_layout)

        button_box = QDialogButtonBox(self)
        button_box.setOrientation(Qt.Orientation.Horizontal)
        button_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        button_box.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(
            self.accept
        )
        button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(
            self.reject
        )

        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def updateSongs(self) -> None:
        """Update the selected songs to remap the values."""
        # TODO: Get Person tags from Settings
        # TODO: Iterate through Songs
        # TODO: Iterate through tags
        # TODO: Handle TagValue types
        # TODO: Update model
