# NOTES - spendsum engineering changelog

## Step 1 - Setup
- Ran: `mkdir -p W/tests/data`; `python3 --version`
- Plan: single-file CLI `spendsum.py` (stdlib only), `rules.json`, `tests/test_spendsum.py` (unittest), small sample CSVs in `tests/data/`, README.md.
- Design: keep logic in importable functions (parse_date, parse_amount, categorize, summarize, format_table) and a thin `main()` so tests can hit each piece.
Python 3.10.17

## Step 2 - Wrote spendsum.py, rules.json, sample CSVs
- Files: `spendsum.py`, `rules.json`, `tests/data/{iso,dmy_commas,refund}.csv`.
- Design choices:
  - Chose `decimal.Decimal` over float for money because float sums drift (e.g. 0.1+0.2) and statements need exact cents.
  - Chose trying a fixed list of date formats (YYYY-MM-DD, then DD/MM/YYYY) over auto-detect/dateutil: stdlib only, and the two formats can't be confused (4-digit year first vs. slashes). Did NOT support MM/DD/YYYY because it is ambiguous with DD/MM; unknown formats fail loudly with the line number.
  - Chose strip-all-commas for amounts (assumes `.` is the decimal point as in the examples); also accepts `(5.00)` and currency symbols.
  - Chose first-match-wins in rules.json file order (JSON objects keep order) over scoring/longest-match: simple and the user controls priority by ordering. Case-insensitive substring match.
  - Sign: spent = -amount, so refunds (positive) subtract from their category. Table shows spending as positive numbers.
  - Chose `python -m unittest` + a JSON rules file (not YAML/TOML: tomllib needs 3.11, we run 3.10).

## Step 3 - Tests
- Wrote `tests/test_spendsum.py` (14 tests: date formats, DD/MM vs MM/DD, comma/paren amounts, rule priority, uncategorized, refund, missing column, CLI table, CLI error exit code).
- Ran: `python3 -m unittest discover -s tests -v`
- Result: `Ran 14 tests in 0.153s` / `OK`. Passed on the first run; 0 failures, 0 errors encountered during development.
- Also ran the CLI by hand on the sample CSVs; output looked right (refund sample: Groceries 75.00 = 100 - 25).
- Known caveat (documented in README): positive rows matching no rule (salary) show as negative spend in Uncategorized, because refunds and income are indistinguishable by sign. Chose not to special-case it; user can add an "Income" rule.

## Step 4 - README
- Wrote `README.md` (usage, CSV format, rules, output, tests).
- Final: all 14 tests pass; 0 failures/errors along the way.
