# Customer Order Mart Reference

The SQLite database contains a curated order-level mart derived from the UCI source transactions.

## Relevant conventions

- One row in `orders` is one qualifying sales invoice.
- `customer_id` may be null when the source transaction cannot be linked to an identified customer.
- One customer may place many orders.
- `first_observed_order_at` is the first qualifying order visible in the available history.
- All timestamps are stored in the source system's recorded local time.
- The latest available order timestamp is recorded in `report_runs.data_through_at`.

The mart is designed for analysis. It does not contain marketing attribution, gross margin, voucher redemption, or randomized experiment assignments.
