Here is `is_valid_ipv4(s)`. It accepts only dotted-decimal IPv4 addresses: exactly four parts separated by `.`, each made of 1 to 3 ASCII digits, with a value from 0 to 255 and no leading zeros.

```python
def is_valid_ipv4(s):
    """Return True if s is a valid dotted-decimal IPv4 address, else False.

    Rules: exactly four parts separated by '.', each part is 1-3 ASCII digits,
    value 0-255, and no leading zeros (e.g. '01' is rejected).
    """
    if not isinstance(s, str):
        return False
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isascii() or not part.isdigit():
            return False
        if not 1 <= len(part) <= 3:
            return False
        if len(part) > 1 and part[0] == "0":
            return False
        if int(part) > 255:
            return False
    return True
```

Examples:

```python
assert is_valid_ipv4("192.168.1.1") is True
assert is_valid_ipv4("0.0.0.0") is True
assert is_valid_ipv4("255.255.255.255") is True

assert is_valid_ipv4("256.1.1.1") is False   # octet out of range
assert is_valid_ipv4("1.2.3") is False       # only three parts
assert is_valid_ipv4("1.2.3.4.5") is False   # five parts
assert is_valid_ipv4("01.2.3.4") is False    # leading zero
assert is_valid_ipv4("1.2.3.4 ") is False    # trailing whitespace
assert is_valid_ipv4("a.b.c.d") is False     # non-numeric
assert is_valid_ipv4("") is False            # empty string
assert is_valid_ipv4(None) is False          # not a string
```

Notes:

- The leading-zero rule is a choice. Some parsers read `010` as octal, so rejecting it avoids ambiguity. If you want to accept `01.2.3.4`, delete the `len(part) > 1 and part[0] == "0"` check.
- The `isascii()` check stops Unicode digits such as `²` from passing `isdigit()`.
- If you need more than a yes/no check (IPv6, network objects, and so on), the standard library's `ipaddress.IPv4Address(s)` does the same job and raises `ValueError` on bad input. Wrap it in `try/except` if you want a boolean.
