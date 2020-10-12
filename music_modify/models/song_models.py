"""Module for the different models that are used to
    store songs added to the program.
    """
# pylint: disable=invalid-name
from typing import List, Union

from PyQt5.QtCore import QAbstractTableModel,  QModelIndex,\
    QSortFilterProxyModel, Qt, QVariant

from prefs import settings
from songs import Song
from utils import enums


class SongTableModel(QAbstractTableModel):
    """Main model used to represent songs.
        """
    empty_message = "Files Will Show Here When Added. Drag files here."
    # ? message shown when no values present

    def __init__(self, songs: List[Song]):
        """Constructor for SongTableModel. Stores a reference to the
            songs in the model.

            Parameters
            ----------
            songs : List[Song]
                list of songs to add to the model
            """
        super().__init__()
        self.songs = songs

    def data(self, index: QModelIndex,
             role: Union[Qt.ItemDataRole, enums.UserRole])\
            -> Union[str, QVariant, Song]:
        """Stores the data that the model should expose.

            Parameters
            ----------
            index : QModelIndex -
                Row and Column that data is being requested for\n
            role : Union[Qt.ItemDataRole, enums.UserRole] -
                Role of the data, to include colors etc.

            Returns
            -------
            Union[str, QVariant, Song] -
                If role is display, returns value to display.
                If role requests Song, returns that.
                Else role is invalid, and QVariant is returned.
            """
        if role == Qt.DisplayRole:
            song = self.songs[index.row()]
            tag_info = song.display_info[index.column()]
            return tag_info
        if role == enums.UserRole.SongRole.value:
            song = self.songs[index.row()]
            return song
        return QVariant()

    def rowCount(self, _: QModelIndex) -> int:
        """Sets number of rows of this model.

            Parameters
            ----------
            _ : QModelIndex -
                Row and column info received when called.
                Number doesn't need to be stored

            Returns
            -------
            int -
                number of rows of this model
            """
        return len(self.songs)

    def columnCount(self, _: QModelIndex) -> int:
        """Sets number of columns of this model.

            Parameters
            ----------
            _ : QModelIndex -
                Row and column info received when called.
                Number doesn't need to be stored

            Returns
            -------
            int -
                number of columns of this model
            """
        if len(self.songs) == 0:
            return 1  # ? uses 1 to keep a column for info
        else:
            return len(settings.files_tags)

    def headerData(self,
                   section: int,
                   orientation: Qt.Orientation,
                   role: Qt.ItemDataRole) -> Union[str, QVariant]:
        """Sets the headers for the model.

            Parameters
            ----------
            section : int -
                The current column or row that is being accessed/populated\n
            orientation : Qt.Orientation -
                Whether the header is horizontal or vertical.\n
            role : Qt.ItemDataRole -
                The type of information being requested.\n

            Returns
            -------
            Union[str, QVariant] -
                Returns str if valid, else QVariant

            Extended
            --------
            If songs in model is empty, sets the horizontal header to
                the empty message.\n
            Else sets horizontal header to the display names of the
                args in settings.
            """
        if role == Qt.DisplayRole:
            if len(self.songs) == 0:
                if orientation == Qt.Horizontal:
                    return self.empty_message
                if orientation == Qt.Verical:
                    return QVariant()
            if orientation == Qt.Horizontal:
                return settings.files_tags[section].display_name
            elif orientation == Qt.Vertical:
                return str(section + 1)
            else:
                return QVariant()
        return QVariant()


class SongTableProxyModel(QSortFilterProxyModel):
    """Model used to show selected songs being edited.
        """
    def __init__(self):
        """Constructor for SongTableProxyModel.
            """
        super().__init__()
        self.model_indexes: List[QModelIndex] = []
        self.selected_rows: List[int] = []

    def filterAcceptsRow(self,
                         source_row: int,
                         _: QModelIndex) -> bool:
        """Determines whether the row should be included in the model or not.
        Checks whether the row index is in the model_indexes of the model.

        Parameters
        ----------
        source_row : int -
            Row that is being checked for inclusion\n
        _ : QModelIndex -
            Parent of the model. Not used, as there isn't a parent model.

        Returns
        -------
        bool
            Whether the row should be included or not.
        """
        return source_row in self.selected_rows

    def change_model_indexes(self, model_indexes: List[QModelIndex]):
        """Change the data that is shown by the model, by changing the filter
            to disregard the original indexes, and instead show the indexes
            being sent here.

            Parameters
            ----------
            model_indexes : List[QModelIndex]
                The indexes that should be shown in the model.
            """
        self.model_indexes = model_indexes
        self.selected_rows = [model_index.row()
                              for model_index in self.model_indexes]
        self.invalidateFilter()
