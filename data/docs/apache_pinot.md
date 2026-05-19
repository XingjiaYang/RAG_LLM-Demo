# Apache Pinot Notes

Category: real-time OLAP database
Primary model: columnar analytics for low-latency user-facing queries
Best fit: user-facing analytics, metrics exploration, event dashboards

## Use Case

Apache Pinot is an OLAP database built for low-latency analytics on real-time and batch data. It is often used when customers or internal users need interactive dashboards backed by large event datasets.

## Architecture and Data Model

Pinot uses tables, segments, controllers, brokers, servers, and minions. Offline tables load batch data, while real-time tables consume streams such as Kafka. Indexes can include inverted indexes, range indexes, text indexes, JSON indexes, and star-tree indexes for pre-aggregated query acceleration.

Pinot schemas define dimensions, metrics, and time columns. Query performance depends heavily on segment layout, indexing, partitioning, and common filter patterns.

## Strengths

Pinot is strong at high-concurrency, low-latency analytical queries. It supports ingestion from streams, hybrid tables combining real-time and offline segments, and indexing choices tailored to dashboard workloads.

## Tradeoffs

Pinot is not an OLTP database. It favors denormalized event tables and predictable analytical queries. Complex joins, frequent transactional updates, and arbitrary relational workloads are not its primary focus.

## When to Choose

Choose Pinot when the product needs fast user-facing analytics over events. Avoid it when the workload is a traditional application database or when data modeling cannot be aligned with query patterns.
