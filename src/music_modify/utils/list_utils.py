def getUniqueOrdered(text: str, separator: str) -> list[str]:
    items = [word.strip() for word in text.split(separator)]
    ordered_unique_items: dict[str, None] = {}
    for item in items:
        ordered_unique_items[item] = None
    return list(ordered_unique_items.keys())


def toPairs(values: list[str], separator: str) -> list[list[str]]:
    result: list[list[str]] = []
    for value in values:
        if not value.find(separator):
            continue
        parts = value.split(separator)
        if len(parts) == 2:
            result.append(parts)
    return result


def addValues(new: list[list[str]], original: list[list[str]]) -> list[list[str]]:
    return original + [item for item in new if item not in original]


def removePairs(
    pairs: set[tuple[str, ...]], original: list[list[str]]
) -> list[list[str]]:
    return [item for item in original if tuple(item) not in pairs]


def removeMatchingSublistPairs(
    remove_values: set[str], original: list[list[str]], index: int
) -> list[list[str]]:
    return [
        item for item in original if len(item) == 2 and item[index] not in remove_values
    ]


def remapMatchingSublistPairs(
    replacements: dict[str, str], original: list[list[str]], index: int
) -> list[list[str]]:
    return [
        [
            replacements.get(item[0], item[0]) if index == 0 else item[0],
            replacements.get(item[1], item[1]) if index == 1 else item[1],
        ]
        for item in original
    ]
