from PySide6.QtWidgets import QWidget
from .widgets_complete import EditWithComplete


def createCompletionWidget(
    parent: QWidget, items: tuple[str, ...], multiple: bool = True, initial: str = ""
) -> EditWithComplete:
    widget = EditWithComplete(parent, multiple)
    widget.updateItemsCache(items)
    widget.showInitialValue(initial)
    return widget


__all__ = ["EditWithComplete", "createCompletionWidget"]
