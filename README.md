# The Retention Mirage

## Customer Cohort Analysis and Campaign Decision

An SQL business-analysis project investigating whether an apparent decline in customer retention was real or caused by a misleading KPI.

| Project detail | Value |
|---|---|
| Role | Business Analyst |
| Tools | SQL, SQLite, VS Code, SQLTools |
| Analysis type | Cohort analysis, KPI validation, root-cause analysis |
| Dataset | UCI Online Retail II |
| Final decision | Do not approve the GBP 30,000 campaign as proposed |

## Executive summary

Marketing reported that repeat purchase rate for newly acquired customers fell from **72.55% in July 2011** to **28.80% in November 2011**. Based on this apparent decline, the team requested **GBP 30,000** for an emergency voucher campaign.

I reproduced the dashboard successfully, but found that its monthly cohorts were not directly comparable. A customer was classified as repeated if any later order was visible by the report cutoff, regardless of how much time had passed since acquisition. July customers therefore had several months to repeat, while November customers had only days or weeks.

After replacing the cumulative metric with a fixed **30-day repeat purchase rate**, the mature July–October cohorts no longer showed a consistent downward trend. The available data also contained no experiment, margin assumption, or evidence that vouchers would generate incremental purchases.

**Recommendation:** do not approve the full campaign in its current form. If Marketing wants to test the idea, run a limited randomized pilot and evaluate incremental repeat purchases and contribution margin.

## Business problem

The Managing Director asked the analysis to answer:

1. Can the CRM dashboard figures be reproduced?
2. What population, numerator, denominator, and reporting cutoff does the KPI use?
3. Are monthly acquisition cohorts directly comparable?
4. What does a fair retention comparison show?
5. How much of the order population can be linked to an identified customer?
6. Should the proposed voucher campaign be approved?
7. What KPI and control process should replace the current approach?

## Dataset

The company, stakeholders, dashboard, and campaign proposal are fictional. The underlying transactions come from the real **Online Retail II** dataset published by the UCI Machine Learning Repository.

| Item | Value |
|---|---:|
| Original transaction rows | 1,067,371 |
| Derived qualifying orders | 40,077 |
| Identified customers | 5,878 |
| Source period | 1 December 2009–9 December 2011 |

The source contains transactions from a UK-based non-store retailer. For this project, qualifying sales lines were restricted to completed invoices with positive quantity and unit price, then aggregated to one row per invoice.

### Analytical tables

| Table | Grain | Purpose |
|---|---|---|
| `orders` | One qualifying sales invoice | Order activity and value |
| `customer_accounts` | One identified customer | First observed order and customer cohort |
| `report_runs` | One dashboard run | Report generation time and data cutoff |
| `crm_dashboard_snapshot` | One cohort month per report | Published CRM figures |

## Metric contract

### Original CRM metric

| Component | Definition |
|---|---|
| Population | Identified customers grouped by month of first observed qualifying order |
| Numerator | Customers with at least one other qualifying order visible by the report cutoff |
| Denominator | All identified customers in the acquisition cohort |
| Observation window | Variable and unspecified |
| Data cutoff | Latest order available when the dashboard was generated |

The calculation was mathematically reproducible, but the observation window was longer for older cohorts.

### Replacement metric

> **30-day repeat purchase rate:** percentage of identified new customers who place another qualifying order within 30 days of their first observed qualifying order.

Only customers whose complete 30-day window is present by the data cutoff are eligible. A monthly cohort should be used for direct comparison only after the entire cohort has matured.

## Analysis

### 1. Dashboard reproduction

The published CRM values were reproduced exactly.

| Cohort | Customers | Repeated by report cutoff | Dashboard rate |
|---|---:|---:|---:|
| July 2011 | 102 | 74 | 72.55% |
| August 2011 | 106 | 63 | 59.43% |
| September 2011 | 189 | 104 | 55.03% |
| October 2011 | 221 | 94 | 42.53% |
| November 2011 | 191 | 55 | 28.80% |

The downward line was real in the saved dashboard, but it did not measure each cohort over an equal amount of time.

### 2. Comparable 30-day retention

| Cohort | Full cohort | 30-day eligible | Repeated within 30 days | 30-day rate | Comparison status |
|---|---:|---:|---:|---:|---|
| July 2011 | 102 | 102 | 30 | 29.41% | Mature |
| August 2011 | 106 | 106 | 19 | 17.92% | Mature |
| September 2011 | 189 | 189 | 44 | 23.28% | Mature |
| October 2011 | 221 | 221 | 63 | 28.51% | Mature |
| November 2011 | 191 | 58 | 18 | 31.03% | Partial; not directly comparable |

Among the fully matured July–October cohorts, retention falls in August and then recovers in September and October. This does **not** support Marketing's claim of five consecutive months of deteriorating customer quality.

The November value is shown for transparency, but it represents only the 58 customers acquired early enough to complete a 30-day observation window. It must not be interpreted as the result for the entire November cohort.

### 3. Customer identification coverage

Retention can only be calculated for orders linked to a customer identifier.

| Month | Total orders | Identified orders | Order coverage | Identified value coverage |
|---|---:|---:|---:|---:|
| July 2011 | 1,475 | 1,331 | 90.24% | 83.44% |
| August 2011 | 1,361 | 1,280 | 94.05% | 85.01% |
| September 2011 | 1,837 | 1,755 | 95.54% | 90.01% |
| October 2011 | 2,040 | 1,929 | 94.56% | 89.99% |
| November 2011 | 2,769 | 2,657 | 95.96% | 76.97% |

Across the full dataset, **92.24% of qualifying orders** and **84.60% of qualifying order value** are linked to an identified customer. The retention KPI therefore describes identified customers rather than the entire purchasing population. November's lower value coverage is an additional reason to avoid broad conclusions about overall customer value.

## Core SQL

The following query creates a customer-level 30-day eligibility and repeat flag. A different invoice at the same recorded timestamp is treated as another order by comparing `order_id` with `first_observed_order_id`.

```sql
WITH report_cutoff AS (
    SELECT MAX(data_through_at) AS data_through_at
    FROM report_runs
),

cohort_customers AS (
    SELECT
        c.customer_id,
        c.first_observed_order_id,
        c.first_observed_order_at,
        strftime('%Y-%m', c.first_observed_order_at) AS cohort_month,
        CASE
            WHEN datetime(c.first_observed_order_at, '+30 days')
                 <= r.data_through_at
            THEN 1 ELSE 0
        END AS is_eligible_30d
    FROM customer_accounts AS c
    CROSS JOIN report_cutoff AS r
    WHERE c.first_observed_order_at >= '2011-07-01'
      AND c.first_observed_order_at <  '2011-12-01'
),

customer_repeat AS (
    SELECT
        c.customer_id,
        c.cohort_month,
        c.is_eligible_30d,
        CASE
            WHEN c.is_eligible_30d = 1
             AND EXISTS (
                SELECT 1
                FROM orders AS o
                WHERE o.customer_id = c.customer_id
                  AND o.order_id <> c.first_observed_order_id
                  AND o.ordered_at >= c.first_observed_order_at
                  AND o.ordered_at <= datetime(
                      c.first_observed_order_at,
                      '+30 days'
                  )
             )
            THEN 1 ELSE 0
        END AS repeated_within_30_days
    FROM cohort_customers AS c
)

SELECT
    cohort_month,
    COUNT(*) AS cohort_customers,
    SUM(is_eligible_30d) AS eligible_customers,
    SUM(repeated_within_30_days) AS repeated_within_30_days,
    ROUND(
        SUM(repeated_within_30_days) * 100.0
        / NULLIF(SUM(is_eligible_30d), 0),
        2
    ) AS repeat_rate_30d_pct
FROM customer_repeat
GROUP BY cohort_month
ORDER BY cohort_month;
```

## Root cause

The principal measurement problem was **unequal observation time**:

- July customers could repeat at any point through early December.
- November customers had only days or weeks to repeat.
- Older cohort rates continued increasing as new transactions became available.
- The dashboard presented these cumulative values as if they were directly comparable monthly performance measures.

The original dashboard therefore confused **time available to repeat** with **customer retention quality**.

## Campaign decision

The proposed campaign requested:

- GBP 30,000 budget;
- 20% off the next order;
- customers acquired since September 2011 as the target group;
- GBP 85,000 expected revenue lift based only on Marketing judgment;
- no control group.

### Decision

**Do not approve the GBP 30,000 campaign as proposed.**

The original retention decline is not validated under a consistent observation window. In addition, the available data does not establish that a voucher would cause incremental purchases or produce positive contribution margin.

This decision does not prove that vouchers are ineffective. It means the current proposal lacks sufficient measurement and economic evidence.

### Recommended pilot

If management wants to explore the opportunity, use a limited randomized experiment:

| Group | Treatment |
|---|---|
| Control | No voucher |
| Treatment | Proposed post-purchase voucher |

Primary measure:

- incremental 30-day repeat purchase rate.

Financial and customer guardrails:

- contribution margin per eligible customer;
- average order value;
- voucher redemption rate;
- refund or cancellation rate;
- discount cost per incremental repeat customer.

## Recommended controls

1. Publish a written KPI contract defining population, numerator, denominator, event eligibility, observation window, and cutoff.
2. Report only fully matured cohorts in headline comparisons.
3. Label partial cohorts clearly and exclude them from trend conclusions.
4. Freeze or version historical dashboard outputs so later orders do not silently rewrite previous performance.
5. Display customer-ID coverage beside retention metrics.
6. Require experiment evidence and contribution-margin assumptions before approving campaign expenditure.

## Limitations

- `first_observed_order_at` is the first purchase in the available dataset, not proof of the customer's first-ever purchase.
- Orders without `customer_id` cannot be included in customer-level retention analysis.
- The dataset does not include acquisition channel, gross margin, voucher redemption, or randomized assignment.
- The analysis is descriptive and does not estimate the causal effect of a discount.
- Seasonal and customer-mix effects may still influence cohort performance.

## Repository structure

```text
case_002_retention_mirage/
├── README.md
├── START_HERE.md
├── PLAY_GUIDE_ID.md
├── LICENSE_DATA.md
├── data/
│   ├── alder_finch_case_002.db
│   ├── SOURCE.md
│   ├── TRANSFORMATION_NOTES.md
│   └── derived/
├── evidence/
├── sql/
│   ├── 01_data_discovery.sql
│   ├── 02_reproduce_dashboard.sql
│   ├── 03_retention_analysis.sql
│   └── 04_decision_checks.sql
├── documentation/
│   ├── data_dictionary.md
│   └── hypothesis_log.md
├── deliverables/
│   └── case_closure_memo.md
└── scripts/
    └── build_case_database.py
```

## How to run

1. Clone or download the repository.
2. Open the project folder in VS Code.
3. Connect SQLTools with the SQLite driver to `data/alder_finch_case_002.db`.
4. Run the numbered SQL files in order.
5. Compare the query outputs with the findings documented above.

The database is already included. `scripts/build_case_database.py` is only needed to rebuild the derived database from the original UCI workbook.

## Skills demonstrated

- SQL data discovery and validation;
- CTEs, `CASE`, `EXISTS`, date functions, and conditional aggregation;
- customer cohort and retention analysis;
- KPI definition and governance;
- table-grain and denominator validation;
- root-cause analysis;
- evaluation of campaign evidence;
- decision-making under incomplete information.

## Data source and license

- Daqing Chen, *Online Retail II*, UCI Machine Learning Repository, 2012
- Source: https://archive.ics.uci.edu/dataset/502/online%2Bretail%2Bii
- DOI: https://doi.org/10.24432/C5CG6D
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)

See `data/SOURCE.md` and `LICENSE_DATA.md` for attribution and transformation details.

## Author

**Tsani Fauzan Alhakim**

Portfolio: https://tsanialhkm.github.io
