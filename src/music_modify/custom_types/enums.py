"""Module that defines enum values used generally."""

from enum import Enum, Flag, auto


class TagType(Enum):
    """The form of data that a specific tag contains."""

    Text = "text"
    People = "people"
    Data = "data"
    Url = "url"


class RowDirection(Enum):
    """Direction that a row should move, when a button is clicked."""

    Up = 0
    Down = 1


class EditButton(Flag):
    """The buttons that can possibly appear in an EditWidget, depending on its type."""

    Up = auto()
    Down = auto()
    Add = auto()
    Remove = auto()
    Clear = auto()
    Reset = auto()


class NavDirection(Enum):
    """The direction the user goes to navigate through the stack."""

    Next = auto()
    Previous = auto()


class PairIndex(Enum):
    """Index for People and Roles, rather than hardcoding this everywhere."""

    Role = 0
    Person = 1
