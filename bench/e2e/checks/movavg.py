def run(ns):
    fn = ns["moving_average"]

    def close(a, b):
        return len(a) == len(b) and all(abs(x - y) < 1e-9 for x, y in zip(a, b))

    checks = [
        lambda: close(fn([1, 2, 3, 4, 5], 3), [1.0, 1.5, 2.0, 3.0, 4.0]),
        lambda: close(fn([10], 3), [10.0]),
        lambda: fn([], 2) == [],
        lambda: close(fn([2, 4, 6], 1), [2.0, 4.0, 6.0]),
        # calling twice must not accumulate results from the first call
        lambda: (fn([1, 1], 2), close(fn([3, 3], 2), [3.0, 3.0]))[1],
        lambda: close(fn([1, 2, 3, 4], 10), [1.0, 1.5, 2.0, 2.5]),
    ]
    passed = 0
    for c in checks:
        try:
            passed += bool(c())
        except Exception:  # noqa: BLE001
            pass
    return passed, len(checks)
