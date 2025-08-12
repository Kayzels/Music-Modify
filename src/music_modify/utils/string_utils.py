"""Module for utilities related to working with strings."""


def snakeToTitle(value: str) -> str:
    """Converts snake case text to title case."""
    return value.replace("_", " ").title()


def tableHeader(value: str) -> str:
    """Convers snake case text to title case, and replaces Id3 with ID3."""
    return snakeToTitle(value).replace("Id3", "ID3")
