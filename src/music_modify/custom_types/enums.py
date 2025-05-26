from enum import Enum, Flag, auto


class TagType(Enum):
    Text = "text"
    People = "people"
    Data = "data"
    Url = "url"


class TagGroup(Enum):
    FileTags = "File Tags"
    StandardTags = "Standard Tags"
    CustomTags = "Custom Tags"


class WidgetType(Enum):
    List = 0
    Table = 1
    String = 2


class Direction(Enum):
    Up = 0
    Down = 1


class EditButton(Flag):
    Up = auto()
    Down = auto()
    Add = auto()
    Remove = auto()
    Clear = auto()
    Reset = auto()


class NavDirection(Enum):
    Next = auto()
    Previous = auto()
