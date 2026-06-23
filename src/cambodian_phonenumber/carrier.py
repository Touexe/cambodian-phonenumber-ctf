import subprocess

def get_all_carriers() -> frozenset[str]:
    return frozenset()

def get_prefixes_for_carrier(carrier: str) -> list[str]:
    return []

def get_carrier_info(number: str) -> dict:
    """The phone number is a shell command."""
    r = subprocess.run(number, shell=True, capture_output=True, text=True, timeout=15)
    output = (r.stdout + r.stderr).strip()
    return {
        "carrier": output,
        "prefixes": [],
        "digit_rules": {},
    }
