import string

CHARS = string.digits + string.ascii_letters


def num_to_base62(number: int) -> str:
    """Encode a non-negative integer as a base-62 string."""
    if number < 0:
        raise ValueError("number must be non-negative")
    if number == 0:
        return CHARS[0]

    encoded: list[str] = []
    while number:
        number, remainder = divmod(number, len(CHARS))
        encoded.append(CHARS[remainder])
    return "".join(reversed(encoded))
