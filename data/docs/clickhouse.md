# ClickHouse Notes

Category: OLAP columnar database
Primary model: column-oriented SQL analytics
Best fit: event analytics, dashboards, logs, metrics, high-volume aggregations

## Use Case

ClickHouse is an analytical database optimized for fast scans, aggregations, and compression over large datasets. It is commonly used for product analytics, observability, security logs, ad tech, time-series events, and user-facing analytical dashboards.

## Architecture and Data Model

ClickHouse stores data by column and processes queries with vectorized execution. Its MergeTree family of table engines supports partitioning, sorting keys, sparse primary indexes, background merges, replication, and TTL policies.

The physical sort order matters. Good schemas choose partition and order keys based on common filters such as time, tenant, customer, or event type.

## Strengths

ClickHouse is very fast for append-heavy analytical workloads and can achieve high compression. It supports SQL, materialized views, projections, approximate aggregations, and distributed query execution. It can serve low-latency dashboards when data is modeled for the query patterns.

## Tradeoffs

ClickHouse is not an OLTP database. It is not designed for frequent small row updates, foreign-key-heavy schemas, or high-concurrency transactional writes. Joins are supported, but denormalization and pre-aggregation are often better for performance.

## When to Choose

Choose ClickHouse when analytical event volume is high and queries scan or aggregate many rows. Avoid it as the source of truth for transactional application state.
