def snakeToTitle(value: str) -> str:
    return value.replace("_", " ").title()


def tableHeader(value: str) -> str:
    return snakeToTitle(value).replace("Id3", "ID3")
