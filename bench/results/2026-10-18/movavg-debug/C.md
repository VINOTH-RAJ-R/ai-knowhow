There are two bugs, and the first one explains the "calling it twice" symptom.

1. **Mutable default argument.** `out=[]` is created once, when the function is defined. Every call that doesn't pass `out` appends to the same list, so the second call returns the first call's results followed by the new ones.

2. **Wrong window slice.** `values[start:i]` excludes the current element `values[i]`, so the window is shifted one position back. For `i = 0` the slice is empty, `sum([]) / len([])` raises `ZeroDivisionError`. Once the list is shared (bug 1), the value you see at the front can come from an earlier call, which is the "first value is wrong" symptom.

Fixed version:

```python
def moving_average(values, window):
    if window < 1:
        raise ValueError("window must be >= 1")
    out = []
    for i in range(len(values)):
        start = max(0, i - window + 1)   # last `window` values, ending at i
        chunk = values[start:i + 1]      # include values[i]
        out.append(sum(chunk) / len(chunk))
    return out
```

Check with `values = [1, 2, 3, 4]`, `window = 2`: the result is `[1.0, 1.5, 2.5, 3.5]`. The first element is the average of just `[1]` because there are fewer values than the window at the start, as you specified.

If some caller passes `out` on purpose, keep the parameter but default it to `None`:

```python
def moving_average(values, window, out=None):
    if out is None:
        out = []
    ...
```

**Optional: O(n) version.** The version above re-sums the window at each step, which is O(n * window). A running sum is O(n):

```python
def moving_average(values, window):
    if window < 1:
        raise ValueError("window must be >= 1")
    out = []
    total = 0.0
    for i, v in enumerate(values):
        total += v
        if i >= window:
            total -= values[i - window]
        out.append(total / min(i + 1, window))
    return out
```

With float inputs, the running sum can accumulate tiny rounding errors over a long series. If that matters, use the simple version or `math.fsum` on each chunk.
