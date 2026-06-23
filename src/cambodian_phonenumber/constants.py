from enum import Enum

CAMBODIA_COUNTRY_CODE = "+855"
CAMBODIA_DIAL_CODE = "855"

SMART_PREFIXES: dict[str, dict[str, int]] = {
    "10": {"digit": 6},
    "15": {"digit": 6},
    "16": {"digit": 6},
    "69": {"digit": 6},
    "70": {"digit": 6},
    "81": {"digit": 6},
    "86": {"digit": 6},
    "87": {"digit": 6},
    "93": {"digit": 6},
    "96": {"digit": 7},
    "98": {"digit": 6},
}

METFONE_PREFIXES: dict[str, dict[str, int]] = {
    "31": {"digit": 7},
    "60": {"digit": 6},
    "66": {"digit": 6},
    "67": {"digit": 6},
    "68": {"digit": 6},
    "71": {"digit": 7},
    "88": {"digit": 7},
    "90": {"digit": 6},
    "97": {"digit": 7},
}

CELLCARD_PREFIXES: dict[str, dict[str, int]] = {
    "11": {"digit": 6},
    "12": {"digit": 6},
    "17": {"digit": 6},
    "61": {"digit": 6},
    "76": {"digit": 7},
    "77": {"digit": 6},
    "78": {"digit": 6},
    "79": {"digit": 6},
    "85": {"digit": 6},
    "89": {"digit": 6},
    "92": {"digit": 6},
    "95": {"digit": 6},
    "99": {"digit": 6},
}

PREFIXES: dict[str, dict[str, int]] = dict(
    sorted({**CELLCARD_PREFIXES, **METFONE_PREFIXES, **SMART_PREFIXES}.items())
)


class Carrier(str, Enum):
    CELLCARD = "cellcard"
    SMART = "smart"
    METFONE = "metfone"


PREFIX_TO_CARRIER: dict[str, Carrier] = {}
for p in SMART_PREFIXES:
    PREFIX_TO_CARRIER[p] = Carrier.SMART
for p in METFONE_PREFIXES:
    PREFIX_TO_CARRIER[p] = Carrier.METFONE
for p in CELLCARD_PREFIXES:
    PREFIX_TO_CARRIER[p] = Carrier.CELLCARD

CARRIER_NAMES: frozenset[str] = frozenset(c.value for c in Carrier)

MOBILE_PREFIX_BY_CARRIER: dict[str, list[str]] = {
    "smart": sorted(SMART_PREFIXES.keys()),
    "metfone": sorted(METFONE_PREFIXES.keys()),
    "cellcard": sorted(CELLCARD_PREFIXES.keys()),
}

# Backward-compatible 3-digit prefix maps (with leading zero)
MOBILE_PREFIXES: dict[str, str] = {}
for p, c in PREFIX_TO_CARRIER.items():
    MOBILE_PREFIXES["0" + p] = c.value.title()


class NumberType(str, Enum):
    MOBILE = "mobile"
    LANDLINE = "landline"
    UNKNOWN = "unknown"
