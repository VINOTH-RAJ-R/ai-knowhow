```python
from datetime import datetime


def _parse_ts(value):
    # Python < 3.11 fromisoformat() rejects a trailing "Z", so map it to an explicit UTC offset.
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def dedupe_by_email(rows):
    """Keep only the most recent row per email (case-insensitive, whitespace-trimmed).

    Returns the kept rows sorted by normalized email.
    """
    latest = {}  # normalized email -> row with the newest updated_at
    for row in rows:
        key = row["email"].strip().lower()
        current = latest.get(key)
        if current is None or _parse_ts(row["updated_at"]) > _parse_ts(current["updated_at"]):
            latest[key] = row
    return [latest[key] for key in sorted(latest)]


if __name__ == "__main__":
    rows = [
        {"email": "Ana@Example.com ", "updated_at": "2024-01-02T10:00:00"},
        {"email": "ana@example.com", "updated_at": "2024-03-05T09:30:00Z"},
        {"email": "bob@example.com", "updated_at": "2024-02-01T00:00:00"},
    ]
    print(dedupe_by_email(rows))
    # [{'email': 'ana@example.com', 'updated_at': '2024-03-05T09:30:00Z'},
    #  {'email': 'bob@example.com', 'updated_at': '2024-02-01T00:00:00'}]
```

Notes:

- Emails are normalized with `strip().lower()` for matching only. The returned rows keep their original fields, including the original email spelling.
- Timestamps are parsed rather than compared as strings, so mixed offsets and `Z` suffixes compare correctly.
- If two rows for the same email have identical `updated_at`, the first one seen is kept.
- Naive and timezone-aware timestamps cannot be compared in Python and will raise `TypeError`. Make sure all rows use the same kind.
- Runs in O(n) time with one dict of kept rows.
