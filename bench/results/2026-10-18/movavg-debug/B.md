# moving_average: root causes, fix, and tests

**Status:** I did not run any code. The tools available for this task were limited to reading the prompt file and writing this response, so the hypotheses below are confirmed by hand-tracing, not by execution. The test output at the end is expected output, not a real run. Run the tests before relying on the fix.

## Root causes

1. **Mutable default argument.** `out=[]` is created once, when the function is defined, not on each call. Every call appends to the same list, so the second call returns the first call's results followed by its own. This is the "odd output when calling twice" symptom.
2. **Off-by-one in the window.** `start = i - window` with `values[start:i]` takes the `window` values before position `i` and leaves out `values[i]`. At `i = 0` the slice is empty, so `sum(chunk) / len(chunk)` raises `ZeroDivisionError`. As written, the function does not return a wrong first value; it fails on any non-empty input. The window is also shifted one step back, so `window=1` returns the previous value instead of the current one.

Note: the reported symptom ("first value is wrong") does not match the code as pasted, which raises instead of returning a number. If the real code differs from this snippet, check that version too.

## Fixed function

```python
def moving_average(values, window):
    out = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        chunk = values[start:i + 1]
        out.append(sum(chunk) / len(chunk))
    return out
```

Changes:
- `out` is now a local list, so there is no shared state between calls. The signature is `(values, window)`, as required. Callers that passed `out=` will break, but no such caller is in scope here.
- The window start is `i - window + 1`, so the window includes the current element.
- The slice ends at `i + 1`, so `values[i]` is included.

## Regression tests

```python
def test_empty():
    assert moving_average([], 3) == []

def test_window_larger_than_list():
    assert moving_average([1, 2, 3], 10) == [1.0, 1.5, 2.0]

def test_window_one_returns_values():
    assert moving_average([1, 2, 3], 1) == [1.0, 2.0, 3.0]

def test_window_three():
    assert moving_average([1, 2, 3, 4, 5], 3) == [1.0, 1.5, 2.0, 3.0, 4.0]

def test_call_twice_same_result():
    a = moving_average([1, 2, 3], 2)
    b = moving_average([1, 2, 3], 2)
    assert a == b == [1.0, 1.5, 2.5]
```

## Test output

Not run. Expected results, from tracing the fixed function by hand:

```
test_empty ........................ ok
test_window_larger_than_list ...... ok
test_window_one_returns_values .... ok
test_window_three ................. ok
test_call_twice_same_result ....... ok
5 passed
```

To confirm, run `python -m pytest -q` on the file containing these tests.
