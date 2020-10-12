"""Functions that are not module specifc.
    """

import datetime
from functools import wraps
import json
from time import time
from typing import Any, Callable, List

from PyQt5.QtWidgets import QBoxLayout, QTableView, QWidget

from models import SongTableModel
from prefs import settings


def refresh_widget(widget: QWidget):
    """Sets the widget stylesheet to display.

        Parameters
        ----------
        widget : QWidget -
            Widget that the set stylesheet should display for.

        Reason
        ------
        Used because of a bug in Qt where nested widgets don't
        display the set stylesheet when initialised.
        """
    widget_style_sheet = widget.styleSheet()
    widget.setStyleSheet(r"\*")
    widget.setStyleSheet(widget_style_sheet)


def format_time(time_to_format: datetime.timedelta,
                decimal_places: int = 2) -> str:
    """Converts a timedelta to a readable string.

        Parameters
        ----------
        time : datetime.timedelta -
            Timedelta object that should be converted\n
        decimal_places : int, optional -
            Number of decimal places to include for seconds.
            By default 2.

        Returns
        -------
        str -
            String of the form hours, mins, seconds excluding empty fields.
            Seconds formatted to decimal_places decimal places.
        """
    time_string = ""
    hours, mins, seconds = str(time_to_format).split(':')
    # ? timedelta objects look like 0:00:23.456789. Makes this string.
    seconds_split = seconds.split(".")
    seconds = seconds_split[0] + "." + seconds_split[1][:decimal_places]
    if hours == '0':
        if mins == '00':
            time_string = f"{seconds} seconds"
        else:
            time_string = f"{mins} mins, {seconds} seconds"
    else:
        time_string = f"{hours} hours, {mins} mins, {seconds} seconds"
    return time_string


def timing(func: Callable) -> Any:
    """Decorator that is used to time the duration of a function.
        Prints this to the console, with info about the function.
        The duration is formatted to be human readable.

        Parameters
        ----------
        func : Callable) -
            function that is being timed.

        Returns
        -------
        Any -
            Result of the function being timed.
        """
    @wraps(func)
    # ? used so that the function runs normally,
    # ? with proper garbage collection
    def wrap(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        time_taken = format_time(datetime.timedelta(seconds=end - start))
        print(f"Time taken for {func.__name__} is {time_taken}.")
        return result
    return wrap


def jprint(obj: dict):
    """Creates a formatted string of the Python JSON Object

    Parameters
    ----------
    obj : JSON object -
        JSON text to be converted.
    """
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def remove_all_widgets(layout: QBoxLayout,
                       min_count: int = 0):
    """Remove all widgets from the given layout

        Parameters
        ----------
        layout : Union[QBoxLayout, None] -
            Layout that widgets should be removed from.\n
        min_count : int, optional -
            Number of widgets that should remain in the layout, by default 0.
        """
    if layout is not None:
        while layout.count() - min_count:
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                remove_all_widgets(child.layout())


def remove_widget_from_scroll(widget: QWidget,
                              parent_layout: QBoxLayout,
                              data_list: List):
    """Remove a widget from a scroll area, and remove the associated data.

        Parameters
        ----------
        widget : QWidget
            Widget that should be removed
        parent_layout : QBoxLayout
            The layout of the scroll area the widget should be removed from
        data_list : List
            The list of data related to the widgets in this scroll area.

        Information
        -----------
        Only removes the widget and data if there will still be widgets
        in the scroll area after this widget is removed.
        """
    if parent_layout.count() > 2:  # ? 2 instead of 1 because of spacer.
        index = parent_layout.indexOf(widget)
        del data_list[index]
        remove_all_widgets(widget.layout())
        parent_layout.removeWidget(widget)
        widget.deleteLater()


def update_table_view(table_view: QTableView):
    """Updates the appearance of the table view.
        This updates the column width and the stylesheet.
            """
    model = table_view.model()
    if isinstance(model, SongTableModel) and not model.songs:
        return

    for index, tag in enumerate(settings.files_tags):
        if tag.value_length == 1:
            table_view.resizeColumnToContents(index)
        else:
            table_view.setColumnWidth(index, 150)
    refresh_widget(table_view)
