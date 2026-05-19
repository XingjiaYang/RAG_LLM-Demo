# YugabyteDB Notes

Category: distributed SQL database
Primary model: PostgreSQL-compatible YSQL over distributed DocDB storage
Best fit: cloud-native transactional workloads, horizontal scale, high availability

## Use Case

YugabyteDB is a distributed database that provides PostgreSQL-compatible SQL through YSQL and a Cassandra-inspired API through YCQL. It is used when applications need relational transactions with distributed storage and high availability.

## Architecture and Data Model

YugabyteDB stores data in distributed tablets replicated through consensus. The YSQL layer exposes a PostgreSQL-compatible interface, while the DocDB storage layer handles sharding, replication, and persistence.

## Strengths

YugabyteDB combines familiar SQL with distributed deployment. It can support transactional applications that need horizontal scaling, resilience, and cloud-native operation. PostgreSQL compatibility helps reuse existing tools and application patterns.

## Tradeoffs

Like any distributed SQL system, YugabyteDB introduces more operational complexity than single-node PostgreSQL. Cross-node transactions, schema changes, data placement, and latency need attention. Compatibility is broad but should be tested for specific PostgreSQL extensions and features.

## When to Choose

Choose YugabyteDB when PostgreSQL-like development and distributed resilience are both required. Avoid it for small applications where PostgreSQL is simpler and sufficient.
