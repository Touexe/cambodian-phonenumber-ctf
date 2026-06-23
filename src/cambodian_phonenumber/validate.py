import re

from .constants import PREFIXES, PREFIX_TO_CARRIER
from .exceptions import BadLength, BadPrefix, InvalidPhoneNumber


def strip_number(number: str) -> str:
    """Remove all non-digit characters except the leading +."""
    number = number.strip()
    if number.startswith("+"):
        inner = re.sub(r"\D", "", number[1:])
        return "+" + inner if inner else ""
    return re.sub(r"\D", "", number)


def sanitize(number: str) -> str:
    """Remove non-digits, strip leading 855 or 0. Returns only the digit string."""
    phone_number = strip_number(number)

    if phone_number.startswith("+"):
        phone_number = phone_number[1:]

    # All characters removed — empty string
    if len(phone_number) == 0:
        return ""

    # If it starts with 855 and has exactly 8 chars (855 + 5 remaining = wrong, but
    # per original logic: if "855" + 8 chars, return as-is; that's total 11).
    # Actually, the original means: after stripping non-digits, if it starts
    # with "855" AND len == 11 (855 + 8 suffix) — but "len(phone_number) == 8" cannot
    # hold when it starts with "855". Re-examining: the original says:
    #   if phone_number.startswith("855") and len(phone_number) == 8:
    # This seems to mean: when the number is "855" + 5 digits = 8 total.
    # That's a special case where the number is already in 855-format with exactly
    # the right length. We take it as-is.
    if phone_number.startswith("855") and len(phone_number) >= 8:
        # If exactly prefixless, keep as-is; otherwise strip the 855 prefix
        pass

    # Remove 855 and leading 0
    return phone_number.removeprefix("855").removeprefix("0")


def prefix(number: str) -> str:
    """Extract the 2-digit prefix (after stripping 855/0)."""
    return sanitize(number)[:2]


def digit_count(prefix_code: str) -> int:
    """Return the expected suffix digit count for a given 2-digit prefix."""
    entry = PREFIXES.get(prefix_code)
    if entry is None:
        raise BadPrefix(prefix=prefix_code)
    return entry["digit"]


def required_length(prefix_code: str) -> int:
    """Total expected digit count (prefix 2 + suffix digits)."""
    return digit_count(prefix_code) + 2


def is_valid(number: str) -> bool:
    """Check if a phone number is a valid Cambodian phone number (prefix + length)."""
    try:
        validate(number)
        return True
    except InvalidPhoneNumber:
        return False


def is_mobile(number: str) -> bool:
    """Check if a phone number is a Cambodian mobile number."""
    return is_valid(number)


def is_landline(number: str) -> bool:
    """Currently no landline prefixes in the digit-rule set — always False."""
    return False


def validate(phone_number: str) -> str:
    """
    Validate and normalize a Cambodian phone number.

    Returns the number in international format (+855XXXXXXXX).
    Raises InvalidPhoneNumber (BadPrefix / BadLength) on failure.
    """
    if not phone_number or len(phone_number) == 0:
        raise InvalidPhoneNumber

    if phone_number[0] != "+" and not phone_number[0].isdigit():
        raise InvalidPhoneNumber

    sanitized = sanitize(phone_number)
    if len(sanitized) == 0:
        raise InvalidPhoneNumber

    p = sanitized[:2]

    if p not in PREFIXES:
        raise BadPrefix(prefix=p)

    expected = required_length(p)
    actual = len(sanitized)

    if actual != expected:
        raise BadLength(prefix=p, required_length=expected, given_length=actual)

    return CAMBODIA_COUNTRY_CODE + sanitized


# Re-export for backwards compatibility — kept in module scope
CAMBODIA_COUNTRY_CODE = "+855"


def get_carrier(number: str) -> str | None:
    """Get the carrier name for a mobile number, or None."""
    try:
        validate(number)
    except InvalidPhoneNumber:
        return None
    p = prefix(number)
    c = PREFIX_TO_CARRIER.get(p)
    return c.value.title() if c else None


def get_landline_area(number: str) -> str | None:
    """Landline not supported in current digit-rule set."""
    return None


def to_international(number: str, spaces: bool = True) -> str:
    """Convert to international format (+855 XX XXX XXXX)."""
    try:
        validated = validate(number)
    except InvalidPhoneNumber:
        return ""
    digits = validated.removeprefix("+855")
    if spaces:
        return f"+855 {digits[:2]} {digits[2:5]} {digits[5:]}"
    return validated


def to_local(number: str, spaces: bool = True) -> str:
    """Convert to local format (0XX XXX XXXX)."""
    try:
        validated = validate(number)
    except InvalidPhoneNumber:
        return ""
    digits = validated.removeprefix("+855")
    if spaces:
        return f"0{digits[:2]} {digits[2:5]} {digits[5:]}"
    return f"0{digits}"


def normalize(number: str) -> str:
    """Normalize a Cambodian phone number to local format (0XXXXXXXX)."""
    try:
        validated = validate(number)
    except InvalidPhoneNumber:
        return ""
    return "0" + validated.removeprefix("+855")


def extract_prefix(number: str) -> str:
    """Extract the 2-digit prefix from a normalized number."""
    n = normalize(number)
    if not n or len(n) < 3:
        return ""
    return n[0:3]  # e.g. "0" + "12" = "012"


def extract_numbers(text: str) -> list[str]:
    """Extract all valid Cambodian phone numbers from text."""
    clean = strip_number(text)
    numbers: list[str] = []

    patterns = [
        r"\+855\d+",
        r"0\d+",
        r"855\d+",
    ]
    for pattern in patterns:
        for m in re.finditer(pattern, clean):
            candidate = m.group()
            if is_valid(candidate):
                numbers.append(candidate)

    return numbers
