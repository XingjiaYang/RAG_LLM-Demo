# Apache Cassandra Notes

Category: distributed wide-column database
Primary model: partitioned rows with tunable consistency
Best fit: high-write availability, multi-node scale, predictable access patterns

## Use Case

Apache Cassandra is designed for highly available distributed workloads with high write throughput. It is often used for time-series events, messaging metadata, IoT data, activity feeds, and applications that need to keep accepting writes across node failures.

## Architecture and Data Model

Cassandra uses a peer-to-peer architecture. Data is distributed by partition key and replicated across nodes. It uses an LSM-tree storage design and supports tunable consistency levels for reads and writes.

Data modeling starts from queries. Tables are designed around partition keys, clustering columns, and access patterns rather than normalized relational structure.

## Strengths

Cassandra scales horizontally for write-heavy workloads and avoids a single primary node. It can provide high availability across racks or regions when configured correctly. Sequential writes and immutable storage files fit append-heavy patterns well.

## Tradeoffs

Cassandra is not built for ad hoc joins, relational constraints, or arbitrary secondary-index-heavy queries. Poor partition key design can create hot partitions or large partitions. Operational tuning includes compaction, repair, consistency, and tombstone management.

## When to Choose

Choose Cassandra when the workload has massive write volume, predictable query patterns, and high availability requirements. Avoid it for general relational applications or flexible ad hoc analytics.
