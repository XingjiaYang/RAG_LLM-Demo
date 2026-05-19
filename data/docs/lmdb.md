# LMDB Notes

Category: embedded key-value database
Primary model: memory-mapped B+ tree key-value store
Best fit: read-heavy embedded storage, metadata, small local indexes

## Use Case

LMDB is an embedded key-value database that uses memory-mapped files. It is well suited for read-heavy workloads, local indexes, metadata stores, and applications that need simple transactional persistence without a database server.

## Architecture and Data Model

LMDB stores key-value pairs in a B+ tree. It uses copy-on-write pages and MVCC, allowing readers to proceed without blocking writers. There can be many concurrent readers, but writes are serialized through a single writer transaction.

Because it is memory-mapped, the operating system page cache does much of the caching work. The application accesses data through transactions and cursors rather than SQL.

## Strengths

LMDB has very low read overhead, simple deployment, and strong crash consistency. It is efficient for workloads with many reads, small keys, and predictable embedded access patterns. The database is stored in a small set of files and does not require a daemon.

## Tradeoffs

The single-writer model limits write concurrency. The memory-mapped design also means applications must understand file size limits and environment configuration. LMDB does not provide SQL, secondary indexes, replication, or network access by itself.

## When to Choose

Choose LMDB for embedded read-heavy storage where simplicity and transaction safety are important. Avoid it for high write concurrency, distributed access, or workloads that need rich query features.
