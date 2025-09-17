"""Package for custom types that are used.

Not called `types`, to prevent shadowing the builtin library.
"""

from .song import Song
from .tag_info import TagInfo

__all__ = ["Song", "TagInfo"]
