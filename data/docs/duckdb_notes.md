# DuckDB Notes

DuckDB is an embedded OLAP database system. It runs in-process and is designed for analytical workloads.

DuckDB supports columnar storage, vectorized execution, and direct querying of external files such as CSV and Parquet.

Compared with PostgreSQL, DuckDB is more suitable for local analytical workloads, while PostgreSQL is a client-server database system commonly used for OLTP workloads.

DuckDB automatically creates zonemap indexes for columns in storage blocks. It also supports ART indexes for primary keys, unique constraints, and explicit indexes.
