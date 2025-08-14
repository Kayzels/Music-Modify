"""Module for utilities related to working with lists."""

from music_modify.custom_types import constants


def getUniqueOrdered(text: str, separator: str) -> list[str]:
    """Get the unique values from a string separated at `separator`, alphabetically.

    Args:
        text: String containing the text to be separated
        separator: The character(s) used to split the string
    """
    items = [word.strip() for word in text.split(separator)]
    ordered_unique_items: dict[str, None] = {}
    for item in items:
        ordered_unique_items[item] = None
    return list(ordered_unique_items.keys())


def toPairs(values: list[str], separator: str) -> list[list[str]]:
    """Convert a list of strings into a list of string pairs, split by separator.

    For example, given `['one:two', 'three:four']` and `:`,
    this will return `[['one', 'two'], ['three', 'four']]`
    """
    result: list[list[str]] = []
    for value in values:
        if not value.find(separator):
            continue
        parts = value.split(separator)
        if len(parts) == constants.PAIR_SIZE:
            result.append(parts)
    return result


def addValues[T](new: list[T] | None, original: list[T]) -> list[T]:
    """Add the value to the list, if it isn't already present."""
    if not new:
        return original
    return original + [item for item in new if item not in original]


def removePairs(
    pairs: set[tuple[str, ...]],
    original: list[list[str]],
) -> list[list[str]]:
    """Remove any pairs from `pairs` that appear in the `original` list."""
    if not pairs:
        return original
    return [item for item in original if tuple(item) not in pairs]


def removeMatchingSublistPairs(
    remove_values: set[str],
    original: list[list[str]],
    index: int,
) -> list[list[str]]:
    """Remove from original any pairs with values in `remove_values` at that index.

    Remove any pairs that appear in `remove_values` that contain
    any values that appear in `original` specifically at that index.

    For example, if `remove_values` is `{'a'}`,
    and `original` is `[['a', 'b'], ['b', 'a']]`,
    with an index of `0`, the result is `[['b', 'a']]`,
    and with `1` it is `[['a', 'b']]`.
    """
    if not remove_values:
        return original
    return [
        item
        for item in original
        if len(item) == constants.PEOPLE_COL_COUNT and item[index] not in remove_values
    ]


def remapMatchingSublistPairs(
    replacements: dict[str, str],
    original: list[list[str]],
    index: int,
) -> list[list[str]]:
    """Replace values at index, for the strings that are keys in replacements.

    Use the `replacements` dict to change the values that appear in `original`
    at the specified `index`, if the values appear in the list at that point.

    For example, if `replacements` is `{'a': 'c'}`,
    and `original` is `[['a', 'b'], ['d', 'a']]`,
    with an index of `0`, the result is `[['c', 'b'], ['d', 'a']]`,
    and with `1` it is `[['a', 'b'], ['d', 'c']]`
    """
    if not replacements:
        return original
    return [
        [
            replacements.get(item[0], item[0]) if index == 0 else item[0],
            replacements.get(item[1], item[1]) if index == 1 else item[1],
        ]
        for item in original
    ]
    # TODO: Don't add item if already present, remove instead
