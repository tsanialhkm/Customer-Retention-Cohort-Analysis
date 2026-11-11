# Hypothesis Log

| ID | Hypothesis | Evidence for | Evidence against | Status |
|---|---|---|---|---|
| H1 | New-customer retention genuinely deteriorated after July. | The cumulative dashboard rate falls from 72.55% to 28.80%. | On a fixed 30-day window, mature July–October cohorts dip in August and recover in September–October. | Not supported |
| H2 | Recent cohorts appear weaker because they have had less time to place another order. | The dashboard counts any later order visible by the cutoff; July customers had months, November customers days or weeks. | — | Supported |
| H3 | Missing customer identifiers materially limit what the retention metric represents. | 92.24% of qualifying orders and 84.60% of order value are linked to a customer; November value coverage is 76.97%. | — | Supported as a limitation |
| H4 | Customer or country mix explains part of the pattern. | — | — | Not tested |
| H5 | The dashboard calculation cannot be reproduced from the database. | — | All five published cohort rates were reproduced exactly. | Rejected |

## Questions resolved

| ID | Question | Answer | Status |
|---|---|---|---|
| Q1 | What exact logic reproduces the displayed rate? | Customers with any other qualifying order visible by the report cutoff, divided by all identified customers in the cohort. | Resolved |
| Q2 | How much observation time does each cohort receive? | Variable: from months (July) to days or weeks (November). | Resolved |
| Q3 | What fixed-window metric creates a fair comparison? | 30-day repeat purchase rate, eligible customers only. | Resolved |
| Q4 | Which orders are excluded because customer identity is unavailable? | 7.76% of qualifying orders (15.40% of value) across the dataset. | Resolved |
| Q5 | Does the evidence justify the proposed campaign? | No. No validated decline, no control group, no margin assumptions. | Resolved |
