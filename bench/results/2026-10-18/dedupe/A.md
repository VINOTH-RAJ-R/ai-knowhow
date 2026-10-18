```python
from datetime import datetime


def _parse_ts(value: str) -> datetime:
    """Parse an ISO 8601 date/datetime string, accepting a trailing 'Z' for UTC."""
    value = value.strip()
    if value[-1:] in ("Z", "z"):          # fromisoformat only accepts 'Z' on Python 3.11+
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def dedupe_by_email(rows):
    """
    Keep only the most recent row per email.

    - Emails match case-insensitively, ignoring surrounding whitespace.
    - "Most recent" is decided by parsing 'updated_at' as a real datetime,
      so differing formats or UTC offsets still compare correctly.
    - On a tie, the row that appears first in the input wins.
    - Returns the original row dicts (unmodified), sorted by normalized email.
    """
    latest = {}  # normalized email -> (parsed timestamp, row)

    for row in rows:
        key = row["email"].strip().casefold()
        ts = _parse_ts(row["updated_at"])
        current = latest.get(key)
        if current is None or ts > current[0]:
            latest[key] = (ts, row)

    return [latest[key][1] for key in sorted(latest)]
```

Example:

```python
rows = [
    {"email": "Bob@Example.com ", "updated_at": "2024-03-01T10:00:00Z", "name": "Bob v1"},
    {"email": "alice@example.com", "updated_at": "2024-01-15",           "name": "Alice"},
    {"email": " bob@example.com",  "updated_at": "2024-03-02T09:00:00Z", "name": "Bob v2"},
]

dedupe_by_email(rows)
# [
#   {'email': 'alice@example.com', 'updated_at': '2024-01-15', 'name': 'Alice'},
#   {'email': ' bob@example.com', 'updated_at': '2024-03-02T09:00:00Z', 'name': 'Bob v2'},
# ]
```

Some choices I made that you may want to change:

- **Timestamps are parsed, not compared as strings.** Comparing the raw strings only works when every value uses exactly the same format and timezone. Parsing them handles `2024-01-15`, `2024-01-15T08:00:00`, and `...+05:30` correctly. One catch: if some values have a timezone and others don't, Python can't compare them and raises `TypeError`. If your data mixes the two, normalize first (for example, treat naive values as UTC).
- **Output rows are returned unchanged.** The `email` field keeps its original spacing and casing, as shown above. If you want it cleaned up, add `row = {**row, "email": key}` before storing it.
- **Ties keep the first row seen.** To keep the last one instead, change `>` to `>=`.
- **`casefold()` instead of `lower()`.** It handles case-insensitive matching for non-ASCII characters properly. For ordinary ASCII emails the two behave the same.
- Rows with a missing `email` or `updated_at` raise `KeyError`. Use `row.get(...)` and skip those rows if you'd rather drop them quietly.

This runs in O(n log k) time, where k is the number of unique emails: one pass over the rows, then a sort of the unique keys.
