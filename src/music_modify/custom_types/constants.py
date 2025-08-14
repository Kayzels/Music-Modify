from PySide6.QtCore import QModelIndex

PAIR_SIZE = 2
"The number of values that make up a pair"

PEOPLE_COL_COUNT = 2
"The number of columns used for a People Tag (role, person)"

Q_MODEL_INDEX = QModelIndex()
"""Single instance of an empty model index, so that it is not constructed
when used as a value for a default argument"""
