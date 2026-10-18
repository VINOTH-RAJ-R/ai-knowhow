---
title: A stdlib-only Python CLI that sums bank-statement spending per category per month
lesson_format: 1
domain: software
created: 2026-10-18
built_with: "Unknown. NOTES.md records only Python 3.10.17 and the stdlib (unittest, csv, decimal, argparse). The AI model and effort used are not recorded."
difficulty: beginner
time_spent: "Not recorded. The changelog has 4 steps; the code is about 130 lines."
prerequisites: basic Python (functions, dicts, files), what a CSV is, running a command in a terminal
---

# A stdlib-only Python CLI that sums bank-statement spending per category per month

> Evidence note. This lesson was reconstructed after the fact from the finished project (`spendsum.py`, `rules.json`, `tests/`, `README.md`) and its changelog `NOTES.md`. There was no chat transcript, no prompt history and no git history. So: the decisions below are quoted from NOTES.md where it states them, and marked *(inferred)* where I am reading intent from the code. No prompts were recorded, so section 6 says so rather than inventing any.

## 1. The goal
No original request was recorded. From the program's docstring and README, the goal was:

- Read a bank-statement CSV with `date`, `description`, `amount` columns.
- Sort each transaction into a category using keyword rules the user controls.
- Print one table: one row per month, one column per category, plus a total.

Constraints visible in the record: Python 3.10, standard library only, a single-file CLI, and a rules file the user can edit without touching code.

## 2. The result
- `spendsum.py` is a single-file CLI. Usage: `python3 spendsum.py statement.csv --rules rules.json`.
- `rules.json` is an ordered map of category to keywords (Groceries, Transport, Eating Out, Bills).
- `tests/test_spendsum.py` has 14 `unittest` tests, with three tiny CSVs in `tests/data/` (`iso.csv`, `dmy_commas.csv`, `refund.csv`).
- `README.md` covers the CSV format, rules, output and tests.
- Verified by: `python3 -m unittest discover -s tests -v`. NOTES.md reports 14 tests OK on the first run. I re-ran them while writing this lesson and got the same result (`Ran 14 tests`, `OK`). NOTES.md also says the CLI was run by hand on the sample CSVs.

Key snippets are in `artifacts/key-snippets.md`.

## 3. The approach in one paragraph
Keep every piece of logic in a small importable function (`parse_date`, `parse_amount`, `load_rules`, `categorize`, `read_rows`, `summarize`, `format_table`) and keep `main()` thin. That makes each piece testable on its own. Make each ambiguous input rule explicit and simple: two fixed date formats, one amount style, first-matching-rule-wins. When input doesn't fit those rules, fail loudly with a line number instead of guessing. Use `Decimal` for money. Write tests and tiny sample CSVs alongside the code, then document the one known caveat in the README.

## 4. Step by step
These are the four steps in NOTES.md, in order.

1. **Setup and plan**
   - **What:** Created `W/tests/data`, checked `python3 --version` (3.10.17). Planned a single-file stdlib CLI, a rules file, unittest tests, sample CSVs and a README.
   - **Why now:** The design rule "logic in importable functions, thin `main()`" was fixed up front so that testing would be easy.
   - **Tool/model:** Not recorded.
   - **Output:** A plan with a file list and the design rule.
2. **Wrote the code and sample data**
   - **What:** Wrote `spendsum.py`, `rules.json` and three sample CSVs. Made six design choices, all in the decision log below.
   - **Why now:** The sample CSVs were written with the code, so each format decision had a concrete example (ISO dates, DD/MM dates with comma amounts, a refund).
   - **Output:** The working tool.
3. **Tests**
   - **What:** Wrote 14 tests in four groups: parsing (dates, amounts, bad input), categorize (priority, case, uncategorized), summary (the three sample files, missing column), and the CLI (table output, Uncategorized column, clean error and exit code 1 for a missing file). Ran them, then ran the CLI by hand.
   - **Result recorded:** `Ran 14 tests in 0.153s` and `OK`, first run, 0 failures or errors.
   - **Also recorded:** a known caveat. A positive row that matches no rule (for example salary) shows as negative spend under Uncategorized, because refunds and income look the same by sign. It was deliberately not special-cased.
4. **README**
   - **What:** Wrote usage, CSV format, rules, output and tests. The salary caveat and its workaround (add an `"Income": ["salary"]` rule) went into the README.
   - **Why last:** The behaviour was settled, so the docs could describe what actually happens.

## 5. Decision log
Rows 1 to 6 are stated in NOTES.md. The "Why" text is its wording unless marked *(inferred)*.

| # | Decision | Options considered | Why this one | Evidence |
|---|---|---|---|---|
| 1 | Money as `decimal.Decimal` | float | Float sums drift (e.g. 0.1+0.2); statements need exact cents | NOTES step 2; tests compare against `Decimal("45.20")` etc. |
| 2 | Try a fixed list of date formats: `YYYY-MM-DD`, then `DD/MM/YYYY` | auto-detect / dateutil | Stdlib only; the two formats can't be confused (4-digit year first vs slashes). Unknown formats fail with the line number | `DATE_FORMATS` in code; `test_bad_date` |
| 3 | Do NOT support `MM/DD/YYYY` | support it too | It is ambiguous with `DD/MM`, so a wrong guess would silently put spending in the wrong month *(inferred consequence; NOTES says only "ambiguous")* | README states it is unsupported; `test_ddmm_not_read_as_mmdd` |
| 4 | Strip all commas from amounts; also accept `(5.00)` and `$ £ €` | locale-aware parsing | Assumes `.` is the decimal point, as in the examples. Simple | NOTES step 2; `test_amounts`. See mistake 2 below for the cost |
| 5 | First-match-wins in `rules.json` file order, case-insensitive substring | scoring, longest-match | Simple, and the user controls priority by ordering entries | `test_first_rule_wins_and_case_insensitive` |
| 6 | Sign: `spent = -amount`; spending shown positive | show raw signed amounts | A refund (positive in the statement) naturally subtracts from its category | `refund.csv`: Groceries 75.00 = 100 - 25 |
| 7 | `python -m unittest` and a JSON rules file | pytest; YAML or TOML | `tomllib` needs Python 3.11 and the machine runs 3.10; JSON and unittest are in the stdlib | NOTES step 2 |
| 8 | Leave the salary-as-negative-spend behaviour alone | auto-detect income | Refunds and income are indistinguishable by sign; a user rule (`Income`) solves it | NOTES step 3; README Output section |
| 9 | Keep `main()` thin and logic in functions | one script body | Tests can hit each piece | NOTES step 1 |

Other options an expert might consider (not weighed in the record): a `--date-format` flag for MM/DD/YYYY and a `--decimal-comma` flag for European numbers; matching keywords on word boundaries (see mistake 1); a `--month` filter; storing money as integer cents.

## 6. Prompts that worked
**No prompts were recorded.** The project has no transcript or prompt history, so there is nothing verbatim to quote, and I won't invent any.

What the record does show is the *shape* of the instructions behind the work, because the changelog reads like a plan the builder followed:
- a stack constraint (stdlib only, Python 3.10);
- an explicit file list (`spendsum.py`, `rules.json`, `tests/`, sample CSVs, `README.md`);
- a structural rule (logic in importable functions, thin `main()`);
- a verification command (`python3 -m unittest discover -s tests -v`).

*(inferred)* If you rebuild this with an AI assistant, a prompt along those lines is the part worth copying. This is a suggestion, not a recorded prompt:

```
Build a single-file Python 3.10 CLI, standard library only, that reads a bank CSV
(date, description, amount) and prints monthly spending per category using keyword
rules from a JSON file (first match wins, file order = priority).
Rules: Decimal for money; accept YYYY-MM-DD and DD/MM/YYYY only; refunds reduce
their category; bad input must exit 1 with "error: line N: ..." on stderr.
Keep logic in small functions with a thin main(). Write unittest tests plus tiny
sample CSVs, run them, and list the behaviours you chose not to handle.
```

### A prompt that didn't work
None recorded. NOTES.md reports 0 failures or errors during development, so there was no visible re-prompting.

## 7. Mistakes and fixes
**What the record shows:** nothing failed. NOTES.md says the tests passed on the first run with 0 failures or errors, so there are no dead ends to report. Be wary of reading that as "no weaknesses": the tests only check the cases the author thought of.

While preparing this lesson I probed the tool on a copy of the project (details in `artifacts/review-probes.md`). These are **review findings, not mistakes made during the build**, and they were not fixed (I did not modify the project):

| Symptom | Root cause | Fix (not applied) | How to avoid next time |
|---|---|---|---|
| 1. `Constraint Ltd` is counted as Transport | Case-insensitive substring match: the keyword `train` is inside "cons**train**t". Same risk for `shell`, `water`, `cafe` | Match on word boundaries (e.g. regex `\bkeyword\b`) | Add a test with a near-miss description; make "keywords match inside words" an explicit, documented choice |
| 2. Amount `"1.234,50"` is read as 1.23 with no error | Decision 4: all commas are stripped, so a European decimal comma gives `1.23450`, shown as 1.23 | Reject amounts where the comma is followed by exactly one or two digits at the end, or add a `--decimal-comma` option | The README says "`1,234.50` style commas are fine" but does not say that the other style is silently wrong. A "fail loudly" policy for dates should extend to amounts. Test the *other* locale |
| 3. A salary row shows -2,000.00 spend and drags the month total negative | Sign convention (decisions 6 and 8) | Already documented: add an `Income` rule | This one was spotted and written down by the builder. Copy the habit: write each known caveat into the README the moment you find it |

Lesson: the build's own habit of failing loudly (dates, missing columns, missing file) is good. Findings 1 and 2 are the places where that rule stopped short.

## 8. Efficiency review — doing it cheaper and faster next time
- **Models and effort used:** not recorded. I can't say what was used, so I won't guess.
- **Where tokens/time went:** not recorded. From the changelog alone, the process was efficient: four steps, no retries, no debugging loop. The likely cost drivers are the code, the 14 tests and the README, each written once.
- **Cheaper path (expert suggestions, not from the record):**
  - This is small, well-specified work. A mid-tier model at low or medium effort is the sensible starting point *(inferred)*. If the `modelwise` skill is installed, ask it for the current recommendation rather than trusting a model name written here.
  - Put the design choices (stack, date formats, sign convention, rule priority) in the first prompt, as NOTES.md's plan did. Most rework in small CLIs comes from choices left open.
  - Ask the assistant for the edge cases up front, in one pass: substring-match false positives, the other decimal style, empty files. That would have caught findings 1 and 2 before the README was written.
  - Keep the changelog as you go. It is what made this lesson possible.

## 9. The reusable pattern
1. State the stack constraint and the file list first (language version, stdlib only, files wanted).
2. Make the logic small importable functions; keep the CLI wrapper thin.
3. For every input ambiguity, pick one simple rule and write it down. Refuse the ambiguous cases rather than guess (here: no MM/DD/YYYY).
4. Fail loudly and specifically: error message with the line number, non-zero exit code, errors on stderr.
5. Use exact types for money (`Decimal`, or integer cents).
6. Put user-tunable behaviour in a data file (here, ordered rules in JSON), not in code.
7. Write tiny sample inputs, one per format or behaviour, and test the pure functions and the CLI.
8. Keep a changelog of choices with their reasons, and write known caveats into the README.
9. Before calling it done, test the inputs you *didn't* design for.

## 10. Check your understanding
1. Why does `summarize` add `-amount` rather than `amount`?
   <details><summary>Answer</summary>Statements store spending as negative numbers. Flipping the sign makes spending positive in the table, and a refund (positive in the statement) then subtracts from its category. In `refund.csv`, -100.00 and +25.00 give 75.00 for Groceries.</details>
2. Why is `MM/DD/YYYY` not supported, and what happens to a date like `Jan 5 2024`?
   <details><summary>Answer</summary>`MM/DD/YYYY` can't be told apart from `DD/MM/YYYY` for days 1 to 12, so a guess could silently put spending in the wrong month. Unsupported formats raise a ValueError with the line number, and the CLI prints `error: line N: ...` and exits with 1.</details>
3. In `rules.json`, "Transport" comes before "Eating Out". A transaction reads "Shell cafe". Where does it go, and how would you make it go elsewhere?
   <details><summary>Answer</summary>Transport: the first category in file order with a matching keyword wins ("shell" matches). To change it, reorder the entries in `rules.json`, or make the keywords more specific.</details>
4. What was recorded as a known limitation, and what unrecorded limitation can you demonstrate?
   <details><summary>Answer</summary>Recorded: a positive row matching no rule (salary) appears as negative spend under Uncategorized; add an `Income` rule. Unrecorded (found in review): keywords match inside words, so "Constraint Ltd" matches "train"; and a European-style amount like "1.234,50" is silently read as 1.23.</details>
5. **Scenario:** A bank gives you amounts like `1.234,50` and dates like `31.01.2024`. What would you do?
   <details><summary>Answer</summary>Don't just widen the parsing blindly. First add failing tests built from real sample rows. Then add an explicit option for the decimal-comma style and add `%d.%m.%Y` to `DATE_FORMATS` (unambiguous, since the dots and the order differ from the other formats). Keep the "fail loudly" rule: reject any amount whose style you can't classify, instead of stripping commas and hoping.</details>

## 11. Try it yourself
Rebuild the core in 30 to 45 minutes.

- **Task:** Write a script that reads a CSV with `date,description,amount`, takes a JSON rules file (category to keywords, first match wins), and prints spending per category per month. Use `Decimal`, accept `YYYY-MM-DD` only, and exit 1 with a line number for bad rows.
- **Hint:** Write `parse_amount`, `categorize` and `summarize` as separate functions first; test them with two 3-row CSVs (one with a refund) before writing `main()`.
- **Stretch:** Add a test with a description like `Constraint Ltd` and make word-boundary matching pass it.
- **Done when:** your tests pass, a bad date exits 1 with `error: line N: ...` on stderr, a refund reduces its category, and the README states which inputs you refuse.
