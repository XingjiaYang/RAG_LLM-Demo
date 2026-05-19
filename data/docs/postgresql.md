# PostgreSQL Notes

Category: OLTP relational database
Primary model: row-oriented SQL tables with ACID transactions
Best fit: product backends, transactional applications, relational data, extensions

## Use Case

PostgreSQL is a general-purpose relational database and a strong default choice for application development. It works well for user accounts, orders, payments, permissions, metadata, operational records, and systems that need correctness more than raw distributed scale.

## Architecture and Data Model

PostgreSQL is a client-server database with SQL, transactions, foreign keys, constraints, views, stored procedures, and mature backup tooling. It uses MVCC so readers and writers can operate concurrently without most read locks. Write-ahead logging supports crash recovery and replication.

PostgreSQL supports many index types: B-tree for equality and range filters, GIN for arrays and full-text search, GiST for geometric and extensible indexing, and BRIN for large naturally ordered tables.

## Strengths

PostgreSQL is extensible. Extensions such as PostGIS, pgvector, TimescaleDB, and full-text search features allow one database to cover many product needs. It has a mature optimizer, strong transactional semantics, and a large ecosystem of tools.

## Tradeoffs

PostgreSQL scales vertically very well, but horizontal write scaling usually requires application-level sharding, read replicas, partitioning, or a distributed SQL alternative. It is also not a columnar warehouse by default, so very large analytical scans may be better served by DuckDB, ClickHouse, BigQuery, or Snowflake.

## When to Choose

Choose PostgreSQL when data is relational, correctness matters, SQL is useful, and the team wants a reliable default. Avoid using it as the only analytical engine when event volumes are extremely high or dashboard queries scan billions of rows frequently.
