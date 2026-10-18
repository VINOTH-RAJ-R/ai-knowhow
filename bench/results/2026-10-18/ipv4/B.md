```python
def is_valid_ipv4(s):
    """Return True only for a strict dotted-decimal IPv4 address such as '192.168.1.1'."""
    if not isinstance(s, str):
        return False
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not (1 <= len(part) <= 3) or not part.isascii() or not part.isdigit():
            return False
        if len(part) > 1 and part[0] == "0":
            return False
        if int(part) > 255:
            return False
    return True
```

Asserts (not executed: this session has no code-execution tool, so these are unverified):

```python
assert is_valid_ipv4("192.168.1.1") is True
assert is_valid_ipv4("0.0.0.0") is True
assert is_valid_ipv4("255.255.255.255") is True
assert is_valid_ipv4("1.2.3.0") is True
assert is_valid_ipv4("256.1.1.1") is False
assert is_valid_ipv4("1.2.3") is False
assert is_valid_ipv4("1.2.3.4.5") is False
assert is_valid_ipv4("01.2.3.4") is False
assert is_valid_ipv4("1.2.3.00") is False
assert is_valid_ipv4("1.2.3.1000") is False
assert is_valid_ipv4("1..2.3") is False
assert is_valid_ipv4("") is False
assert is_valid_ipv4(" 1.2.3.4") is False
assert is_valid_ipv4("1.2.3.4 ") is False
assert is_valid_ipv4("1.2.3.4\n") is False
assert is_valid_ipv4("+1.2.3.4") is False
assert is_valid_ipv4("-1.2.3.4") is False
assert is_valid_ipv4("0x1.2.3.4") is False
assert is_valid_ipv4("1.2.3.4a") is False
assert is_valid_ipv4("١.2.3.4") is False  # Arabic-Indic digit one
assert is_valid_ipv4(None) is False
assert is_valid_ipv4(16843009) is False
```

Assumptions:
1. Only ASCII 0-9 count as digits; any other character, including whitespace and signs, makes the input invalid, with no trimming.
2. Non-str input (None, int, bytes) returns False rather than raising; the length cap of 3 digits per octet also keeps `int()` away from very long digit strings.
