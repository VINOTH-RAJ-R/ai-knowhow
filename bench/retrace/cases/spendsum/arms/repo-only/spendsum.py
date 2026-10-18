#!/usr/bin/env python3
"""spendsum - monthly spending per category from a bank-statement CSV.

Usage:
    python3 spendsum.py statement.csv --rules rules.json
"""
import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation

UNCATEGORIZED = "Uncategorized"
DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y")


def parse_date(text):
    """Parse YYYY-MM-DD or DD/MM/YYYY into a date. Raises ValueError otherwise."""
    text = text.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError("unrecognised date %r (expected YYYY-MM-DD or DD/MM/YYYY)" % text)


def parse_amount(text):
    """Parse '1,234.50', '-12.00', '(5.00)', '$3' into a Decimal."""
    s = text.strip().replace(",", "").replace("$", "").replace("£", "").replace("€", "")
    negative = s.startswith("(") and s.endswith(")")
    if negative:
        s = s[1:-1]
    try:
        value = Decimal(s)
    except InvalidOperation:
        raise ValueError("unrecognised amount %r" % text)
    return -value if negative else value


def load_rules(path):
    """Rules file: {"Category": ["keyword", ...], ...}. Order = priority."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("rules file must be a JSON object of category -> keyword list")
    rules = []
    for category, keywords in data.items():
        if isinstance(keywords, str):
            keywords = [keywords]
        rules.append((category, [k.lower() for k in keywords]))
    return rules


def categorize(description, rules):
    """First category (in file order) with a keyword found in description wins."""
    desc = description.lower()
    for category, keywords in rules:
        if any(k and k in desc for k in keywords):
            return category
    return UNCATEGORIZED


def read_rows(path):
    """Yield (date, description, amount). Needs date, description, amount columns."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV is empty")
        cols = {name.strip().lower(): name for name in reader.fieldnames}
        missing = [c for c in ("date", "description", "amount") if c not in cols]
        if missing:
            raise ValueError("CSV missing column(s): %s (found: %s)"
                             % (", ".join(missing), ", ".join(reader.fieldnames)))
        for lineno, row in enumerate(reader, start=2):
            try:
                yield (parse_date(row[cols["date"]]),
                       row[cols["description"]] or "",
                       parse_amount(row[cols["amount"]]))
            except ValueError as e:
                raise ValueError("line %d: %s" % (lineno, e))


def summarize(rows, rules):
    """Return {month 'YYYY-MM': {category: spent}} where spent is positive for spending.

    Spending is negative in the statement and refunds positive, so spent = -amount;
    a refund therefore reduces its category. Income-like positive rows that match no
    rule land in Uncategorized as negative spend, which is the honest net figure.
    """
    totals = defaultdict(lambda: defaultdict(Decimal))
    for date, desc, amount in rows:
        totals[date.strftime("%Y-%m")][categorize(desc, rules)] += -amount
    return totals


def format_table(totals):
    months = sorted(totals)
    cats = sorted({c for m in totals.values() for c in m} - {UNCATEGORIZED})
    if UNCATEGORIZED in {c for m in totals.values() for c in m}:
        cats.append(UNCATEGORIZED)
    header = ["Month"] + cats + ["Total"]
    table = [header]
    for m in months:
        vals = [totals[m].get(c, Decimal("0")) for c in cats]
        table.append([m] + ["{:,.2f}".format(v) for v in vals] + ["{:,.2f}".format(sum(vals))])
    widths = [max(len(r[i]) for r in table) for i in range(len(header))]
    lines = []
    for i, r in enumerate(table):
        lines.append("  ".join(c.ljust(widths[0]) if j == 0 else c.rjust(widths[j])
                               for j, c in enumerate(r)))
        if i == 0:
            lines.append("  ".join("-" * w for w in widths))
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description="Spending per category per month from a bank CSV.")
    p.add_argument("csv", help="bank statement CSV (columns: date, description, amount)")
    p.add_argument("--rules", required=True, help="JSON file mapping category -> keywords")
    args = p.parse_args(argv)
    try:
        rules = load_rules(args.rules)
        totals = summarize(read_rows(args.csv), rules)
    except (OSError, ValueError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 1
    if not totals:
        print("No transactions found.")
        return 0
    print(format_table(totals))
    return 0


if __name__ == "__main__":
    sys.exit(main())
