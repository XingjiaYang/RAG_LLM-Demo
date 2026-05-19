# Apache Druid Notes

Category: real-time OLAP database
Primary model: columnar event analytics with time-based segments
Best fit: streaming analytics, dashboards, time-filtered aggregations

## Use Case

Apache Druid is designed for low-latency analytical queries over event data. It is often used for operational dashboards, clickstream analytics, telemetry, ad analytics, network events, and other workloads where recent data must be queryable quickly.

## Architecture and Data Model

Druid organizes data into immutable time-based segments. Ingestion jobs transform, index, partition, and optionally roll up events. Query nodes can filter by time, dimensions, and metrics, then aggregate results across segments.

Druid separates ingestion, coordination, historical storage, brokers, and query execution. This architecture supports real-time ingestion and scalable analytical reads.

## Strengths

Druid is strong for time-filtered group-by queries, top-N queries, approximate distinct counts, sketches, and dashboards over streaming data. It supports rollup, bitmap indexes, and pre-aggregation, which can reduce query cost.

## Tradeoffs

Druid requires careful ingestion design. Schema changes, late data, compaction, and segment management add operational complexity. It is not intended for arbitrary transactional updates, relational joins, or normalized OLTP schemas.

## When to Choose

Choose Druid for real-time analytical dashboards over event streams. Avoid it when the workload is mostly transactional, document-oriented, or based on complex ad hoc relational joins.
