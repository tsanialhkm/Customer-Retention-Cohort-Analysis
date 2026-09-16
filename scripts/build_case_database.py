"""Build the spoiler-free SQLite data package for Case 002.

Source:
    UCI Machine Learning Repository, Online Retail II
    https://archive.ics.uci.edu/dataset/502/online+retail+ii

Usage:
    python scripts/build_case_database.py --source /path/to/online_retail_II.xlsx
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd


SHEETS = ("Year 2009-2010", "Year 2010-2011")
REPORT_ID = "CRM-2011-12-09"
REPORT_GENERATED_AT = "2011-12-09 15:00:00"
COHORT_MONTHS = ("2011-07", "2011-08", "2011-09", "2011-10", "2011-11")


def normalize_id(value: object) -> str:
    if pd.isna(value):
        raise ValueError("Invoice identifier cannot be null.")
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def first_non_null(series: pd.Series) -> int | None:
    values = series.dropna()
    if values.empty:
        return None
    return int(values.iloc[0])


def mode_or_first(series: pd.Series) -> str:
    values = series.dropna().astype(str)
    modes = values.mode()
    if not modes.empty:
        return str(modes.iloc[0])
    return str(values.iloc[0])


def load_source(source_path: Path) -> pd.DataFrame:
    frames = []
    for sheet_name in SHEETS:
        frame = pd.read_excel(source_path, sheet_name=sheet_name)
        frame["source_sheet"] = sheet_name
        frames.append(frame)

    source = pd.concat(frames, ignore_index=True)
    source["invoice_id"] = source["Invoice"].map(normalize_id)
    source["customer_id"] = pd.to_numeric(
        source["Customer ID"], errors="coerce"
    ).astype("Int64")
    source["ordered_at"] = pd.to_datetime(source["InvoiceDate"])
    source["quantity"] = pd.to_numeric(source["Quantity"], errors="raise")
    source["unit_price_gbp"] = pd.to_numeric(source["Price"], errors="raise")
    source["line_amount_gbp"] = source["quantity"] * source["unit_price_gbp"]
    source["stock_code"] = source["StockCode"].astype(str).str.strip()
    source["country"] = source["Country"].astype(str).str.strip()
    return source


def build_orders(source: pd.DataFrame) -> pd.DataFrame:
    qualifying_lines = source[
        (~source["invoice_id"].str.upper().str.startswith("C"))
        & (source["quantity"] > 0)
        & (source["unit_price_gbp"] > 0)
    ].copy()

    orders = (
        qualifying_lines.groupby("invoice_id", as_index=False)
        .agg(
            customer_id=("customer_id", first_non_null),
            ordered_at=("ordered_at", "min"),
            country=("country", mode_or_first),
            order_value_gbp=("line_amount_gbp", "sum"),
            units=("quantity", "sum"),
            distinct_products=("stock_code", "nunique"),
            line_count=("stock_code", "size"),
        )
        .sort_values(["ordered_at", "invoice_id"])
        .reset_index(drop=True)
    )

    orders["customer_id"] = orders["customer_id"].astype("Int64")
    orders["order_value_gbp"] = orders["order_value_gbp"].round(2)

    if orders["invoice_id"].duplicated().any():
        raise ValueError("Expected one row per invoice_id.")

    return orders


def build_customers(orders: pd.DataFrame) -> pd.DataFrame:
    identified = orders[orders["customer_id"].notna()].copy()
    identified = identified.sort_values(
        ["customer_id", "ordered_at", "invoice_id"]
    )

    first_orders = identified.groupby("customer_id", as_index=False).first()[
        ["customer_id", "invoice_id", "ordered_at"]
    ]
    first_orders = first_orders.rename(
        columns={
            "invoice_id": "first_observed_order_id",
            "ordered_at": "first_observed_order_at",
        }
    )

    countries = (
        identified.groupby("customer_id")["country"]
        .agg(mode_or_first)
        .rename("home_country")
        .reset_index()
    )

    customers = first_orders.merge(countries, on="customer_id", how="left")
    customers["customer_id"] = customers["customer_id"].astype(int)
    return customers.sort_values("customer_id").reset_index(drop=True)


def build_dashboard_snapshot(
    orders: pd.DataFrame, customers: pd.DataFrame
) -> pd.DataFrame:
    identified = orders[orders["customer_id"].notna()].copy()
    order_counts = identified.groupby("customer_id")["invoice_id"].nunique()
    repeated_ids = set(order_counts[order_counts >= 2].index.astype(int))

    snapshot = customers.copy()
    snapshot["cohort_month"] = snapshot["first_observed_order_at"].dt.strftime(
        "%Y-%m"
    )
    snapshot["repeated_as_of_run"] = snapshot["customer_id"].isin(repeated_ids)
    snapshot = snapshot[snapshot["cohort_month"].isin(COHORT_MONTHS)]

    result = (
        snapshot.groupby("cohort_month", as_index=False)
        .agg(
            cohort_customers=("customer_id", "size"),
            repeat_customers_as_of_run=("repeated_as_of_run", "sum"),
        )
        .sort_values("cohort_month")
    )
    result["displayed_repeat_rate"] = (
        result["repeat_customers_as_of_run"] / result["cohort_customers"]
    ).round(4)
    result.insert(0, "report_id", REPORT_ID)
    return result


def write_sqlite(
    database_path: Path,
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    dashboard: pd.DataFrame,
) -> None:
    if database_path.exists():
        database_path.unlink()

    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON;")
    connection.executescript(
        """
        CREATE TABLE customer_accounts (
            customer_id INTEGER PRIMARY KEY,
            home_country TEXT NOT NULL,
            first_observed_order_at TEXT NOT NULL,
            first_observed_order_id TEXT NOT NULL
        );

        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id INTEGER,
            ordered_at TEXT NOT NULL,
            country TEXT NOT NULL,
            order_value_gbp REAL NOT NULL,
            units INTEGER NOT NULL,
            distinct_products INTEGER NOT NULL,
            line_count INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customer_accounts(customer_id)
        );

        CREATE TABLE report_runs (
            report_id TEXT PRIMARY KEY,
            dashboard_name TEXT NOT NULL,
            generated_at TEXT NOT NULL,
            data_through_at TEXT NOT NULL
        );

        CREATE TABLE crm_dashboard_snapshot (
            report_id TEXT NOT NULL,
            cohort_month TEXT NOT NULL,
            cohort_customers INTEGER NOT NULL,
            repeat_customers_as_of_run INTEGER NOT NULL,
            displayed_repeat_rate REAL NOT NULL,
            PRIMARY KEY (report_id, cohort_month),
            FOREIGN KEY (report_id) REFERENCES report_runs(report_id)
        );

        CREATE VIEW schema_notes AS
        SELECT 'orders' AS object_name,
               'table' AS object_type,
               'One row per qualifying sales invoice' AS grain
        UNION ALL
        SELECT 'customer_accounts', 'table',
               'One row per identified customer in the available history'
        UNION ALL
        SELECT 'report_runs', 'table',
               'One row per dashboard generation event'
        UNION ALL
        SELECT 'crm_dashboard_snapshot', 'table',
               'One row per acquisition month in a dashboard snapshot';
        """
    )

    customer_rows = [
        (
            int(row.customer_id),
            row.home_country,
            row.first_observed_order_at.strftime("%Y-%m-%d %H:%M:%S"),
            row.first_observed_order_id,
        )
        for row in customers.itertuples(index=False)
    ]
    connection.executemany(
        """
        INSERT INTO customer_accounts (
            customer_id,
            home_country,
            first_observed_order_at,
            first_observed_order_id
        ) VALUES (?, ?, ?, ?);
        """,
        customer_rows,
    )

    order_rows = [
        (
            row.invoice_id,
            None if pd.isna(row.customer_id) else int(row.customer_id),
            row.ordered_at.strftime("%Y-%m-%d %H:%M:%S"),
            row.country,
            float(row.order_value_gbp),
            int(row.units),
            int(row.distinct_products),
            int(row.line_count),
        )
        for row in orders.itertuples(index=False)
    ]
    connection.executemany(
        """
        INSERT INTO orders (
            order_id,
            customer_id,
            ordered_at,
            country,
            order_value_gbp,
            units,
            distinct_products,
            line_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        order_rows,
    )

    data_through_at = orders["ordered_at"].max().strftime("%Y-%m-%d %H:%M:%S")
    connection.execute(
        """
        INSERT INTO report_runs (
            report_id,
            dashboard_name,
            generated_at,
            data_through_at
        ) VALUES (?, ?, ?, ?);
        """,
        (
            REPORT_ID,
            "New Customer Repeat Purchase",
            REPORT_GENERATED_AT,
            data_through_at,
        ),
    )

    dashboard_rows = [
        (
            row.report_id,
            row.cohort_month,
            int(row.cohort_customers),
            int(row.repeat_customers_as_of_run),
            float(row.displayed_repeat_rate),
        )
        for row in dashboard.itertuples(index=False)
    ]
    connection.executemany(
        """
        INSERT INTO crm_dashboard_snapshot (
            report_id,
            cohort_month,
            cohort_customers,
            repeat_customers_as_of_run,
            displayed_repeat_rate
        ) VALUES (?, ?, ?, ?, ?);
        """,
        dashboard_rows,
    )

    connection.executescript(
        """
        CREATE INDEX idx_orders_customer_time
            ON orders (customer_id, ordered_at);
        CREATE INDEX idx_orders_time
            ON orders (ordered_at);
        CREATE INDEX idx_orders_country
            ON orders (country);
        """
    )
    connection.commit()
    connection.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()

    source = load_source(args.source)
    orders = build_orders(source)
    customers = build_customers(orders)
    dashboard = build_dashboard_snapshot(orders, customers)

    data_dir = args.project_root / "data"
    derived_dir = data_dir / "derived"
    evidence_dir = args.project_root / "evidence"
    derived_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)

    orders_export = orders.rename(columns={"invoice_id": "order_id"}).copy()
    orders_export["ordered_at"] = orders_export["ordered_at"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    orders_export.to_csv(derived_dir / "orders.csv", index=False)

    customers_export = customers.copy()
    customers_export["first_observed_order_at"] = customers_export[
        "first_observed_order_at"
    ].dt.strftime("%Y-%m-%d %H:%M:%S")
    customers_export.to_csv(
        derived_dir / "customer_accounts.csv", index=False
    )

    dashboard.to_csv(
        evidence_dir / "06_crm_dashboard_export.csv", index=False
    )

    write_sqlite(
        data_dir / "alder_finch_case_002.db",
        orders,
        customers,
        dashboard,
    )

    print(f"Source rows: {len(source):,}")
    print(f"Orders: {len(orders):,}")
    print(f"Identified customers: {len(customers):,}")
    print(dashboard.to_string(index=False))


if __name__ == "__main__":
    main()
