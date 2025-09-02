"""Module that defines enum values used generally."""

from enum import Enum, Flag, auto


class TagType(Enum):
    """The form of data that a specific tag contains."""

    Text = "text"
    People = "people"
    Data = "data"
    Url = "url"


class EditorType(Enum):
    """The type of widget/display that should be used for editing a tag.

    Should only contain the types that can actually be handled.
    """

    Automatic = "Determine the editor based on tag data."
    SingleText = "Tags storing single values."
    MultipleText = "Tags storing multiple values."
    PeopleValue = "Tags storing role, person pairs."


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
