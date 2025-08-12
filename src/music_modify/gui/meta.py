"""Module that contains the metaclass that works with abstract classes
and PySide6."""

from abc import ABCMeta

from PySide6.QtCore import QObject


class ABCQMeta(ABCMeta, type(QObject)):
    """Used when there is an abstract class that also needs PySide6 attributes,
    like signals."""

    pass
