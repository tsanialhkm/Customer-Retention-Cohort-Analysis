# Transformation Notes

The case data was derived deterministically from both worksheets in the UCI Online Retail II workbook.

## Qualifying sales lines

A source line was retained for the order-level dataset when:

- the invoice identifier did not begin with `C`;
- quantity was greater than zero;
- unit price was greater than zero.

Cancellation, reversal, zero-value, and negative-price lines are outside the retention event definition for this case.

## Orders

Qualifying lines were aggregated by invoice identifier. Each row in `orders` represents one qualifying sales invoice.

The following fields were derived:

- `order_value_gbp`: sum of quantity multiplied by unit price;
- `units`: total units across qualifying lines;
- `distinct_products`: distinct stock codes;
- `line_count`: qualifying source lines.

Orders with a missing source customer identifier are retained with a null `customer_id`.

## Customer accounts

`customer_accounts` contains one row per identified customer. The first observed order is the earliest qualifying order for that customer within the available source history.

“First observed” does not prove that the customer had never purchased before the dataset began.

## Reproducibility

The transformation is implemented in `scripts/build_case_database.py`. The SQLite database is already included, so running the script is not required to investigate the case.
