"""Package that contains widgets specifically for completion suggestions
in dropdown menus.
"""

from PySide6.QtWidgets import QWidget

from .widgets_complete import EditWithComplete


def createCompletionWidget(
    parent: QWidget, items: tuple[str, ...], *, multiple: bool = True, initial: str = ""
) -> EditWithComplete:
    """
    Creates a widget for showing completion suggestions,
    that is populated with the items sent through.

    Args:
        parent: The parent widget.
        items: A tuple of strings representing the completion suggestions.
        multiple (optional): Whether multiple selections are allowed. Defaults to True.
        initial (optional): The initial value to display in the widget. Defaults to "".

    Returns:
        EditWithComplete: The configured completion widget.
    """
    widget = EditWithComplete(parent, multiple)
    widget.updateItemsCache(items)
    widget.showInitialValue(initial)
    return widget


__all__ = ["EditWithComplete", "createCompletionWidget"]
