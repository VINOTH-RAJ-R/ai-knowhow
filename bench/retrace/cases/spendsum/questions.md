1. Why does spendsum use decimal.Decimal rather than float for amounts?
2. The tool accepts YYYY-MM-DD and DD/MM/YYYY dates but deliberately not MM/DD/YYYY, and does not use auto-detection such as dateutil. Why?
3. How are categories assigned to transactions, and why was this chosen over scoring or longest-match approaches?
4. Why is the rules file JSON rather than YAML or TOML, and why does the project use unittest instead of pytest?
5. A statement contains a positive row 'SALARY ACME 2,000.00' and no rule matches it. What does the output show, why, and how should a user fix it?
6. What happens if one CSV row has an unparseable date such as 'Jan 5 2024', or the CSV is missing the 'amount' column? What does the user see and what is the exit code?
7. How was spendsum verified, and what does the test suite cover beyond happy-path parsing?
8. Why is the code structured as importable functions plus a thin main(), and how do the tests use that? Which tests exercise the CLI as a real subprocess?
9. A teammate reports that 'Uber Eats' dinners show up under Transport instead of Eating Out. What would you do, and why does that fix work?
10. A bank exports dates as 03/25/2024 (MM/DD/YYYY) and the tool fails. A colleague suggests adding MM/DD/YYYY to DATE_FORMATS. What do you do?