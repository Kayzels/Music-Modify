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
