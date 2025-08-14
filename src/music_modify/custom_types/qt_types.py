"""Module that defines some types needed for Qt."""

from typing import TypedDict

from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QLineEdit

Q_MODEL_INDEX = QModelIndex()


class QLineEditArgs(TypedDict, total=False):
    """The argument types that can be used when initialising a QLineEdit."""

    inputMask: str | None
    text: str | None
    maxLength: int | None
    frame: bool | None
    echoMode: QLineEdit.EchoMode | None
    displayText: str | None
    cursorPosition: int | None
    alignment: Qt.AlignmentFlag | None
    modified: bool | None
    hasSelectedText: bool | None
    selectedText: str | None
    dragEnabled: bool | None
    readOnly: bool | None
    undoAvailable: bool | None
    redoAvailable: bool | None
    acceptableInput: bool | None
    placeholderText: str | None
    cursorMoveStyle: Qt.CursorMoveStyle | None
    clearButtonEnabled: bool | None
