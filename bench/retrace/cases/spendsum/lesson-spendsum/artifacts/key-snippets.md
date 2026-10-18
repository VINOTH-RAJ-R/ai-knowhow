# Key snippets from spendsum.py (copied from the project; the project itself is the source of truth)

## 1. Money as Decimal, tolerant amount parsing
```python
def parse_amount(text):
    s = text.strip().replace(",", "").replace("$", "").replace("£", "").replace("€", "")
    negative = s.startswith("(") and s.endswith(")")
    if negative:
        s = s[1:-1]
    try:
        value = Decimal(s)
    except InvalidOperation:
        raise ValueError("unrecognised amount %r" % text)
    return -value if negative else value
```
Known limit: stripping every comma assumes "." is the decimal point. "1.234,50" (European) becomes 1.2345, with no error.

## 2. Fixed date formats, loud failure
```python
DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y")
# loop over formats; if none match: raise ValueError("unrecognised date ...")
```
`MM/DD/YYYY` is deliberately unsupported: it cannot be told apart from `DD/MM/YYYY`.

## 3. First-match-wins categorisation, ordered by the rules file
```python
def categorize(description, rules):
    desc = description.lower()
    for category, keywords in rules:
        if any(k and k in desc for k in keywords):
            return category
    return UNCATEGORIZED
```
Known limit: plain substring match, so "Constraint Ltd" matches the keyword "train" and lands in Transport.

## 4. Sign convention in one line
```python
totals[date.strftime("%Y-%m")][categorize(desc, rules)] += -amount   # spent = -amount
```
Statement spending is negative, refunds positive; flipping the sign makes spending positive and lets a refund subtract from its category.

## 5. Error reporting with line numbers, clean exit code
```python
except ValueError as e:
    raise ValueError("line %d: %s" % (lineno, e))
...
except (OSError, ValueError) as e:
    print("error: %s" % e, file=sys.stderr)
    return 1
```

## 6. Test shape (14 unittest tests)
Pure-function tests (parse_date, parse_amount, categorize), summary tests against three tiny CSVs in tests/data/ (iso, dmy_commas, refund), and CLI tests via subprocess (table output, Uncategorized column, missing file gives exit code 1 and "error:" on stderr).
