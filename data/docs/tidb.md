# TiDB Notes

Category: distributed SQL and HTAP database
Primary model: MySQL-compatible SQL over distributed row storage and optional columnar replicas
Best fit: MySQL-compatible scale-out OLTP, hybrid transactional and analytical processing

## Use Case

TiDB is a distributed SQL database with MySQL compatibility. It is used when teams want to scale MySQL-style workloads horizontally or combine transactional storage with analytical acceleration through a distributed architecture.

## Architecture and Data Model

TiDB separates SQL processing from storage. TiDB nodes handle SQL, TiKV stores transactional row data, and Placement Driver coordinates metadata and scheduling. TiFlash can provide columnar replicas for analytical queries in HTAP workloads.

## Strengths

TiDB provides horizontal scale with a familiar MySQL-compatible interface. It can reduce pressure on a traditional MySQL deployment when data volume or concurrency grows. The HTAP model can serve both operational and analytical queries when designed carefully.

## Tradeoffs

Distributed SQL requires operational expertise. Query plans, transaction size, hotspot keys, region scheduling, and network latency affect performance. MySQL compatibility is useful, but applications should test SQL behavior and edge cases before migration.

## When to Choose

Choose TiDB when MySQL compatibility and distributed scaling are important. Avoid it when a single MySQL or PostgreSQL server is simpler and already meets the workload.
