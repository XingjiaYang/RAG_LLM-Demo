# ScyllaDB Notes

Category: distributed wide-column database
Primary model: Cassandra-compatible partitioned rows
Best fit: low-latency high-throughput Cassandra-style workloads

## Use Case

ScyllaDB is a distributed wide-column database compatible with Cassandra-style data modeling. It targets high throughput and low latency for workloads such as telemetry, real-time services, messaging, and large-scale operational event storage.

## Architecture and Data Model

ScyllaDB follows the Cassandra data model: partition keys distribute data, clustering columns order rows within partitions, and queries should align with primary-key design. It is implemented with a shard-per-core architecture to reduce coordination overhead and improve CPU utilization.

## Strengths

ScyllaDB can provide strong performance for write-heavy and latency-sensitive workloads when data modeling is correct. It supports horizontal scaling, replication, and Cassandra-compatible APIs, which can ease migration from Cassandra.

## Tradeoffs

The core tradeoffs are similar to Cassandra. It is not a relational database, and it does not reward arbitrary queries, joins, or heavily normalized schemas. Partition design, repair, compaction, and operational monitoring still matter.

## When to Choose

Choose ScyllaDB when the team wants Cassandra-like scalability with a focus on predictable low latency. Avoid it when a normal PostgreSQL or MySQL schema would be simpler and sufficient.
