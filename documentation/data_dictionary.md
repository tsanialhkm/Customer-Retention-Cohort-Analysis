# Case Data Dictionary

## `orders`

Grain: one row per qualifying sales invoice.

| Column | Type | Meaning |
|---|---|---|
| `order_id` | TEXT | Source invoice identifier |
| `customer_id` | INTEGER, nullable | Identified customer when available |
| `ordered_at` | TIMESTAMP | Earliest source timestamp on the invoice |
| `country` | TEXT | Country recorded on the invoice |
| `order_value_gbp` | REAL | Sum of qualifying quantity multiplied by unit price |
| `units` | INTEGER | Total qualifying units |
| `distinct_products` | INTEGER | Distinct stock codes on the order |
| `line_count` | INTEGER | Qualifying source lines on the order |

## `customer_accounts`

Grain: one row per identified customer in the available history.

| Column | Type | Meaning |
|---|---|---|
| `customer_id` | INTEGER | Customer identifier |
| `home_country` | TEXT | Most frequently observed order country |
| `first_observed_order_at` | TIMESTAMP | Earliest qualifying order timestamp in available history |
| `first_observed_order_id` | TEXT | Identifier of the earliest qualifying order |

## `report_runs`

Grain: one row per dashboard generation event.

| Column | Type | Meaning |
|---|---|---|
| `report_id` | TEXT | Report-run identifier |
| `dashboard_name` | TEXT | Dashboard title |
| `generated_at` | TIMESTAMP | Time the report was generated |
| `data_through_at` | TIMESTAMP | Latest available order timestamp |

## `crm_dashboard_snapshot`

Grain: one row per acquisition month in the saved dashboard snapshot.

| Column | Type | Meaning |
|---|---|---|
| `report_id` | TEXT | Links the snapshot to `report_runs` |
| `cohort_month` | TEXT | Month of first observed qualifying order |
| `cohort_customers` | INTEGER | Identified customers in the cohort |
| `repeat_customers_as_of_run` | INTEGER | Customers with another visible qualifying order |
| `displayed_repeat_rate` | REAL | Dashboard numerator divided by denominator |

## `schema_notes`

A database view documenting the grain of each analytical object.
