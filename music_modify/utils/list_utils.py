def getUniqueOrdered(text: str, separator: str) -> list[str]:
    items = [word.strip() for word in text.split(separator)]
    ordered_unique_items: dict[str, None] = {}
    for item in items:
        ordered_unique_items[item] = None
    return list(ordered_unique_items.keys())
