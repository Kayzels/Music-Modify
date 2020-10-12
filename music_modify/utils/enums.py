"""General enums for different parts of the program.
    """
from enum import Enum, Flag
from PyQt5.QtCore import Qt


class ActionType(Enum):
    """The type of action that will be performed.
        """
    Unset = 0
    Manual = 1
    Download = 2
    Excel = 3


class CopyType(Flag):
    """How copying should be done for an action.
        """
    NotUsed = 0
    Append = 1
    Across = 2


class InputWidget(Enum):
    """The type of widget that should be used for input.
        """
    NotUsed = 0
    ValuesTable = 1
    DiscogsTable = 2
    CopyTable = 3


class ValuesTableType(Enum):
    """The type of data being stored in the values table.
        """
    Standard = 1
    Replace = 2
    Copy = InputWidget.CopyTable


class UserRole(Enum):
    """Roles related to models for Qt.
        """
    SongRole = Qt.UserRole + 1


class ChangeSelectionType(Enum):
    """The type of songs that should be shown when changing song selection.
        """
    Global = 1,
    Current = 2,
    Original = 3


class InfoType(Enum):
    """The type of information being stored in a TextWidget
        """
    Action = 1
    Tag = 2


class SaveState(Enum):
    """Whether data has been saved or not.
        """
    Unsaved = 1
    Updated = 2
    Saved = 3


class ScrollBarSlotType(Enum):
    """The type of slot that a scrollbar's signal should link to.
        """
    Value = 1
    Range = 2
