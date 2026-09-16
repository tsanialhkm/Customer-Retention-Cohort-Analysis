# Case 002: The Retention Mirage

A spoiler-free SQL and business-analysis investigation built from real retail transactions.

## Portfolio context

You are a Business Analyst supporting **Alder & Finch Retail**, a fictional UK gift retailer. Marketing reports that the repeat purchase rate for newly acquired customers has fallen sharply. The team wants approval for an emergency discount campaign before the holiday season.

Your job is to determine whether the reported decline is real, whether the metric supports a fair comparison, and what management should do next.

## Difficulty

**Level:** 4 of 15  
**Estimated investigation time:** 4–8 hours  
**Primary tool:** SQL with SQLite

Concepts likely to be useful:

- table grain and data coverage;
- joins and conditional aggregation;
- customer cohorts;
- date differences and observation windows;
- numerator and denominator validation;
- metric governance;
- decision-making with incomplete evidence.

## Start

1. Read `START_HERE.md`.
2. Review every file in `evidence/`.
3. Connect SQLTools to `data/alder_finch_case_002.db`.
4. Record your hypotheses in `documentation/hypothesis_log.md`.
5. Save your investigation in the numbered files under `sql/`.
6. Complete `deliverables/case_closure_memo.md`.

No solution is included in this repository.

## Dataset

The company, stakeholders, dashboard, and proposed campaign are fictional. The underlying orders are derived from the real **Online Retail II** dataset published by the UCI Machine Learning Repository.

| Item | Value |
|---|---:|
| Original transaction rows | 1,067,371 |
| Derived qualifying orders | 40,077 |
| Identified customers | 5,878 |
| Source period | 1 December 2009–9 December 2011 |

The original source contains all transactions from a UK-based non-store retailer over approximately two years. The case database aggregates qualifying sales lines to one row per order while preserving the transaction dates and values needed for the investigation.

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
│       ├── orders.csv
│       └── customer_accounts.csv
├── evidence/
│   ├── 01_executive_request.md
│   ├── 02_marketing_director_email.md
│   ├── 03_crm_analyst_note.md
│   ├── 04_kpi_dictionary.md
│   ├── 05_source_system_note.md
│   ├── 06_crm_dashboard_export.csv
│   ├── 07_campaign_proposal.csv
│   └── 08_finance_email.md
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

## Source and license

- Daqing Chen, *Online Retail II*, UCI Machine Learning Repository, 2012
- Source: https://archive.ics.uci.edu/dataset/502/online%2Bretail%2Bii
- DOI: https://doi.org/10.24432/C5CG6D
- License: CC BY 4.0

See `data/SOURCE.md` and `LICENSE_DATA.md` for attribution and transformation details.
