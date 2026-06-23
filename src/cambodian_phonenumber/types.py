from .constants import NumberType
from .validate import is_mobile, get_carrier


def detect_type(number: str) -> dict:
    """Detect the type of a phone number (mobile only in current digit-rule set)."""
    if is_mobile(number):
        return {
            "type": NumberType.MOBILE,
            "carrier": get_carrier(number),
            "area": None,
        }

    return {
        "type": NumberType.UNKNOWN,
        "carrier": None,
        "area": None,
    }
