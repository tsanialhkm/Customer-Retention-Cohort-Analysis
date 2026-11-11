# Case Closure Memo — The Retention Mirage

**To:** Managing Director, Alder & Finch Retail (fictional)
**Subject:** New-customer retention decline and the proposed GBP 30,000 voucher campaign
**Data:** UCI Online Retail II (40,077 qualifying orders, 5,878 identified customers)

## Business question

Did new-customer retention genuinely fall from 72.55% (July 2011) to 28.80% (November 2011), and should management approve Marketing's GBP 30,000 emergency voucher campaign?

## Executive finding

The dashboard figures are reproducible, but the cohorts are not comparable: each customer counted as "repeated" if any later order was visible by the report cutoff, so July customers had months to repeat while November customers had days or weeks. On a fixed 30-day repeat window, the mature July–October cohorts do not show a continuous decline. The campaign should not be approved as proposed.

## Dashboard reproduction

| Cohort | Dashboard rate | Reproduced rate | Difference |
|---|---:|---:|---:|
| July 2011 | 72.55% | 72.55% | 0.00 |
| August 2011 | 59.43% | 59.43% | 0.00 |
| September 2011 | 55.03% | 55.03% | 0.00 |
| October 2011 | 42.53% | 42.53% | 0.00 |
| November 2011 | 28.80% | 28.80% | 0.00 |

## Comparable retention analysis

**Metric:** 30-day repeat purchase rate — the share of identified new customers who place another qualifying order within 30 days of their first observed qualifying order. Only customers whose full 30-day window falls before the data cutoff are eligible.

| Cohort | Eligible customers | Repeat customers | Comparable rate |
|---|---:|---:|---:|
| July 2011 | 102 | 30 | 29.41% |
| August 2011 | 106 | 19 | 17.92% |
| September 2011 | 189 | 44 | 23.28% |
| October 2011 | 221 | 63 | 28.51% |
| November 2011 (partial) | 58 of 191 | 18 | 31.03% — not comparable |

Retention dips in August and recovers in September and October. November is shown for transparency only; it covers the 58 customers acquired early enough to complete a 30-day window.

## Customer identification coverage

Across the dataset, 92.24% of qualifying orders and 84.60% of qualifying order value are linked to an identified customer. Identified value coverage ranges from 76.97% (November 2011) to 90.01% (September 2011). The KPI therefore describes identified customers, not the whole purchasing population.

## Root cause

Unequal observation time. The dashboard presented cumulative repeat rates as comparable monthly performance, confusing time available to repeat with customer retention quality. Older cohort rates also kept rising as new orders arrived.

## Rejected hypotheses

| Hypothesis | Result |
|---|---|
| New-customer retention genuinely deteriorated after July | Not supported: mature cohorts on a fixed 30-day window show no continuous decline. |
| The dashboard calculation cannot be reproduced | Rejected: all five published rates were reproduced exactly. |

## Campaign decision

**Do not approve the GBP 30,000 campaign as proposed.** The decline is not validated under a consistent observation window, and the proposal has no control group, no margin assumptions, and an expected GBP 85,000 revenue lift based only on Marketing judgment. This does not prove vouchers are ineffective; it means the proposal lacks measurement and economic evidence.

If management wants to test the idea, run a limited randomized pilot (control: no voucher; treatment: proposed voucher). Primary measure: incremental 30-day repeat purchase rate. Guardrails: contribution margin per eligible customer, average order value, redemption rate, refund or cancellation rate, and discount cost per incremental repeat customer.

## KPI recommendation

| Element | Definition |
|---|---|
| Population | Identified customers grouped by month of first observed qualifying order |
| Numerator | Customers with another qualifying order within 30 days of their first |
| Denominator | Customers whose full 30-day window is inside the data cutoff |
| Comparison rule | Only fully matured cohorts appear in headline trends; partial cohorts are labelled |

## Preventive control

1. Publish a written KPI contract: population, numerator, denominator, event eligibility, observation window and cutoff.
2. Report only fully matured cohorts in headline comparisons and label partial cohorts.
3. Freeze or version historical dashboard outputs so later orders do not silently rewrite past performance.
4. Show customer-ID coverage beside retention metrics.
5. Require experiment evidence and contribution-margin assumptions before approving campaign spend.

## Assumptions and limitations

- `first_observed_order_at` is the first purchase in the dataset, not proof of a customer's first-ever purchase.
- Orders without `customer_id` are excluded from customer-level retention.
- No acquisition channel, gross margin, voucher redemption or randomized assignment data.
- The analysis is descriptive and does not estimate the causal effect of a discount.
- Seasonal and customer-mix effects were not tested and may still influence cohort performance.
