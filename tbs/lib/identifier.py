"""
The Bestory Project
"""


ALPHABET = {
    36: "0123456789abcdefghijklmnopqrstuvwxyz",
}


def to(id: int, base: int) -> str:
    """
    Converts 10 base int ID to the N base str ID (public id)
    """
    if id < 0:
        raise ValueError("A positive int for ID must be provided")

    converted = []

    while id != 0:
        id, r = divmod(id, base)
        converted.insert(0, ALPHABET[base][r])

    return "".join(converted) or ALPHABET[base][0]


def to36(id: int) -> str:
    """
    Converts 10 base int ID to the 36 base str ID (public id)
    """
    return to(id, 36)


def from36(id: str) -> int:
    """
    Converts 36 base str ID to the 10 base int ID (internal id)
    """
    return int(id, 36)
