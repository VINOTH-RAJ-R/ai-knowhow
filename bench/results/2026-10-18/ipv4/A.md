```python
def is_valid_ipv4(s):
    """Return True if s is a valid dotted-decimal IPv4 address, e.g. '192.168.0.1'."""
    if not isinstance(s, str):
        return False

    parts = s.split(".")
    if len(parts) != 4:
        return False

    for part in parts:
        # Must be 1-3 ASCII digits (str.isdigit() alone accepts things like '²' or '٣')
        if not (1 <= len(part) <= 3) or not all("0" <= c <= "9" for c in part):
            return False
        # No leading zeros ("01", "001"), but "0" itself is fine
        if len(part) > 1 and part[0] == "0":
            return False
        if int(part) > 255:
            return False

    return True
```

What it accepts and rejects:

```python
assert is_valid_ipv4("192.168.1.1")
assert is_valid_ipv4("0.0.0.0")
assert is_valid_ipv4("255.255.255.255")

assert not is_valid_ipv4("256.1.1.1")      # octet out of range
assert not is_valid_ipv4("1.2.3")          # too few octets
assert not is_valid_ipv4("1.2.3.4.5")      # too many octets
assert not is_valid_ipv4("1..2.3")         # empty octet
assert not is_valid_ipv4("01.2.3.4")       # leading zero
assert not is_valid_ipv4("1.2.3.-4")       # sign
assert not is_valid_ipv4(" 1.2.3.4")       # whitespace
assert not is_valid_ipv4("1.2.3.4\n")      # trailing newline
assert not is_valid_ipv4("1.2.3.²")        # non-ASCII digit
assert not is_valid_ipv4(None)             # not a string
```

Notes on the choices:

- **Leading zeros are rejected.** `"01.2.3.4"` is ambiguous, since some parsers (like `inet_aton`) read a leading zero as octal. Rejecting it is the safe default. If you want to allow it, delete the leading-zero check.
- **Only strict dotted-decimal is accepted.** Shorthand forms like `"127.1"` or hex `"0x7f.0.0.1"` are rejected, even though some C libraries accept them.

If you don't need the details spelled out, the standard library gives the same strict behavior (Python 3.9.5+ rejects leading zeros):

```python
import ipaddress

def is_valid_ipv4(s):
    try:
        ipaddress.IPv4Address(s)
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False
```

One difference: `IPv4Address` also accepts an integer (`IPv4Address(3232235777)`). Add an `isinstance(s, str)` check if you only want strings.
