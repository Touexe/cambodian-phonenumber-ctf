import re

from .validate import is_valid, normalize, strip_number


PHONE_PATTERNS = [
    re.compile(r"\+855[-\s]?\d{2}[-\s]?\d{2,4}[-\s]?\d{2,4}"),
    re.compile(r"0\d{1,2}[-\s]?\d{2,4}[-\s]?\d{2,4}"),
    re.compile(r"855[-\s]?\d{2}[-\s]?\d{2,4}[-\s]?\d{2,4}"),
]


def extract(text: str, unique: bool = True) -> list[str]:
    """Extract valid Cambodian phone numbers from unstructured text.

    Args:
        text: The text to search for phone numbers.
        unique: If True, return only unique numbers.

    Returns:
        A list of valid Cambodian phone number strings.
    """
    results: list[str] = []

    for pattern in PHONE_PATTERNS:
        for match in pattern.finditer(text):
            raw = match.group()
            cleaned = strip_number(raw)
            if is_valid(cleaned):
                results.append(raw.strip())

    if unique:
        seen: set[str] = set()
        unique_results: list[str] = []
        for r in results:
            n = normalize(r)
            if n and n not in seen:
                seen.add(n)
                unique_results.append(r)
        return unique_results

    return results
