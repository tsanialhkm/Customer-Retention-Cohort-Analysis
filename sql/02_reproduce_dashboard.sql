-- CASE 002: Reproduce the stakeholder dashboard before evaluating it.

SELECT *
FROM report_runs;

SELECT *
FROM crm_dashboard_snapshot
ORDER BY cohort_month;
