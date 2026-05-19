# SQLite Notes

Category: embedded OLTP-style relational database
Primary model: single-file SQL database
Best fit: local apps, mobile apps, edge devices, tests, prototypes

## Use Case

SQLite is an embedded relational database stored in a normal file. It is excellent for local-first applications, mobile apps, command-line tools, desktop software, test fixtures, and small services that do not need a separate database server.

## Architecture and Data Model

SQLite runs inside the application process and reads or writes a database file directly. It supports SQL, transactions, indexes, constraints, views, triggers, and WAL mode. Because it is serverless, there is no network process, user account system, or daemon to manage.

## Strengths

SQLite is reliable, portable, and easy to distribute. A complete database can be copied as a single file. It is ideal for development and testing because setup is minimal. Many applications use SQLite as an embedded metadata store or local cache.

## Tradeoffs

SQLite handles many readers well, especially with WAL mode, but write concurrency is limited compared with client-server databases. It is not intended for many application servers writing to the same database file over a network filesystem. Access control is usually handled by the application or operating system.

## When to Choose

Choose SQLite when deployment simplicity matters and the workload is local, embedded, or single-node. Avoid it when many concurrent writers, network clients, centralized user management, or horizontal scaling are required.

## Comparison

Compared with PostgreSQL, SQLite is easier to embed but less suitable as a shared production service. Compared with DuckDB, SQLite is more OLTP-oriented, while DuckDB is more OLAP-oriented.
