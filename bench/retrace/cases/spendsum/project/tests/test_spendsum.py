import os
import subprocess
import sys
import unittest
from datetime import date
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import spendsum  # noqa: E402

DATA = os.path.join(HERE, "data")
RULES = os.path.join(ROOT, "rules.json")


def totals_for(name):
    rules = spendsum.load_rules(RULES)
    return spendsum.summarize(spendsum.read_rows(os.path.join(DATA, name)), rules)


class ParseTests(unittest.TestCase):
    def test_both_date_formats(self):
        self.assertEqual(spendsum.parse_date("2024-01-05"), date(2024, 1, 5))
        self.assertEqual(spendsum.parse_date("05/01/2024"), date(2024, 1, 5))

    def test_ddmm_not_read_as_mmdd(self):
        self.assertEqual(spendsum.parse_date("13/02/2024"), date(2024, 2, 13))

    def test_bad_date(self):
        with self.assertRaises(ValueError):
            spendsum.parse_date("Jan 5 2024")

    def test_amounts(self):
        self.assertEqual(spendsum.parse_amount("-1,234.50"), Decimal("-1234.50"))
        self.assertEqual(spendsum.parse_amount("25.00"), Decimal("25.00"))
        self.assertEqual(spendsum.parse_amount("(5.00)"), Decimal("-5.00"))

    def test_bad_amount(self):
        with self.assertRaises(ValueError):
            spendsum.parse_amount("abc")


class CategorizeTests(unittest.TestCase):
    def test_first_rule_wins_and_case_insensitive(self):
        rules = [("A", ["foo"]), ("B", ["foo", "bar"])]
        self.assertEqual(spendsum.categorize("FOO bar", rules), "A")
        self.assertEqual(spendsum.categorize("BAR", rules), "B")

    def test_uncategorized(self):
        self.assertEqual(spendsum.categorize("zzz", [("A", ["foo"])]), "Uncategorized")


class SummaryTests(unittest.TestCase):
    def test_iso_dates(self):
        t = totals_for("iso.csv")
        self.assertEqual(t["2024-01"]["Groceries"], Decimal("45.20"))
        self.assertEqual(t["2024-01"]["Transport"], Decimal("12.00"))
        self.assertEqual(t["2024-02"]["Uncategorized"], Decimal("7.50"))

    def test_dmy_dates_and_comma_amounts(self):
        t = totals_for("dmy_commas.csv")
        self.assertEqual(t["2024-01"]["Bills"], Decimal("1234.50"))
        self.assertEqual(t["2024-01"]["Groceries"], Decimal("20.00"))
        self.assertEqual(t["2024-02"]["Groceries"], Decimal("30.00"))

    def test_refund_reduces_category(self):
        t = totals_for("refund.csv")
        self.assertEqual(t["2024-03"]["Groceries"], Decimal("75.00"))

    def test_missing_column(self):
        bad = os.path.join(DATA, "_bad.csv")
        with open(bad, "w") as f:
            f.write("Date,Memo\n2024-01-01,x\n")
        try:
            with self.assertRaises(ValueError):
                list(spendsum.read_rows(bad))
        finally:
            os.remove(bad)


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, os.path.join(ROOT, "spendsum.py"), *args],
                              capture_output=True, text=True)

    def test_table_output(self):
        r = self.run_cli(os.path.join(DATA, "refund.csv"), "--rules", RULES)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("2024-03", r.stdout)
        self.assertIn("Groceries", r.stdout)
        self.assertIn("75.00", r.stdout)

    def test_uncategorized_column(self):
        r = self.run_cli(os.path.join(DATA, "iso.csv"), "--rules", RULES)
        self.assertIn("Uncategorized", r.stdout)

    def test_missing_file_is_clean_error(self):
        r = self.run_cli("nope.csv", "--rules", RULES)
        self.assertEqual(r.returncode, 1)
        self.assertIn("error:", r.stderr)


if __name__ == "__main__":
    unittest.main()
