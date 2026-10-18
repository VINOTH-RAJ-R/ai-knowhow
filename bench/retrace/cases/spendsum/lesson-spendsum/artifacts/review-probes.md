# Probes run while writing this lesson (not part of the original build)

Run on a copy of the project, Python 3, nothing in the original project modified. Original 14 tests: Ran 14 tests, OK.

| Input row | Result | Meaning |
|---|---|---|
| `Constraint Ltd,-5` with rules.json | counted under Transport | substring false positive on "train" |
| `Salary,2000.00` (no Income rule) | Uncategorized -2,000.00, month total -1,965.00 | documented caveat; income looks like negative spend |
| `"1.234,50"` (European number) | -1.23 in Uncategorized, no error | silent wrong number; comma-stripping assumes US format |
| `03/04/2024` | 2024-04 (3 April) | DD/MM reading, as documented |

Only the salary caveat is recorded in NOTES.md/README. The other two are findings from this review.
