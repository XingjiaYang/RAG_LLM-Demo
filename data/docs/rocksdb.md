# RocksDB Notes

Category: embedded key-value database
Primary model: ordered key-value store based on LSM trees
Best fit: write-heavy embedded storage engines, stream processing state, custom databases

## Use Case

RocksDB is an embedded persistent key-value store designed for high write throughput and efficient storage on SSDs. It is commonly used inside larger systems as a storage engine rather than as an end-user database. Examples include stream processors, metadata stores, search systems, and distributed databases.

## Architecture and Data Model

RocksDB stores sorted key-value pairs using a log-structured merge tree. Writes first go to memory structures and logs, then are flushed and compacted into sorted files. This design makes writes efficient and supports range scans over ordered keys.

Column families allow separate logical key spaces with different tuning. Applications control serialization, schema, secondary indexes, transactions, and query behavior.

## Strengths

RocksDB is highly tunable. It supports compression, bloom filters, prefix extractors, compaction strategies, snapshots, and iterators. It is a good fit when an application needs an embedded storage engine with predictable low-level control.

## Tradeoffs

RocksDB is not a SQL database and not a standalone server. Developers must build higher-level features such as schemas, query planning, replication, and access control. Compaction can cause write amplification and requires careful tuning for latency-sensitive workloads.

## When to Choose

Choose RocksDB when building infrastructure that needs an embedded, persistent, ordered key-value engine. Avoid it for normal application CRUD unless the team is prepared to own database behavior above the storage layer.
