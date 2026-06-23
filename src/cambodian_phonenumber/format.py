from .validate import to_international, to_local, normalize, strip_number


def format_number(
    number: str,
    fmt: str = "international",
    spaces: bool = True,
) -> dict:
    """
    Format a phone number.

    Args:
        number: The phone number string.
        fmt: Format style — "international", "local", "e164", or "raw".
        spaces: Whether to include spaces in the formatted output.

    Returns:
        A dict with the formatted number and available formats.
    """
    normalized = normalize(number)
    if not normalized:
        return {
            "input": number,
            "error": "Invalid Cambodian phone number",
            "formats": {},
        }

    digits = normalized[1:]
    e164 = f"+855{digits}"

    formats = {
        "international": to_international(normalized, spaces),
        "local": to_local(normalized, spaces),
        "e164": e164,
        "raw": digits,
    }

    formatted = formats.get(fmt, formats["international"])

    return {
        "input": number,
        "formatted": formatted,
        "format": fmt,
        "formats": formats,
    }
