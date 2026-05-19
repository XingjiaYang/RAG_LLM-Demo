# Database Selection Guide

Category: database architecture overview
Primary model: comparative guide across OLTP, OLAP, embedded, NoSQL, time-series, search, and vector systems
Best fit: choosing a database for a product, prototype, benchmark, or RAG application

## Selection Dimensions

Choose a database by workload first. OLTP systems optimize small reads and writes with transactions. OLAP systems optimize scans, joins, aggregations, compression, and analytical concurrency. Vector databases optimize nearest-neighbor search over embeddings. Search engines optimize keyword relevance, inverted indexes, and document retrieval. Time-series databases optimize append-heavy measurements with timestamps, retention, and downsampling.

## Common Categories

Embedded databases such as SQLite, DuckDB, RocksDB, and LMDB run in the same process as the application. They are simple to deploy and excellent for local or single-node workloads.

OLTP relational databases such as PostgreSQL and MySQL provide SQL, indexes, constraints, transactions, backup tools, and mature operational behavior. Distributed SQL systems such as CockroachDB, YugabyteDB, and TiDB extend the relational model across multiple nodes.

OLAP systems such as ClickHouse, Druid, Pinot, Snowflake, and BigQuery are better for event analytics, dashboards, reporting, and large scans. They are not replacements for a primary transactional database.

Vector systems such as Qdrant, Milvus, Weaviate, Chroma, pgvector, and FAISS support semantic search over embeddings. They differ in operational complexity, filtering, distributed scale, and integration with existing application data.

## Practical Advice

Prefer PostgreSQL for a default product database unless the workload clearly needs another system. Use SQLite for local-first applications, DuckDB for embedded analytics, ClickHouse for high-volume analytical events, Redis for caching, Elasticsearch for text search, and Qdrant or pgvector for RAG retrieval.

Avoid selecting a distributed database before there is a real need for multi-node scale, high availability across regions, or independent storage and compute scaling. Distributed systems add latency, operational complexity, and failure modes.

## RAG-Specific Advice

A RAG application usually needs two stores: a source-of-truth store for documents and metadata, and a retrieval index for embeddings. For small projects, pgvector or Qdrant is enough. For larger systems, keep raw documents in object storage or PostgreSQL, then use Qdrant, Milvus, Weaviate, or Elasticsearch hybrid search for retrieval.
