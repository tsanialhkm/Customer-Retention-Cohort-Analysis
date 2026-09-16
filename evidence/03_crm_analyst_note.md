# CRM Dashboard Calculation Note

**Owner:** CRM Analytics  
**Report generated:** 9 December 2011 at 15:00

The dashboard groups customers by the month of their first observed qualifying order.

A customer is marked as repeated when the system can see at least one other qualifying order after the first observed order. The numerator is the number of repeated customers visible when the report runs. The denominator is all identified customers whose first observed order belongs to that acquisition month.

Orders without a customer identifier cannot be connected across purchases and are excluded from customer-cohort calculations.

The report uses all data available at generation time. It does not freeze earlier cohort results.
