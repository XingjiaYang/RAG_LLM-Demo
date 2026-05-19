# Snowflake Notes

Category: cloud data warehouse
Primary model: SQL analytics with separated storage and compute
Best fit: enterprise analytics, ELT, reporting, governed warehouse workloads

## Use Case

Snowflake is a managed cloud data warehouse used for analytics, reporting, data sharing, and ELT pipelines. It is suitable when teams want a managed SQL warehouse without operating storage, compute clusters, or distributed query infrastructure directly.

## Architecture and Data Model

Snowflake separates storage from compute. Data is stored in compressed columnar micro-partitions, while virtual warehouses provide compute resources for queries and loading. Multiple warehouses can access the same data with isolated compute.

Snowflake supports SQL, semi-structured data, roles, governance features, data sharing, streams, tasks, and integrations with many data tools.

## Strengths

Snowflake is strong for managed analytics, workload isolation, elastic compute, and enterprise data governance. It reduces operational burden and allows teams to scale compute for separate workloads such as ingestion, dashboards, and ad hoc analysis.

## Tradeoffs

Snowflake is not a low-latency OLTP database. Cost management requires attention to warehouse sizing, query patterns, auto-suspend settings, and data transfer. Very small operational queries may be better served by PostgreSQL, MySQL, or a service database.

## When to Choose

Choose Snowflake for managed warehouse analytics and cross-team data sharing. Avoid it as the primary transactional store for product writes or millisecond request paths.
