from dataclasses import dataclass


@dataclass
class TagInfo:
    id3_key: str
    display_name: str
    show_in_table: bool = False
