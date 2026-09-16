# Data Source

## Original dataset

**Online Retail II**, UCI Machine Learning Repository

- Creator: Daqing Chen
- DOI: https://doi.org/10.24432/C5CG6D
- Source: https://archive.ics.uci.edu/dataset/502/online%2Bretail%2Bii
- Original file: `online_retail_II.xlsx`
- Original rows: 1,067,371
- Original period: 1 December 2009 through 9 December 2011
- License: CC BY 4.0

The UCI repository describes the source as real transactions from a UK-based, registered, non-store retailer that mainly sells giftware and serves many wholesale customers.

## Files included in this case

- `alder_finch_case_002.db`: SQLite investigation database.
- `derived/orders.csv`: order-level extract used in the database.
- `derived/customer_accounts.csv`: identified-customer dimension derived from the available history.

The complete original workbook can be downloaded from the UCI source page. It is not duplicated in this repository because the case includes the required derived data and a reproducible build script.
