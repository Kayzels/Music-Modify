"""Module for the dialog that is shown to create a job
    """
# pylint: disable=too-many-lines
# region Python Imports
from functools import partial
from typing import cast, List, Union
# endregion
# region PyQt Imports
from PyQt5 import sip
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtWidgets import QComboBox, QDialog, QListView, QMainWindow,\
    QMenu, QScrollBar, QTableWidgetItem, QWidget
# endregion
# region Custom Imports
import requests
# endregion
# region Ui Imports
from gui.dialog_job import Ui_JobDialog
from gui.widget_action import Ui_actionWidget_Main as Ui_actionWidget
from gui.widget_tag import Ui_tagWidget
# endregion
# region Project Imports
from actions import ActionToCreate, download_discogs, function_mappings
from actions.actions import copy_values
from jobs import values_table
from models import SongTableModel, SongTableProxyModel
from prefs import settings
from songs import FileSelectionDialog, SelectedTag
from utils import util_functions as util_f
from utils.enums import ActionType, ChangeSelectionType, InputWidget,\
    InfoType, SaveState, ScrollBarSlotType, ValuesTableType
# endregion


# region Scrollbars
def set_scrollbar_value(value: int,
                        slot_scrollbar: QScrollBar,
                        signal_scrollbar: QScrollBar,
                        ):
    """Set the value on the slot scrollbar
        to be the value on the signal scrollbar.

        Parameters
        ----------
        value : int -
            The value on the scrollbar.\n
        slot_scrollbar : QScrollBar -
            The scrollbar that should be changed.\n
        signal_scrollbar : QScrollBar -
            The scrollbar that sends the value to be changed.\n
        """
    if value == signal_scrollbar.maximum():
        slot_scrollbar.setValue(slot_scrollbar.maximum())
    else:
        slot_scrollbar.setValue(value)


def set_scrollbar_changed_range(range_min: int,
                                range_max: int,
                                slot_scrollbar: QScrollBar,
                                ):
    """Set the range of the slot scrollbar to (min, max).

        Parameters
        ----------
        range_min : int -
            Minimum of the range\n
        range_max : int -
            Maximum of the range\n
        slot_scrollbar : QScrollBar -
            The scrollbar whose range should change\n
        """
    slot_scrollbar.setRange(range_min, range_max)
# endregion


class TagWidget (QWidget, Ui_tagWidget):
    """Widget that is used for selecting which tags should be edited.
        """
    def __init__(self,
                 parent: QWidget,
                 parent_action_widget: 'ActionWidget'):
        """Constructor for TagWidget.

            Parameters
            ----------
            parent : QWidget -
                The parent of this widget,
                i.e. where this widget should be placed.\n
            parent_action_widget : ActionWidget -
                The action widget that contains the scroll area of tag widgets.
            """
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.parent_action_widget = parent_action_widget
        self.created_action = parent_action_widget\
            .created_action  # type: ignore
        self.created_action = cast(ActionToCreate, self.created_action)
        if self.created_action.tags is None:
            self.created_action.tags = []

        self.tags = settings.standard_tags + settings.custom_tags
        self.tag_names = [tag.display_name for tag in self.tags]
        for combobox in (self.tagsComboBox, self.copyTagsComboBox):
            combobox.addItems(self.tag_names)
            list_view = QListView()
            combobox.setView(list_view)
            util_f.refresh_widget(combobox)
            combobox.currentIndexChanged.connect(self.set_tag_selection)

        self.display_role_widget(False)

        self.addButton.clicked.connect(self.add_tag_widget)
        self.removeButton.clicked.connect(self.remove_tag_widget)

        self.roleLineEdit.editingFinished.connect(self.set_tag_role)

    def set_tag_selection(self, index: int):
        """Sets which tags have been selected based on the index
            in the combobox

            Parameters
            ----------
            index : int
                The index where the tag is selected.
            """
        tag_index = self.parentWidget().layout().indexOf(self)
        tag = self.tags[index - 1] if index > 0 else None
        combobox: QComboBox = self.sender()
        combobox = cast(QComboBox, combobox)
        if combobox == self.tagsComboBox:
            self.created_action.tags[tag_index].tag = tag
        elif combobox == self.copyTagsComboBox:
            self.created_action.tags[tag_index].copy_tag = tag
        self.display_role_widget()
        self.parent_action_widget.display_selected_tags()
        self.parent_action_widget.setup_values_table()

    def add_tag_widget(self):
        """Add another tag widget to the scroll area.
            """
        index = self.parentWidget().layout().indexOf(self)
        self.parent_action_widget.create_tag_widget(index + 1)

    def remove_tag_widget(self):
        """Remove this tag widget from the scroll area.
            """
        self.parent_action_widget.remove_tag_widget(self)

    def add_tag_to_created_action(self):
        """Add the information selected to the created action
            of the action widget
        """
        tag_index = self.parentWidget().layout().indexOf(self)
        self.created_action.tags.insert(tag_index, SelectedTag())

    def set_tag_role(self):
        """Set the role in the tag to the text in the role line edit.
            """
        tag_index = self.parentWidget().layout().indexOf(self)
        self.created_action.tags[tag_index].role = self.roleLineEdit.text()

    def display_role_widget(self, toggled: Union[bool, None] = None):
        """Display the role widget if necessary

            Parameters
            ----------
            toggled : Union[bool, None], optional -
                Whether the role should be shown, by default None.

            Info
            ----
            If a bool is not sent, checks whether the copy tag and tag
            are compatible.\n
            Displays the role widget if they are incompatible.
            """
        tag_index = self.parentWidget().layout().indexOf(self)
        if toggled is not None:
            self.roleWidget.setVisible(toggled)
            return
        copy_tag = self.created_action.tags[tag_index].copy_tag
        tag = self.created_action.tags[tag_index].tag
        if copy_tag is not None and tag is not None:
            if copy_tag.value_length == 1 and tag.value_length == 2:
                self.created_action.tags[tag_index].role = 'instruments'
                self.roleWidget.show()
            else:
                self.created_action.tags[tag_index].role = None
                self.roleWidget.hide()


class ActionWidget(QWidget, Ui_actionWidget):
    """Widget used for selecting which actions should be performed.
        """
    def __init__(self, parent: QWidget, parent_dialog: 'JobDialog'):
        """Constructor for Action Widget.

            Parameters
            ----------
            parent : QWidget -
                Which widget should contain this widget.\n
            parent_dialog : JobDialog -
                The dialog the widget is shown in.
            """
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.created_action = ActionToCreate(parent_dialog.song_proxy_model)
        self.parent_dialog = parent_dialog

        self.table_type: Union[ValuesTableType, None] = None

        # region Refresh Widgets
        for widget in (self.newValuesTableWidget,
                       self.selectedSongsTableView,
                       self.discogsTableWidget,
                       self.discogsSelectedSongsTableView):
            util_f.refresh_widget(widget)
        # ! check - hasn't been initialised, so might not work.
        # endregion

        # region Actions Combo Box
        self.actions_list = list(function_mappings.keys())
        self.actionsComboBox.addItems(self.actions_list)
        self.actionsComboBox.currentIndexChanged.connect(
            self.set_selected_action)
        combobox_view = QListView()
        self.actionsComboBox.setView(combobox_view)
        util_f.refresh_widget(self.actionsComboBox)
        # endregion

        # region Selected Songs
        proxy_model_indexes = parent_dialog.song_proxy_model.model_indexes
        proxy_model = SongTableProxyModel()
        proxy_model.setSourceModel(self.parent_dialog.original_model)
        proxy_model.change_model_indexes(proxy_model_indexes)
        self.song_proxy_model = proxy_model

        self.selectedSongsTableView.setModel(self.song_proxy_model)
        self.copyTableSelectedSongs.setModel(self.song_proxy_model)
        self.discogsSelectedSongsTableView.setModel(self.song_proxy_model)
        self.songCount.setText(f"{self.song_proxy_model.rowCount()}")
        # endregion

        for table_view in (self.selectedSongsTableView,
                           self.discogsSelectedSongsTableView,
                           self.copyTableSelectedSongs):
            util_f.update_table_view(table_view)
        # region Selected Songs Menu
        selection_menu = QMenu(self.changeSelectedSongsButton)
        for action in (self.actionCurrentSelection,
                       self.actionGlobalSongs,
                       self.actionOriginalSelection):
            selection_menu.addAction(action)
        self.changeSelectedSongsButton.setMenu(selection_menu)
        self.actionGlobalSongs.triggered.connect(
            lambda: self.change_selected_songs(ChangeSelectionType.Global))
        self.actionCurrentSelection.triggered.connect(
            lambda: self.change_selected_songs(ChangeSelectionType.Current))
        self.actionOriginalSelection.triggered.connect(
            lambda: self.change_selected_songs(ChangeSelectionType.Original))
        self.changeSelectedSongsButton.menu().aboutToShow.connect(
            lambda: self.changeSelectedSongsButton.menu().setMinimumWidth(
                self.changeSelectedSongsButton.width()))
        # endregion

        # region Action Edit Buttons
        self.addAnotherActionButton.clicked.connect(
            self.create_new_action)
        self.removeActionPushButton.clicked.connect(
            self.remove_this_action)
        # endregion

        # region Discogs Release Widgets
        self.releaseIDLineEdit.textChanged.connect(
            lambda _: self.downloadReleaseButton.setEnabled(
                self.releaseIDLineEdit.hasAcceptableInput()))
        self.downloadReleaseButton.clicked.connect(
            self.get_and_display_discogs_release)
        self.discogsTableWidget.cellChanged.connect(
            self.map_discogs_indexes)
        # endregion

        # region Values and Copy Table Signal Connections
        self.saveValuesButton.clicked.connect(
            self.save_table_values)
        self.newValuesTableWidget.cellChanged.connect(
            self.activate_update_table_values)
        self.saveCopyValuesButton.clicked.connect(
            self.save_copy_table_values)
        self.copyTableIndexesTableWidget.cellChanged.connect(
            self.activate_update_copy_values)
        # endregion

        # region Sync Text
        # text_edits = self.actionInfo, self.actionInfo_Main,\
        #     self.tagInfo, self.tagInfo_Main
        text_edit_tuple = ((self.actionInfo, InfoType.Action),
                           (self.tagInfo, InfoType.Tag))
        for text_edit, info_type in text_edit_tuple:
            text_edit.textChanged.connect(
                partial(self.set_info_text, info_type))
        # endregion

        # region Syncing Discogs
        self.scrollbar_partials: List[partial] = []
        self.autoMapButton.clicked.connect(self.auto_map_discogs_release)
        self.syncButton.toggled.connect(self.sync_discogs_scrollbar)
        # endregion

        self.songsCustomName.textChanged.connect(self.set_songs_custom_name)
        self.valuesCustomName.textChanged.connect(self.set_values_custom_name)

        self.link_scrollbars(self.copyTableIndexesTableWidget
                             .verticalScrollBar(),
                             self.copyTableSelectedSongs.verticalScrollBar(),
                             hide=True)

        self.set_start_state()

    # region Sync Text
    def set_info_text(self, info_type: InfoType):
        """Sync the text from the info panel to the main info panel.

            Parameters
            ----------
            text : str -
                Text that should be synced.\n
            info_type : InfoType -
                The type of info widget being edited.
            """
        if info_type == InfoType.Action:
            main_widget = self.actionInfo_Main
            info_widget = self.actionInfo
        elif info_type == InfoType.Tag:
            main_widget = self.tagInfo_Main
            info_widget = self.tagInfo
        else:
            return
        main_widget.setHtml(info_widget.toHtml())
        if info_widget == self.tagInfo:
            self.created_action.tags_display = info_widget.toHtml()
        # if not info_widget.toHtml() == text:
        #     info_widget.setHtml(text)
        # if not main_widget.toHtml() == text:
        #     main_widget.setHtml(text)
    # endregion

    # region Set States
    def set_start_state(self):
        """Set the way the action widget should appear at the start.
        """
        self.set_default_state()
        self.displaySelectedSongsButton.setChecked(False)
        self.discogsVerticalScrollBar.hide()
        self.selectedSongsVerticalScrollBar.hide()
        self.syncWidget.hide()

    def clear_manual_action_info(self):
        """Remove the information related to a manual action from the
            created action.
            """
        self.created_action.tags = None
        self.tagInfo.setText("No Tags")
        self.created_action.values = None
        self.created_action.copy_mappings = None
        util_f.remove_all_widgets(self.tagsScrollAreaContentsVerticalLayout,
                                  min_count=1)
        self.tagsSummary.setVisible(False)
        self.tagInfo.setVisible(False)
        self.tagsScrollArea.setVisible(False)
        self.valuesSummary.setVisible(False)
        self.tableValuesFrame.setVisible(False)
        self.copyTableFrame.setVisible(False)
        self.table_type = None
        self.display_values_table(False)

    def clear_download_action_info(self):
        """Remove the information related to a download action from the
            created action.
            """
        self.created_action.mappings = None
        self.created_action.response = None
        self.releaseIDLineEdit.clear()

        self.discogsTableWidget.clear()
        self.discogsTableWidget.reset()
        self.discogsTableWidget.setColumnCount(0)
        self.discogsTableWidget.setRowCount(0)

        self.discogsReleaseFrame.setVisible(False)
        self.discogsSummary.setVisible(False)

    def set_default_state(self):
        """Clear the existing data and set to a neutral state.
            """
        self.clear_manual_action_info()
        self.clear_download_action_info()

    def setup_manual_action(self):
        """Setup the widgets and containers needed to create a manual action.
            """
        self.clear_download_action_info()
        self.tagsSummary.setVisible(True)
        self.tagInfo.setVisible(True)
        self.tagsScrollArea.setVisible(True)

        if self.tagsScrollAreaContentsVerticalLayout.count() < 2:
            self.create_tag_widget()

        function = function_mappings[self.created_action.action]
        if function.function.__name__ == copy_values.__name__:
            tags_count = self.tagsScrollAreaContentsVerticalLayout.count() - 1
            tag_widgets = [self.tagsScrollAreaContentsVerticalLayout
                           .itemAt(i).widget() for i in range(tags_count)]
            tag_widget: TagWidget
            for tag_widget in tag_widgets:
                tag_widget.copyTagsComboBox.show()

        self.setup_values_table()

    def setup_download_action(self):
        """Setup the widgets and containers needed to create a
            download action.
            """
        self.clear_manual_action_info()
        function = function_mappings[self.created_action.action]
        if function.input_type == InputWidget.DiscogsTable:
            self.discogsReleaseID_Main.show()
            self._create_discogs_selected_songs()
            self.link_scrollbars(self.discogsSelectedSongsTableView
                                 .verticalScrollBar(),
                                 self.selectedSongsVerticalScrollBar)
        else:
            self.discogsReleaseFrame.setVisible(False)
            self.created_action.mappings = None
            self.discogsTableWidget.clear()
            self.discogsTableHLayout.reset()
            self.discogsTableWidget.setColumnCount(0)
            self.discogsTableWidget.setRowCount(0)
            self.created_action.response = None
    # endregion

    # region Setting Action Info
    def set_selected_action(self, index: int):
        """Set the action that should be performed.
            Adds this to the created attribute of the Action Widget.

            Parameters
            ----------
            index : int -
                The index of the action in the combobox
                that should be performed.
            """
        if index > 0:
            action = self.actionsComboBox.itemText(index)
            self.created_action.action = action
            self.actionInfo.setText(action)
        else:
            self.created_action.action = None
            self.actionInfo.setText("No Action")
            self.set_default_state()
            return
        try:
            if self.created_action.action is None:
                self.set_default_state()
                return
            function = function_mappings[self.created_action.action]
        except KeyError:
            self.set_default_state()
            return
        if function.action_type == ActionType.Manual:
            self.setup_manual_action()
        elif function.action_type in (ActionType.Download, ActionType.Excel):
            self.setup_download_action()
        else:
            self.set_default_state()

    def change_selected_songs(self, selection_type: ChangeSelectionType):
        """Change which songs the action should be performed on. \n
            Creates a dialog with the selection type for a user to change
            the songs.

            Parameters
            ----------
            selection_type : ChangeSelectionType -
                The list of songs that should be shown
                for selection in the created dialog.
        """
        if selection_type == ChangeSelectionType.Global:
            model = self.parent_dialog.original_model
        elif selection_type == ChangeSelectionType.Original:
            model = self.parent_dialog.song_proxy_model
        elif selection_type == ChangeSelectionType.Current:
            model = self.song_proxy_model
        else:
            return
        selection_dialog = FileSelectionDialog(self, model)
        util_f.refresh_widget(selection_dialog.changeSelectionTableView)
        if selection_dialog.exec_():
            new_selection = selection_dialog.selection
            self.song_proxy_model.change_model_indexes(new_selection)
            self.songCount.setText(f"{self.song_proxy_model.rowCount()}")
            if self.copyTableFrame.isVisible():
                values_table.create_values_table(self,
                                                 ValuesTableType.Copy,
                                                 None)
                self.link_scrollbars(self.copyTableIndexesTableWidget
                                     .verticalScrollBar(),
                                     self.copyTableSelectedSongs
                                     .verticalScrollBar(),
                                     hide=True)
                self.created_action.copy_mappings = []
                self._set_save_state(SaveState.Unsaved, InputWidget.CopyTable)
            elif self.discogsReleaseFrame.isVisible():
                self._create_discogs_selected_songs()
                self.link_scrollbars(self.discogsSelectedSongsTableView
                                     .verticalScrollBar(),
                                     self.selectedSongsVerticalScrollBar)
                if self.discogsTableWidget.rowCount() > 0:
                    self.created_action.mappings = []
                    for row in range(self.discogsTableWidget.rowCount()):
                        self.created_action.mappings.append(None)
                        current_widget_item: QTableWidgetItem =\
                            self.discogsTableWidget.takeItem(row, 0)
                        sip.delete(current_widget_item)
                    self.allow_scrollbar_sync()
                self._set_save_state(SaveState.Unsaved,
                                     InputWidget.DiscogsTable)

    # region Tag Widgets
    def create_tag_widget(self, index: int = 0):
        """Generate a new Tag Widget and add to the Tag Scroll Area
            at the index sent.

            Parameters
            ----------
            index : int, optional -
                Where in the scroll area the new tag widget should be added.
                By default 0.
            """
        tag_widget = TagWidget(self.tagsScrollAreaWidgetContents, self)
        self.tagsScrollAreaContentsVerticalLayout\
            .insertWidget(index, tag_widget)
        tag_widget.add_tag_to_created_action()
        if self.created_action.action is None:
            self.copyTagsComboBox.hide()
        else:
            function = function_mappings[self.created_action.action]
            tag_widget.copyTagsComboBox.setVisible(function.function.__name__
                                                   == copy_values
                                                   .__name__)
        self.display_selected_tags()

    def display_selected_tags(self):
        """Show which tags have been selected in the tag info box.
            """
        self.tagInfo.clear()
        if not self.created_action.tags or\
                (len(self.created_action.tags) == 1
                    and self.created_action.tags[0].tag is None):
            self.tagInfo.setText("No Tags")
            return
        # if self.created_action.tags is None\
        #         or len(self.created_action.tags) == 0:
        #     self.tagInfo.setText("No Tags")
        #     self.created_action.tags_display = self.tagInfo.toHtml()
        #     return
        # elif len(self.created_action.tags) == 1:
        #     tag = self.created_action.tags[0].tag
        #     if tag is None:
        #         self.tagInfo.setText("No Tags")
        #         return
        for index, tag_selection in enumerate(self.created_action.tags):
            tag_selection = cast(SelectedTag, tag_selection)
            tag = tag_selection.tag
            copy_tag = tag_selection.copy_tag
            tag_shown = '' if tag is None\
                else f"\n\t{tag.display_name} [{tag.name}]"
            copy_tag_shown = '' if copy_tag is None\
                else f"\n\t{copy_tag.display_name} [{copy_tag.name}]"
            new_text = f"Tag {index + 1}:{tag_shown}{copy_tag_shown}"
            self.tagInfo.append(new_text)

    def remove_tag_widget(self, tag_widget: TagWidget):
        """Remove the tag widget sent in from the scroll area.

            Parameters
            ----------
            tag_widget : TagWidget
                The tag widget that should be removed.
            """
        parent_layout = self.tagsScrollAreaContentsVerticalLayout
        util_f.remove_widget_from_scroll(tag_widget,
                                         parent_layout,
                                         self.created_action
                                         .tags)  # type: ignore
        self.display_selected_tags()
    # endregion

    # endregion

    # region Action List Edit
    def create_new_action(self):
        """Create a new Action Widget and add to the parent widget.
            """
        current_index = self.parentWidget().layout().indexOf(self)
        self.parent_dialog.create_action_widget(current_index + 1)

    def remove_this_action(self):
        """Remove this action widget from the parent widget.
        """
        self.parent_dialog.remove_action_widget(self)
    # endregion

    # region Discogs
    def _get_discogs_release(self):
        """Get the response from a discogs release
            and add to the created action attribute.
            """
        release_id = self.releaseIDLineEdit.text()
        response = download_discogs.get_discogs_data(release_id)
        response = cast(requests.Response, response)
        self.created_action.response =\
            response if response.status_code == 200\
            else None

    def _display_discogs_release(self):
        """Display the tracks from the discogs release
            in the discogsTableWidget.
            """
        response = self.created_action.response
        if response is None:
            return
        data = response.json()
        headers = ['Index', 'Position', 'Title']
        self.discogsTableWidget.setColumnCount(len(headers))
        self.discogsTableWidget.setHorizontalHeaderLabels(headers)
        if 'tracklist' in data:
            for track in data['tracklist']:
                if track['type_'] != 'track':
                    continue
                position = QTableWidgetItem(track['position'])
                title = QTableWidgetItem(track['title'])
                self.discogsTableWidget\
                    .insertRow(self.discogsTableWidget.rowCount())
                for index, item in enumerate((position, title)):
                    item.setFlags(item.flags & ~Qt.ItemIsEditable)
                    self.discogsTableWidget\
                        .setItem(self.discogsTableWidget
                                 .rowCount()-1, index + 1, item)
        self.discogsTableWidget.resizeColumnsToContents()
        row_headings: List[str] = []
        for row in range(self.discogsTableWidget.rowCount()):
            if self.created_action.mappings is None:
                self.created_action.mappings = []
            self.created_action.mappings.append(None)
            row_headings.append(f"{row}")
        self.discogsTableWidget.setVerticalHeaderLabels(row_headings)
        util_f.refresh_widget(self.discogsTableWidget)
        self.link_scrollbars(self.discogsTableWidget.verticalScrollBar(),
                             self.discogsVerticalScrollBar)
        self.allow_scrollbar_sync()

    def get_and_display_discogs_release(self):
        """Get the discogs release related to the typed ID
            and show the related tracks.
        """
        self._get_discogs_release()
        self._display_discogs_release()

    def map_discogs_indexes(self, row: int, column: int):
        """Allow a user to type which song this discogs track is the same as.

        Parameters
        ----------
        row : int -
            The row in the discogsTableWidget, referring to which track.\n
        column : int -
            The column being edited. If not the same as
            the song_indexes_column,
            returns.
        """
        song_indexes_column = 0
        if column != song_indexes_column:
            return
        self.created_action.mappings = cast(List[Union[None, int]],
                                            self.created_action.mappings)
        item = self.discogsTableWidget.item(row, column)
        if item is None:
            self.created_action.mappings[row] = None
        else:
            try:
                index: Union[int, None] = int(item.text())
                index = cast(int, index)
                if index > self.discogsSelectedSongsTableView\
                    .model().rowCount()\
                        or index < 0:
                    index = None
                self.created_action.mappings[row] = index
            except ValueError:
                self.created_action.mappings[row] = None
        mappings_set = self._check_mappings_validity()
        save_state = SaveState.Saved if mappings_set else SaveState.Updated
        self._set_save_state(save_state, InputWidget.DiscogsTable)

    def _check_mappings_validity(self) -> bool:
        """Determines whether all discogs indexes have been mapped.

            Returns
            -------
            bool
                Whether the entire discogs release is mapped or not.
            """
        self.created_action.mappings = cast(List[Union[None, int]],
                                            self.created_action.mappings)
        return None not in self.created_action.mappings

    def _create_discogs_selected_songs(self):
        """Display the discogs release frame, and convert mappings to a list.
            """
        self.discogsReleaseFrame.show()
        if self.created_action.mappings is None:
            self.created_action.mappings = []

    def auto_map_discogs_release(self):
        """Set the discogs mapping to the same as the row index.
            """
        song_indexes_column = 0
        for row in range(self.discogsTableWidget.rowCount()):
            item = QTableWidgetItem(f"{row}")
            self.discogsTableWidget.setItem(row, song_indexes_column, item)
    # endregion

    # region Values Table
    def display_values_table(self, toggled: bool):
        """Shows or hides the Values Table Frame.

            Parameters
            ----------
            toggled : bool -
                Whether the values table should be shown or not.
            """
        if not toggled:
            self.newValuesTableWidget.clear()
            self.newValuesTableWidget.reset()
            self.newValuesTableWidget.setColumnCount(0)
            self.newValuesTableWidget.setRowCount(0)
            self.created_action.values = None
        self.tableValuesFrame.setEnabled(toggled)
        self.tableValuesFrame.setVisible(toggled)
        self.valuesSummary.setVisible(toggled)

    def _get_table_values(self) -> List[List[str]]:
        """Get the values that have been typed into the value table.

            Returns
            -------
            List[List[str]] -
                The values that have been typed in the individual columns
                of the values table.
            """
        table_values: List[List[str]] = []
        for row in range(self.newValuesTableWidget.rowCount()):
            row_values = []
            for column in range(2, self.newValuesTableWidget.columnCount()):
                item = self.newValuesTableWidget.item(row, column)
                if item is None:
                    continue
                row_values.append(item.text())
            if len(row_values) > 0:
                table_values.append(row_values)
        return table_values

    def _neaten_table_values(self,
                             values: List[List[str]])\
            -> Union[List[str], List[List[str]]]:
        """Neaten the values from the table,
            splitting on the split string, to allow multiple values

            Parameters
            ----------
            values : List[List[str]] -
                Values that should be neatened.

            Returns
            -------
            Union[List[str], List[List[str]]] -
                The Values that have been neatened.
            """
        neatened_values: Union[List[str], List[List[str]]] = []  # type: ignore
        split_string = settings.split_text_entered
        if self.newValuesTableWidget.columnCount() == 3:  # 1 plus buttons
            neatened_values = cast(List[str], neatened_values)
            for value in values:
                val = value[0]
                vals = val.split(split_string)
                for value_been_split in vals:
                    neatened_values.append(value_been_split)
        elif self.newValuesTableWidget.columnCount() == 4:  # 2 plus buttons
            neatened_values = cast(List[List[str]], neatened_values)
            for value in values:
                all_roles = value[0]
                all_people = value[1]
                roles = all_roles.split(split_string)
                people = all_people.split(split_string)
                for role in roles:
                    for person in people:
                        neatened_values.append([role, person])
        return neatened_values

    def save_table_values(self):
        """Save the values that have been typed in the values table.
            """
        values = self._neaten_table_values(self._get_table_values())
        self.created_action.values = values
        if len(self.created_action.values) > 0:
            self.saveValuesButton.hide()
            save_state = SaveState.Saved
        else:
            print("Length of new values is less than or = 0")
            self.saveValuesButton.setText("SAVE VALUES FROM TABLE")
            self.saveValuesButton.show()
            save_state = SaveState.Unsaved
        self._set_save_state(save_state, InputWidget.ValuesTable)
        self.valuesCount.setText(f"{len(self.created_action.values)}")

    def activate_update_table_values(self, *_):
        """Allows a user to update the values that have been saved,
            if they have been changed.
            """
        if not self.created_action.values:
            return
        else:
            self.saveValuesButton.setText("UPDATE SAVED TABLE VALUES")
            self.saveValuesButton.setVisible(True)
            self._set_save_state(SaveState.Updated, InputWidget.ValuesTable)

    def setup_values_table(self):
        """Setup the display of the values table.
            """
        function = function_mappings[self.created_action.action]
        if function.input_type is InputWidget.CopyTable:
            # self.display_values_table(False)
            self.setup_copy_table()
        if function.input_type is not InputWidget.ValuesTable\
                or self.created_action.tags is None:
            self.display_values_table(False)
            return
        tags_set: bool = True
        self.created_action.tags = cast(List[SelectedTag],
                                        self.created_action.tags)
        for tag in self.created_action.tags:
            if tag.tag is None:
                tags_set = False
                break
            if function.function.__name__ == copy_values.__name__\
                    and tag.copy_tag is None:
                tags_set = False
                break
        if not tags_set:
            self.display_values_table(False)
            return
        self.display_values_table(True)
        util_f.refresh_widget(self.newValuesTableWidget)
        table_type = function.values_table_type
        values_table.create_values_table(self, table_type, self.table_type)

    def _set_save_state(self,
                        save_state: SaveState,
                        input_widget: InputWidget):
        """Sets whether the data in an input widget has been saved or not.

            Parameters
            ----------
            save_state : SaveState
                The state of the way the data is saved.
            input_widget : InputWidget
                The input that should be checked.
            """
        main_color: str
        accent_color: str
        pressed_color: str
        alternating_row_color: str
        disabled_color: str = "lightgrey"
        if save_state == SaveState.Saved:
            main_color = "lightgreen"
            accent_color = "green"
            pressed_color = "limegreen"
            alternating_row_color = "rgb(220, 255, 220)"
        elif save_state == SaveState.Updated:
            main_color = "navajowhite"
            accent_color = "rgb(250, 100, 50)"
            pressed_color = "rgb(255, 200, 120)"
            alternating_row_color = "papayawhip"
        elif save_state == SaveState.Unsaved:
            main_color = "pink"
            accent_color = "rgb(150, 0, 150)"
            pressed_color = "rgb(255, 160, 180)"
            alternating_row_color = "lavenderblush"
        else:
            return

        general_color = f"color: {accent_color}"
        general_border_color = f"border-color: {main_color}"
        button_colors = f"border-color: {accent_color};\
            background: {main_color}"

        general_style_sheet = f"{general_border_color}; {general_color}"
        button_style_sheet = f"{button_colors}; {general_color}"
        pressed_style_sheet = f":pressed {{background: {pressed_color}}}"
        toggled_style_sheet = f":checked {{background: {pressed_color}}}"
        enabled_style_sheet = f":enabled{{{button_style_sheet}}} \
                              {pressed_style_sheet}"
        enabled_toggled_sheet = f":enabled{{{button_style_sheet}}} \
                                {toggled_style_sheet}"
        scroll_bar_style_sheet = f"QScrollBar::handle {{border-color: \
                                {main_color}; background: {main_color}}}"
        scroll_bar_disabled_sheet = f"QScrollBar::handle {{border-color: \
                                {disabled_color}; \
                                background: {disabled_color}}}"
        table_style_sheet = (f"QTableView QTableCornerButton::section\
                                {{background-color: {main_color}}}"
                             f"QHeaderView::section::horizontal\
                                {{background-color: {main_color}}}"
                             f"QHeaderView::section::vertical\
                                {{background-color: {main_color}}}"
                             f"QTableView {{alternate-background-color:\
                                {alternating_row_color}; \
                                gridline-color: {main_color}}}"
                             f"{scroll_bar_style_sheet}"
                             )
        if input_widget == InputWidget.ValuesTable:
            for widget in (self.valuesTableHeading,
                           self.displayValuesTableButton):
                widget.setStyleSheet(general_style_sheet)
            self.saveValuesButton.setStyleSheet(f"QPushButton\
                {{{button_style_sheet}}} {pressed_style_sheet}")
            self.tableValuesFrame.setStyleSheet((f"QFrame#tableValuesFrame\
                {{{general_border_color}}}"))
            current_style_sheet = self.newValuesTableWidget.styleSheet()
            self.newValuesTableWidget.setStyleSheet(f"{current_style_sheet}\
                {table_style_sheet}")
        elif input_widget == InputWidget.DiscogsTable:
            for widget in (self.discogsReleaseHeading,
                           self.displayDiscogsReleaseButton):
                widget.setStyleSheet(general_style_sheet)
            self.discogsReleaseFrame\
                .setStyleSheet(f"QFrame#discogsReleaseFrame\
                    {{{general_border_color}}}")
            for widget in (self.releaseIDLabel,
                           self.discogsLabel,
                           self.selectedLabel):
                widget.setStyleSheet(general_color)
            for widget in (self.downloadReleaseButton, self.autoMapButton):
                widget.setStyleSheet(enabled_style_sheet)
            self.syncButton.setStyleSheet(enabled_toggled_sheet)
            for widget in (self.discogsTableWidget,
                           self.discogsSelectedSongsTableView):
                current_sheet = widget.styleSheet()
                widget.setStyleSheet(f"{current_sheet}{table_style_sheet}")
            for scroll_bar in (self.discogsVerticalScrollBar,
                               self.selectedSongsVerticalScrollBar,
                               self.discogsSyncScrollBar):
                current_sheet = scroll_bar.styleSheet()
                scroll_bar.setStyleSheet(f"{current_sheet}\
                                         {scroll_bar_style_sheet}\
                                         {scroll_bar_disabled_sheet}")
        elif input_widget == InputWidget.CopyTable:
            for widget in (self.copyTableHeading,
                           self.displayCopyTableButton):
                widget.setStyleSheet(general_style_sheet)
            self.saveCopyValuesButton.setStyleSheet(f"QPushButton\
                {{{button_style_sheet}}} {pressed_style_sheet}")
            self.copyTableFrame.setStyleSheet((f"QFrame#copyTableFrame\
                {{{general_border_color}}}"))
            for widget in (self.copyTableIndexesTableWidget,
                           self.copyTableSelectedSongs):
                current_style_sheet = widget.styleSheet()
                widget.setStyleSheet(f"{current_style_sheet}\
                    {table_style_sheet}")
    # endregion

    # region Copy Table
    def display_copy_table(self, toggled: bool):
        """Shows or hides the Copy Table Frame.

            Parameters
            ----------
            toggled : bool -
                Whether the copy table should be shown or not.
            """
        if not toggled:
            self.copyTableIndexesTableWidget.clear()
            self.copyTableIndexesTableWidget.reset()
            self.copyTableIndexesTableWidget.setColumnCount(0)
            self.copyTableIndexesTableWidget.setRowCount(0)
            self.created_action.copy_mappings = None
        self.copyTableFrame.setEnabled(toggled)
        self.copyTableFrame.setVisible(toggled)

    def _get_copy_table_values(self) -> List[int]:
        """Get the values that have been typed into the copy table.

            Returns
            -------
            List[List[str]] -
                The mappings that have been typed in the table.
            """
        table_values: List[int] = []
        for row in range(self.copyTableIndexesTableWidget.rowCount()):
            item = self.copyTableIndexesTableWidget.item(row, 0)
            if item is None:
                table_values.append(-1)
            else:
                try:
                    table_values.append(int(item.text()))
                except ValueError:
                    table_values.append(-1)
        return table_values

    def save_copy_table_values(self):
        """Save the values that have been typed in the copy table.
            """
        values = self._get_copy_table_values()
        self.created_action.copy_mappings = values

        if len(self.created_action.copy_mappings) > 0:
            self.saveCopyValuesButton.hide()
            save_state = SaveState.Saved
        else:
            self.saveCopyValuesButton.setText("SAVE VALUES FROM TABLE")
            self.saveCopyValuesButton.hide()
            save_state = SaveState.Unsaved
        self._set_save_state(save_state, InputWidget.CopyTable)
        self.copyTableCount.setText(
            f"{len(self.created_action.copy_mappings)}"
        )

    def activate_update_copy_values(self, *_):
        """Allows a user to update the values that have been saved,
            if they have been changed.
            """
        if not self.created_action.copy_mappings:
            return
        else:
            self.saveCopyValuesButton.setText("UPDATE SAVED COPY VALUES")
            self.saveCopyValuesButton.show()
            self._set_save_state(SaveState.Updated, InputWidget.CopyTable)

    def setup_copy_table(self):
        """Setup the display of the copy table
            """
        function = function_mappings[self.created_action.action]
        if function.input_type is not InputWidget.CopyTable:
            self.display_copy_table(False)
            return
        if self.created_action.tags is None:
            self.display_copy_table(False)
            return
        tags_set = all(self.created_action.tags)
        if not tags_set:
            self.display_copy_table(False)
            return
        self.display_copy_table(True)
        for widget in (self.copyTableIndexesTableWidget,
                       self.copyTableSelectedSongs):
            util_f.refresh_widget(widget)
        values_table.create_values_table(self, ValuesTableType.Copy, None)
    # endregion

    # region Scrollbars
    def link_scrollbars(self,
                        scrollbar_1: QScrollBar,
                        scrollbar_2: QScrollBar,
                        hide: bool = True):
        """Link the two scrollbars sent,
            so that when bar changes, the other changes too.

            Parameters
            ----------
            scrollbar_1 : QScrollBar -
                First scrollbar that should be linked.\n
            scrollbar_2 : QScrollBar -
                Second scrollbar that should be linked.\n
            hide : bool, optional -
                Whether the first scrollbar should be hidden
                after the scrollbars are linked.
                By default True.
            """
        scrollbar_2.setVisible(True)
        if scrollbar_1.maximum() == 0:
            scrollbar_2.setVisible(False)
        scrollbar_2.setRange(scrollbar_1.minimum(), scrollbar_1.maximum())
        scrollbar_2.setPageStep(scrollbar_1.pageStep())
        scrollbar_2.setSingleStep(scrollbar_1.singleStep())

        value_changed_1 = partial(set_scrollbar_value,
                                  slot_scrollbar=scrollbar_2,
                                  signal_scrollbar=scrollbar_1)
        value_changed_1.slot_type = ScrollBarSlotType.Value  # type: ignore
        value_changed_1.signal_scrollbar = scrollbar_1  # type: ignore
        value_changed_1.slot_scrollbar = scrollbar_2  # type: ignore

        value_changed_2 = partial(set_scrollbar_value,
                                  slot_scrollbar=scrollbar_1,
                                  signal_scrollbar=scrollbar_2)
        value_changed_2.slot_type = ScrollBarSlotType.Value  # type: ignore
        value_changed_2.signal_scrollbar = scrollbar_2  # type: ignore
        value_changed_2.slot_scrollbar = scrollbar_1  # type: ignore

        range_changed = partial(set_scrollbar_changed_range,
                                slot_scrollbar=scrollbar_1)
        range_changed.slot_type = ScrollBarSlotType.Range  # type: ignore
        range_changed.signal_scrollbar = scrollbar_2  # type: ignore
        range_changed.slot_scrollbar = scrollbar_1  # type: ignore

        scrollbar_1.valueChanged.connect(value_changed_1)
        scrollbar_2.valueChanged.connect(value_changed_2)
        scrollbar_1.rangeChanged.connect(range_changed)
        if hide:
            scrollbar_1.setStyleSheet("QScrollbar {width: 0px}")
        for partial_function in (value_changed_1,
                                 value_changed_2,
                                 range_changed):
            self.scrollbar_partials.append(partial_function)

    def unlink_discogs_scrollbar(self):
        """Remove the slots and signals that link the
            discogs scrollbar to other scrollbars in that frame.
            """
        self.discogsSyncScrollBar.valueChanged.disconnect()

        for function in self.scrollbar_partials[:]:
            try:
                if function.slot_scrollbar == self.discogsSyncScrollBar:
                    try:
                        function.signal_scrollbar = cast(QScrollBar,
                                                         function
                                                         .signal_scrollbar)
                        if function.slot_type == ScrollBarSlotType.Value:
                            function.signal_scrollbar.valueChanged\
                                .disconnect(function)
                        elif function.slot_type == ScrollBarSlotType.Range:
                            function.signal_scrollbar.rangeChanged\
                                .disconnect(function)
                        else:
                            continue
                        self.scrollbar_partials.remove(function)
                    except TypeError:
                        print("Unlink Scrollbars Type Error.")
            except AttributeError:
                print("Unlink Scrollbars Attribute Error")

        # for function in self.scrollbar_partials[:]:
        #     sig = inspect.signature(function)
        #     if sig.parameters['slot_scrollbar'].default\
        #             == self.discogsSyncScrollBar:
        #         try:
        #             if sig.parameters['slot_type'].default\
        #                     == ScrollBarSlotType.Value:
        #                 sig.parameters['signal_scrollbar']\
        #                     .default.valueChanged.disconnect(function)
        #             elif sig.parameters['slot_type'].default\
        #                     == ScrollBarSlotType.Range:
        #                 sig.parameters['signal_scrollbar']\
        #                     .default.rangeChanged.disconnect(function)
        #             else:
        #                 continue
        #             self.scrollbar_partials.remove(function)
        #         except TypeError:
        #             print("Unlink Scrollbars Type Error.")

        self.discogsSyncScrollBar.setRange(0, 99)
        self.discogsSyncScrollBar.setValue(0)

    def sync_discogs_scrollbar(self, toggled: bool):
        """Sync the scrolling of the discogs scrollbar
            with the tables in this frame

            Parameters
            ----------
            toggled : bool
                Whether the discogs scrollbar should be synced or unsynced.
            """
        if toggled:
            self.discogsSyncScrollBar.setEnabled(True)
            self.link_scrollbars(self.discogsTableWidget.verticalScrollBar(),
                                 self.discogsSyncScrollBar)
            self.link_scrollbars(self.discogsSelectedSongsTableView
                                 .verticalScrollBar(),
                                 self.discogsSyncScrollBar)
        else:
            self.unlink_discogs_scrollbar()
            self.discogsSyncScrollBar.setEnabled(False)

    def allow_scrollbar_sync(self):
        """Determine whether the discogs scrollbar can be synced
            with the other scrollbars in the discogs frame.
            """
        if self.discogsTableWidget.rowCount() ==\
                self.discogsSelectedSongsTableView.model().rowCount()\
                and self.discogsSelectedSongsTableView.model().rowCount() > 0:
            self.syncWidget.setVisible(True)
            self.autoMapButton.setEnabled(True)
            if self.discogsSelectedSongsTableView\
                    .verticalScrollBar().maximum() <= 0:
                self.syncButton.setEnabled(False)
            else:
                self.syncButton.setEnabled(True)
        else:
            self.syncWidget.setVisible(False)
            self.syncButton.setChecked(False)
            self.syncButton.setEnabled(False)
            self.autoMapButton.setEnabled(False)
    # endregion

    def set_songs_custom_name(self, name: str):
        """Set the given name to the created attribute custom songs name.

            Parameters
            ----------
            name : str -
                String to be set.
            """
        self.created_action.custom_songs_name = name

    def set_values_custom_name(self, name: str):
        """Set the given name to the created attribute custom values name.

            Parameters
            ----------
            name : str -
                String to be set.
            """
        self.created_action.custom_values_name = name


class JobDialog(QDialog, Ui_JobDialog):
    """Dialog that creates a scroll area list of widgets
        used to create multiple actions
    """
    def __init__(self,
                 parent: QMainWindow,
                 song_model: SongTableModel,
                 selected_indexes: List[QModelIndex]):
        """Constructor for Job Dialog.

            Parameters
            ----------
            parent : QMainWindow -
                The Window that the dialog should be displayed for.\n
            song_model : SongTableModel -
                The model that the songs to be worked on are stored in.\n
            selected_indexes : List[QModelIndex] -
                The indexes of the songs to be worked on.
            """
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.original_model = song_model
        self.original_indexes = selected_indexes

        self.song_proxy_model = SongTableProxyModel()
        self.song_proxy_model.setSourceModel(self.original_model)
        self.song_proxy_model.change_model_indexes(self.original_indexes)

        self.created_actions: List[ActionToCreate] = []

        util_f.refresh_widget(self.actionsScrollArea)

        self.create_action_widget(index=0)

    def create_action_widget(self, index: int = 0):
        """Add an action widget to the actions scroll area.

            Parameters
            ----------
            index : int, optional -
                Location where the action widget should be added.
                By default 0.
            """
        action_widget = ActionWidget(self.actionsScrollAreaWidgetContents,
                                     self)
        self.created_actions.insert(index, action_widget.created_action)
        self.actionsScrollAreaContentsVerticalLayout.insertWidget(
            index, action_widget)

    def remove_action_widget(self,
                             action_widget: ActionWidget):
        """Remove the action widget sent from the actions scroll area.

            Parameters
            ----------
            action_widget : ActionWidget -
                The action widget to be removed.
            """
        parent_layout = self.actionsScrollAreaContentsVerticalLayout
        util_f.remove_widget_from_scroll(action_widget,
                                         parent_layout,
                                         self.created_actions)
