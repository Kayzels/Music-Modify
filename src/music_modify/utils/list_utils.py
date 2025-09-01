"""Module for utilities related to working with lists."""

from music_modify.custom_types import constants


def getUnique(text: str, separator: str) -> list[str]:
    """Get the unique values from a string separated at `separator`.

    The values are kept in the original order, rather than being sorted.
    Empty strings are removed.

    Args:
        text: String containing the text to be separated
        separator: The character(s) used to split the string
    """
    items = [word.strip() for word in text.split(separator) if word.strip()]
    unique_items: list[str] = []
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    return unique_items


def toPairs(values: list[str], separator: str) -> list[list[str]]:
    """Convert a list of strings into a list of string pairs, split by separator.

    For example, given `['one:two', 'three:four']` and `:`,
    this will return `[['one', 'two'], ['three', 'four']]`.

    This returns _only_ the values that are pairs separated by separator.
    Any values that are not separated by separator are _excluded_ from the result,
    _not_ kept as they are.

    If there are more than two items separated in a pair, the second up until the last
    are merged into a single string.
    """
    result: list[list[str]] = []
    for value in values:
        if value.find(separator) == -1:
            continue
        parts = value.split(separator)
        if len(parts) == constants.PAIR_SIZE:
            result.append(parts)
        elif len(parts) > constants.PAIR_SIZE:
            first = parts[0]
            rest = separator.join(parts[1:])
            result.append([first, rest])
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

    If `index` is not 0 or 1, returns the original list.
    """
    if not remove_values:
        return original
    if index < 0 or index >= constants.PEOPLE_COL_COUNT:
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

    If `index` is not 0 or 1, returns the original list.
    """
    if not replacements:
        return original
    if index < 0 or index >= constants.PEOPLE_COL_COUNT:
        return original
    new_values: list[list[str]] = []
    for item in original:
        possible_value = [
            replacements.get(item[0], item[0]) if index == 0 else item[0],
            replacements.get(item[1], item[1]) if index == 1 else item[1],
        ]
        if possible_value not in new_values:
            new_values.append(possible_value)
    return new_values
