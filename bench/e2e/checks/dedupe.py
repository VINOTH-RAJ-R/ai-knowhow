import copy


def run(ns):
    fn = ns["dedupe_by_email"]
    tests = []

    rows = [
        {"email": "a@x.com", "updated_at": "2026-01-01", "v": 1},
        {"email": " A@X.com ", "updated_at": "2026-03-01", "v": 2},
        {"email": "b@x.com", "updated_at": "2026-02-01", "v": 3},
        {"email": "a@x.com", "updated_at": "2026-02-01", "v": 4},
    ]
    original = copy.deepcopy(rows)

    def t1():
        out = fn(copy.deepcopy(rows))
        return [r["v"] for r in out] == [2, 3]

    def t2():
        return fn([]) == []

    def t3():
        out = fn([{"email": "z@x.com", "updated_at": "2026-01-01T10:00:00", "v": 1},
                  {"email": "z@x.com", "updated_at": "2026-01-01T09:00:00", "v": 2}])
        return [r["v"] for r in out] == [1]

    def t4():
        out = fn([{"email": "c@x.com", "updated_at": "2025-12-31", "v": 1},
                  {"email": "b@x.com", "updated_at": "2025-12-31", "v": 2},
                  {"email": "a@x.com", "updated_at": "2025-12-31", "v": 3}])
        return [r["v"] for r in out] == [3, 2, 1]

    def t5():
        fn(rows)
        return rows == original  # must not mutate the input

    def t6():
        out = fn([{"email": "Q@x.com", "updated_at": "2026-05-01", "v": 1}])
        return len(out) == 1 and out[0]["v"] == 1

    for t in (t1, t2, t3, t4, t5, t6):
        try:
            tests.append(bool(t()))
        except Exception:  # noqa: BLE001
            tests.append(False)
    return sum(tests), len(tests)
