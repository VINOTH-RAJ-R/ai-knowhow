# spendsum

Monthly spending per category from a bank-statement CSV. Python 3, standard library only.

    python3 spendsum.py statement.csv --rules rules.json

## CSV format
Header row with columns `date`, `description`, `amount` (case-insensitive, any order, extra columns ignored).
- Dates: `YYYY-MM-DD` or `DD/MM/YYYY` (can be mixed). `MM/DD/YYYY` is not supported.
- Amounts: `1,234.50` style commas are fine. Spending is negative, refunds positive.

## Rules (`rules.json`)
    {"Groceries": ["tesco", "aldi"], "Transport": ["uber", "train"]}
A transaction goes to the first category (in file order) whose keyword appears in its description
(case-insensitive substring). No match goes to `Uncategorized`. Reorder entries to change priority.

## Output
One row per month, one column per category plus `Total`. Spending shows as positive numbers; a refund
reduces its category. Note: a positive row with no matching rule (e.g. salary) shows as negative
spend in `Uncategorized`; add a rule such as `"Income": ["salary"]` to separate it.

## Tests
    python3 -m unittest discover -s tests -v
