from enum import Enum


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
