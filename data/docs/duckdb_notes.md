# DuckDB Notes

Category: embedded OLAP database
Primary model: relational SQL over columnar analytical data
Best fit: local analytics, notebooks, data science workflows, CSV and Parquet exploration

## Use Case

DuckDB is an embedded analytical database that runs inside the application process. It is designed for OLAP workloads such as scans, aggregations, joins, data profiling, and local feature engineering. DuckDB is often used from Python, R, notebooks, command-line tools, and lightweight data applications.

## Architecture and Data Model

DuckDB uses SQL and stores data in a columnar format for efficient analytical execution. It supports vectorized execution, compression, parallel query processing, and direct querying of external files such as CSV, JSON, and Parquet. It can also attach to local database files and operate without a separate server.

## Strengths

DuckDB is simple to embed, fast for local analytical queries, and convenient for transforming files without loading them into a remote warehouse. It is a strong fit when data fits on one machine and the developer wants SQL without deploying PostgreSQL, Spark, or a cloud data warehouse.

DuckDB automatically creates zonemap indexes for storage blocks, which can skip irrelevant data during scans. It also supports ART indexes for primary keys, unique constraints, and explicit indexes.

## Tradeoffs

DuckDB is not a general OLTP server. It is not designed for many concurrent writers, long-running multi-user applications, or always-on transactional workloads. Compared with PostgreSQL, DuckDB is better for embedded analytics, while PostgreSQL is better for client-server OLTP applications.

## When to Choose

Choose DuckDB for local analytics, reproducible data pipelines, and fast SQL over files. Avoid it when the application needs high write concurrency, user authentication, network clients, or operational database administration.
