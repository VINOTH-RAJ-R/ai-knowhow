def run(ns):
    f = ns["evaluate"]
    ok_cases = [("1 + 2 * 3", 7), ("(1 + 2) * 3", 9), ("2 ** 3 ** 2", 512), ("-2 ** 2", -4), ("(-2) ** 2", 4),
                ("10 / 4", 2.5), ("1.5 * 4", 6), ("  7 -  -3 ", 10), ("2 * (3 + (4 - 1)) / 3", 4), ("--5", 5),
                ("2 ** -1", 0.5), ("100", 100)]
    bad = ["2 +", "(1", "1 2", "", "* 3", "1 + )", "3 $ 4"]
    passed, total = 0, len(ok_cases) + len(bad) + 1
    for e, want in ok_cases:
        try:
            passed += abs(float(f(e)) - want) < 1e-9
        except Exception:  # noqa: BLE001
            pass
    for e in bad:
        try:
            f(e)
        except ValueError:
            passed += 1
        except Exception:  # noqa: BLE001
            pass
    try:
        f("1 / 0")
    except ZeroDivisionError:
        passed += 1
    except Exception:  # noqa: BLE001
        pass
    return passed, total
