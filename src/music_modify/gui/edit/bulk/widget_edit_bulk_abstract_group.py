from abc import abstractmethod, ABC
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGroupBox, QHBoxLayout, QVBoxLayout, QWidget
from music_modify.custom_types import SongTag

from .widget_edit_bulk_abstract import EditBulkAbstractWidget


class EditBulkAbstractGroupWidget(EditBulkAbstractWidget, ABC):
    def __init__(self, parent: QWidget, tag: SongTag):
        super().__init__(parent, tag)

        self.group_box: QGroupBox
        self.clear_checkbox: QCheckBox
        self.form_container: QWidget

    @override
    def setupUi(self):
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
        pass

    def _toggleClearState(self, state: Qt.CheckState):
        self.form_container.setEnabled(state == Qt.CheckState.Unchecked.value)

    @abstractmethod
    def _resetView(self) -> None:
        pass
