"""Defines variables that don't change, that are needed in many places."""

from PySide6.QtCore import QModelIndex

PAIR_SIZE = 2
"The number of values that make up a pair"

PEOPLE_COL_COUNT = 2
"The number of columns used for a People Tag (role, person)"

Q_MODEL_INDEX = QModelIndex()
"""Single instance of an empty model index, so that it is not constructed
when used as a value for a default argument"""

PAIR_SEPARATOR = ": "
"The character(s) that should be written between pairs in the table."

PEOPLE_TAG_WIDTH = 150
"The general width that a column displaying [role, person] pairs should have."
