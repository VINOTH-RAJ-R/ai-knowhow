```json
[
  { "id": 1, "invoice_no": "A-1043",   "date": "2026-03-03", "total": 1250.00 },
  { "id": 2, "invoice_no": "88231",    "date": "2026-01-17", "total": 99.90 },
  { "id": 3, "invoice_no": "KX/22/7",  "date": "2026-04-07", "total": 3400.50 },
  { "id": 4, "invoice_no": null,       "date": "2026-02-02", "total": 45 },
  { "id": 5, "invoice_no": "5521-B",   "date": "2025-12-12", "total": 236.00 },
  { "id": 6, "invoice_no": "INV-0091", "date": "2026-05-01", "total": 780.25 }
]
```

How I handled the unclear ones:

- **#3**: I read the date as DD/MM, as the text says, so 07/04/2026 becomes 7 April. The total is in European format, where "3.400,50" means 3400.50.
- **#4**: No invoice number is given, so it's `null`. The only date is the order date, so I used that. Change it to `null` if you only want true invoice dates.
- **#5**: I used the total (236.00), not the subtotal.
- **#6**: I used the invoice date (2026-05-01), not the payment date (2026-05-30).
- **Currency** isn't in the output. #3 is in EUR and the others are in USD. Add a `currency` key if you need to tell them apart.
