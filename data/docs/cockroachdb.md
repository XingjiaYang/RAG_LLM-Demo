# CockroachDB Notes

Category: distributed SQL database
Primary model: PostgreSQL-compatible relational SQL over replicated ranges
Best fit: globally resilient transactional applications, distributed OLTP

## Use Case

CockroachDB is a distributed SQL database designed for transactional workloads that need horizontal scale, high availability, and geographic resilience. It is used when a single-node relational database is not enough or when regional failure tolerance is a core requirement.

## Architecture and Data Model

CockroachDB distributes data into ranges and replicates them with consensus. SQL queries use a PostgreSQL-like interface, while the storage layer handles placement, replication, and rebalancing. Transactions provide strong consistency across distributed data.

## Strengths

CockroachDB allows teams to keep a relational SQL model while distributing data across nodes. It is useful for systems that need automatic failover, multi-region deployment, and transactional correctness.

## Tradeoffs

Distributed transactions add latency compared with a single-node PostgreSQL deployment. Schema design, transaction shape, regional placement, and contention patterns affect performance. PostgreSQL compatibility is useful but not identical to running PostgreSQL itself.

## When to Choose

Choose CockroachDB when distributed resilience is a requirement, not just a future idea. Avoid it when a simpler PostgreSQL deployment would meet scale and availability needs.
