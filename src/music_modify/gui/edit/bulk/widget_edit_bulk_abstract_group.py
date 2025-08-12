"""Module that contains the abstract class that defines all functionality
that widgets that display grouped data should have."""

from abc import ABC, abstractmethod
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGroupBox, QHBoxLayout, QVBoxLayout, QWidget

from music_modify.custom_types import SongTag

from .widget_edit_bulk_abstract import EditBulkAbstractWidget


class EditBulkAbstractGroupWidget(EditBulkAbstractWidget, ABC):
    def __init__(self, parent: QWidget, tag: SongTag) -> None:
        super().__init__(parent, tag)

        self.group_box: QGroupBox
        "The checkable box that the widget should be contained in."
        self.clear_checkbox: QCheckBox
        "A checkbox that, when checked, clears the data."
        self.form_container: QWidget
        "The container that holds the form that holds the main widget."

    @override
    def setupUi(self) -> None:
        self.group_box = QGroupBox(self.tag.display_name)
        group_layout = QVBoxLayout()
        self.group_box.setCheckable(True)
        self.group_box.setLayout(group_layout)
        # Have the group disabled by default
        self.group_box.setChecked(False)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.clear_checkbox = QCheckBox("Clear")
        self.clear_checkbox.stateChanged.connect(self._toggleClearState)
        group_layout.addWidget(self.clear_checkbox)

        self.form_container = self.createForm()
        group_layout.addWidget(self.form_container)

        main_layout.addWidget(self.group_box)
        self.setLayout(main_layout)

    @abstractmethod
    def createForm(self) -> QWidget:
        """Creates the form layout that holds the widgets needed."""
        pass

    def _toggleClearState(self, state: Qt.CheckState) -> None:
        """Toggle whether the data should be cleared on confirm, or not."""
        self.form_container.setEnabled(state == Qt.CheckState.Unchecked.value)

    @abstractmethod
    def _resetView(self) -> None:
        """Resets the display to be the same as it was on initialisation."""
        pass
