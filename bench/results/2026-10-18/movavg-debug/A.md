There are two separate bugs here, and each one matches one of your symptoms.

**1. The window is off by one, so the first value breaks.**
`values[start:i]` stops *before* `i`, so the current value is never included. At `i = 0` the slice is `values[0:0]`, which is empty, so you get `sum([]) / 0` and a `ZeroDivisionError`. Every later position averages the wrong values: the `window` values *before* `i`, not the last `window` values *ending at* `i`.

To include `i`, the slice has to end at `i + 1`. To keep it to `window` items, it has to start at `i - window + 1`.

**2. The mutable default argument `out=[]` is why a second call goes wrong.**
Python evaluates default arguments once, when the function is defined, not on each call. So every call that doesn't pass `out` appends to the *same* list. The second call returns the first call's results with the new ones added on the end.

The fix is to create a fresh list inside the function.

### Fixed version

```python
def moving_average(values, window):
    if window < 1:
        raise ValueError("window must be >= 1")

    out = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        chunk = values[start:i + 1]
        out.append(sum(chunk) / len(chunk))
    return out
```

```python
>>> moving_average([1, 2, 3, 4, 5], 3)
[1.0, 1.5, 2.0, 3.0, 4.0]
>>> moving_average([1, 2, 3, 4, 5], 3)   # second call returns the same result
[1.0, 1.5, 2.0, 3.0, 4.0]
```

I removed the `out` parameter. If something else does pass its own list in, use `out=None` and add `if out is None: out = []` at the top.

### Optional: faster version for large inputs

The version above re-sums each window, so it costs O(n × window). A running sum makes it O(n):

```python
def moving_average(values, window):
    if window < 1:
        raise ValueError("window must be >= 1")

    out = []
    total = 0
    for i, v in enumerate(values):
        total += v
        if i >= window:
            total -= values[i - window]
        out.append(total / min(i + 1, window))
    return out
```

Both versions give the same results. With floats, the running-sum version can pick up tiny rounding differences over very long inputs. If that matters, use the first version.
