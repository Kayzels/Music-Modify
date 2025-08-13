from typing import TypedDict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit


class QLineEditArgs(TypedDict, total=False):
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
