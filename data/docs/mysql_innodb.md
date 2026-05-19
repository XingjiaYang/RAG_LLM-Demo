# MySQL InnoDB Notes

Category: OLTP relational database
Primary model: row-oriented SQL tables with transactional storage
Best fit: web applications, transactional systems, MySQL-compatible ecosystems

## Use Case

MySQL with the InnoDB storage engine is widely used for OLTP workloads such as web applications, commerce systems, content platforms, and operational services. It is a practical choice when a team already depends on MySQL-compatible tooling, hosted services, or application frameworks.

## Architecture and Data Model

InnoDB provides ACID transactions, row-level locking, MVCC, crash recovery, and foreign keys. Tables are organized around a clustered primary key, which means the primary key order influences physical locality. Secondary indexes point back to the primary key, so primary key design can affect performance.

MySQL supports replication, read replicas, partitioning, and a large set of operational tools. It is commonly deployed as a primary writer with read replicas for read scaling.

## Strengths

MySQL is simple to operate for common web workloads, has broad hosting support, and performs well for indexed point lookups and short transactions. The ecosystem is mature, and many frameworks provide first-class MySQL support.

## Tradeoffs

MySQL is less extensible than PostgreSQL in some advanced use cases. Complex analytics, recursive queries, custom index behavior, and extension-heavy workflows may be more natural in PostgreSQL or analytical databases. Horizontal write scaling usually requires sharding, Vitess, TiDB, or another distributed architecture.

## When to Choose

Choose MySQL when compatibility, operational familiarity, and web application workloads dominate. Avoid it for heavy OLAP scans, flexible extension needs, or workloads that require sophisticated graph, vector, or time-series behavior inside the same engine.
