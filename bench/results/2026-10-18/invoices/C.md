```json
[
  {"id": 1, "invoice_no": "A-1043", "date": "2026-03-03", "total": 1250.00},
  {"id": 2, "invoice_no": "88231", "date": "2026-01-17", "total": 99.90},
  {"id": 3, "invoice_no": "KX/22/7", "date": "2026-04-07", "total": 3400.50},
  {"id": 4, "invoice_no": null, "date": "2026-02-02", "total": 45},
  {"id": 5, "invoice_no": "5521-B", "date": "2025-12-12", "total": 236.00},
  {"id": 6, "invoice_no": "INV-0091", "date": "2026-05-01", "total": 780.25}
]
```

Notes on the less obvious extractions:

- **Item 3:** The document labels `KX/22/7` as a "Bill ref", not an invoice number. I used it as `invoice_no` because it is the only identifier in the text. The date is read as DD/MM/YYYY, so `07/04/2026` becomes 2026-04-07. The total uses the European format, so `3.400,50` becomes 3400.50.
- **Item 4:** No invoice number appears (only "Thanks for your order!"), so `invoice_no` is null. The date is "Feb 2, 2026" and the total is $45.
- **Item 6:** The invoice date is 2026/05/01. The $780.25 is the amount paid, which I took as the total.
- **Item 2:** The total is the amount including tax, which is what the document states as TOTAL.
