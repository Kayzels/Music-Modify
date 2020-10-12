"""Module for the tables allowing input in an action widget
    """
from typing import Tuple, TYPE_CHECKING, Union

from PyQt5.QtWidgets import QPushButton, QTableWidgetItem

from utils.enums import InputWidget, ValuesTableType

if TYPE_CHECKING:
    from jobs.job_dialog import ActionWidget


def create_values_table(action_widget: 'ActionWidget',
                        table_type: ValuesTableType,
                        current_type: Union[ValuesTableType, None] = None):
    """Create a values table of the specified type

        Parameters
        ----------
        action_widget : ActionWidget -
            The widget containing the values table.\n
        table_type : ValuesTableType -
            The type of values table to be created.\n
        current_type : Union[ValuesTableType, None], optional -
            The type of the values table that is currently there.
            By default None
        """
    if current_type != table_type and table_type != InputWidget.CopyTable:
        action_widget.newValuesTableWidget.clearContents()
    if table_type == ValuesTableType.Standard:
        _create_standard_table(action_widget)
    elif table_type == ValuesTableType.Replace:
        _create_replace_table(action_widget)
    elif table_type == InputWidget.CopyTable:
        _create_copy_table(action_widget)
    action_widget.table_type = table_type


def _create_standard_table(action_widget: 'ActionWidget'):
    """Create a values table with the number of columns
        necessary based on the selected tag

        Parameters
        ----------
        action_widget : ActionWidget -
            The widget that should show the table
        """
    if action_widget.created_action.tags is None:  # type: ignore
        return
    tags = [tag.tag for tag
            in action_widget.created_action.tags  # type: ignore
            if tag.tag is not None]
    column_counts = [tag.value_length for tag in tags]
    if not column_counts.count(column_counts[0]) == len(column_counts):
        incompatible_string = "Selected Tags Are Incompatible \
            for this Action."
        action_widget.newValuesTableWidget.clearContents()
        action_widget.newValuesTableWidget.setColumnCount(1)
        action_widget.newValuesTableWidget.setRowCount(0)
        action_widget.newValuesTableWidget\
            .setHorizontalHeaderLabels([incompatible_string])
        action_widget.newValuesTableWidget\
            .horizontalHeader().setStretchLastSection(True)
        action_widget.created_action.values = None  # type: ignore
        return
    else:
        column_count = column_counts[0]
        if action_widget.newValuesTableWidget.columnCount()\
                != column_count + 2:  # ? +2 included for add buttons
            action_widget.newValuesTableWidget\
                .setColumnCount(column_count + 2)
        action_widget.newValuesTableWidget\
            .setHorizontalHeaderItem(0, QTableWidgetItem(''))
        action_widget.newValuesTableWidget\
            .setHorizontalHeaderItem(1, QTableWidgetItem(''))
        if column_count == 1:
            join_string = ', '
            tags_string = ''
            for tag in action_widget.created_action.tags:  # type: ignore
                if tag.tag is not None:
                    tags_string = f"{tags_string}\
                        {tag.tag.display_name}{join_string}"
            tags_string = tags_string.rstrip(join_string)
            action_widget.newValuesTableWidget\
                .setHorizontalHeaderItem(2, QTableWidgetItem(tags_string))
        elif column_count == 2:
            action_widget.newValuesTableWidget\
                .setHorizontalHeaderItem(2, QTableWidgetItem('Role'))
            action_widget.newValuesTableWidget\
                .setHorizontalHeaderItem(3, QTableWidgetItem('Performer'))
            full_width = action_widget.newValuesTableWidget.columnWidth(2)\
                + action_widget.newValuesTableWidget.columnWidth(3)
            action_widget.newValuesTableWidget\
                .setColumnWidth(2, int(full_width / 2))
            action_widget.newValuesTableWidget\
                .setColumnWidth(3, int(full_width / 2))
        if action_widget.newValuesTableWidget.rowCount() < 5:
            action_widget.newValuesTableWidget.setRowCount(5)
        for row in range(action_widget.newValuesTableWidget.rowCount()):
            _add_row_buttons(action_widget, row)


def _add_row_buttons(action_widget: 'ActionWidget', row: int):
    """Create row buttons and add them to the table

        Parameters
        ----------
        action_widget : ActionWidget
            [description]
        row : int
            [description]
        """
    add_button, remove_button = _create_buttons(action_widget)
    _set_buttons_in_cells(action_widget, row, add_button, remove_button)


def _create_buttons(action_widget: 'ActionWidget')\
        -> Tuple[QPushButton, QPushButton]:
    """Create buttons to allow rows to be added and removed.

    Parameters
    ----------
    action_widget : ActionWidget -
        The widget the table should be added to.

    Returns
    -------
    Tuple[QPushButton, QPushButton] -
        Button to add rows, Button to remove.
    """
    add_button = QPushButton(action_widget.newValuesTableWidget)
    remove_button = QPushButton(action_widget.newValuesTableWidget)
    style_sheet_both = (""
                        "QPushButton {"
                        "border-width: 2px;"
                        "border-style: outset;"
                        "border-radius:9px;"
                        "margin: 1px"
                        "}"
                        "QPushButton:pressed {"
                        "border-style:inset"
                        "}"
                        )
    style_sheet_add = (""
                       "QPushButton {"
                       "border-color:green;"
                       "background: lightgreen;"
                       "color: green;"
                       "}"
                       "QPushButton:pressed {"
                       "background: limegreen;"
                       "}"
                       )
    style_sheet_remove = (""
                          "QPushButton {"
                          "border-color:red;"
                          "background: pink;"
                          "color: darkred;"
                          "}"
                          "QPushButton:pressed {"
                          "background: rgb(255, 160, 180);"
                          "}"
                          )
    add_button.setText("+")
    add_button.resize(32, 32)
    add_button.setMinimumWidth(32)
    remove_button.setText("-")
    remove_button.resize(32, 32)
    remove_button.setMinimumWidth(32)
    add_button.setStyleSheet(style_sheet_both + style_sheet_add)
    remove_button.setStyleSheet(style_sheet_both + style_sheet_remove)
    add_button.clicked.connect(lambda: add_row(action_widget))
    remove_button.clicked.connect(lambda: clear_row(action_widget))
    return add_button, remove_button


def _set_buttons_in_cells(action_widget: 'ActionWidget',
                          row: int,
                          add_button: QPushButton,
                          remove_button: QPushButton):
    """Place the created buttons in the cells related to the specific row.

        Parameters
        ----------
        action_widget : ActionWidget -
            Widget the table should be added to.\n
        row : int -
            The row where the buttons should be placed.\n
        add_button : QPushButton -
            Button for adding a row under this row.\n
        remove_button : QPushButton -
            Button to remove this row.\n
        """
    action_widget.newValuesTableWidget.setCellWidget(row, 0, add_button)
    action_widget.newValuesTableWidget.setCellWidget(row, 1, remove_button)
    action_widget.newValuesTableWidget.setColumnWidth(0, 32)
    action_widget.newValuesTableWidget.setColumnWidth(1, 32)


def add_row(action_widget: 'ActionWidget'):
    """Add a row to the values table.

        Parameters
        ----------
        action_widget : ActionWidget -
            Widget containing the values table.
    """
    button: QPushButton = action_widget.sender()
    row = action_widget.newValuesTableWidget.indexAt(button.pos()).row()
    action_widget.newValuesTableWidget.insertRow(row + 1)
    _add_row_buttons(action_widget, row + 1)


def clear_row(action_widget: 'ActionWidget'):
    """Remove a row from the values table.

        Parameters
        ----------
        action_widget : ActionWidget -
            Widget containing the values table.
        """
    button: QPushButton = action_widget.sender()
    row = action_widget.newValuesTableWidget.indexAt(button.pos()).row()
    if action_widget.newValuesTableWidget.rowCount() > 1:
        action_widget.newValuesTableWidget.removeRow(row)
        action_widget.activate_update_table_values()


def _create_replace_table(action_widget: 'ActionWidget'):
    """Create a values table with two columns,
        one for original values and one for the new values.

        Parameters
        ----------
        action_widget : ActionWidget -
            Widget containing the Values Table
        """
    action_widget.newValuesTableWidget.setColumnCount(4)
    headers = ['', '', 'Original Value', 'New Value']
    action_widget.newValuesTableWidget.setHorizontalHeaderLabels(headers)
    full_width = action_widget.newValuesTableWidget.columnWidth(2)\
        + action_widget.newValuesTableWidget.columnWidth(3)
    action_widget.newValuesTableWidget\
        .setColumnWidth(2, int(full_width / 2))
    action_widget.newValuesTableWidget\
        .setColumnWidth(3, int(full_width / 2))
    if action_widget.newValuesTableWidget.rowCount() < 5:
        action_widget.newValuesTableWidget.setRowCount(5)
    for row in range(action_widget.newValuesTableWidget.rowCount()):
        _add_row_buttons(action_widget, row)


def _create_copy_table(action_widget: 'ActionWidget'):
    """Creates a copy table with the same number of rows
        as the model row count.

        Parameters
        ----------
        action_widget : ActionWidget
            Widget containing the copy table.
        """
    action_widget.copyTableIndexesTableWidget.clear()
    action_widget.copyTableIndexesTableWidget.setRowCount(0)
    action_widget.copyTableIndexesTableWidget\
        .setRowCount(action_widget.copyTableSelectedSongs.model().rowCount())
    action_widget.copyTableIndexesTableWidget.setColumnCount(1)
    action_widget.copyTableIndexesTableWidget\
        .setHorizontalHeaderLabels(['Copy To'])
