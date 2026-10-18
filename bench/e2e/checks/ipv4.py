CASES = [
    ("192.168.1.1", True), ("0.0.0.0", True), ("255.255.255.255", True), ("8.8.8.8", True),
    ("256.1.1.1", False), ("1.1.1", False), ("1.1.1.1.1", False), ("01.1.1.1", False),
    ("1.1.1.-1", False), ("a.b.c.d", False), ("", False), (" 1.1.1.1", False),
    ("1..1.1", False), ("1.1.1.1 ", False), ("999.0.0.0", False), ("1.2.3.04", False),
    ("10.0.0.255", True), ("172.16.254.1", True), ("1.1.1.1\n", False), ("١.١.١.١", False),
]


def run(ns):
    fn = ns["is_valid_ipv4"]
    passed = 0
    for s, want in CASES:
        try:
            if bool(fn(s)) == want:
                passed += 1
        except Exception:  # noqa: BLE001 - a crash is a failed case
            pass
    return passed, len(CASES)
