# pgvector Notes

Category: PostgreSQL vector extension
Primary model: vector columns inside PostgreSQL tables
Best fit: small to medium RAG systems, semantic search near relational data

## Use Case

pgvector adds vector similarity search to PostgreSQL. It is a strong fit when embeddings should live next to relational data such as documents, users, permissions, tenants, and audit metadata.

## Architecture and Data Model

pgvector provides a vector data type and distance operators for similarity search. Tables can store text, metadata, and embedding vectors in the same row. Index options such as HNSW and IVFFlat can speed up approximate nearest-neighbor search.

## Strengths

pgvector keeps application architecture simple. Teams can use PostgreSQL transactions, backups, access control, joins, filters, and existing tooling while adding semantic retrieval. It is especially attractive for early-stage RAG systems and internal tools.

## Tradeoffs

PostgreSQL with pgvector may not match purpose-built vector databases for very large vector collections, distributed indexing, or specialized vector operations. Index tuning, vacuum behavior, and query planning still matter.

## When to Choose

Choose pgvector when relational metadata and semantic search should be managed together. Move to Qdrant, Milvus, or Weaviate when vector scale or operational isolation becomes a clearer requirement.
