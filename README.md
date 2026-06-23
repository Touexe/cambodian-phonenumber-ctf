# cambodian-phonenumber

A Python library for parsing, validating, formatting, and extracting Cambodian phone numbers.

## Features

- **Validation** — Check if a string is a valid Cambodian phone number
- **Carrier detection** — Identify the mobile carrier/provider from the prefix
- **Type detection** — Distinguish between mobile and landline numbers
- **Formatting** — Convert between local and international formats
- **Number extraction** — Extract Cambodian phone numbers from unstructured text

## Installation

```bash
pip install cambodian-phonenumber
```

## Quick Start

```python
from cambodian_phonenumber import PhoneNumber

pn = PhoneNumber("012345678")
print(pn.is_valid)        # True
print(pn.carrier)         # Cellcard
print(pn.number_type)     # mobile
print(pn.to_international())  # +855 12 345 678
print(pn.to_local())          # 012 345 678
```
