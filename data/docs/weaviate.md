# Weaviate Notes

Category: vector database
Primary model: objects with vectors, schema, and metadata
Best fit: semantic search, hybrid search, AI application backends

## Use Case

Weaviate is a vector database for storing objects and embeddings together. It is often used for semantic search, RAG, recommendation, and AI applications that need vector search plus metadata fields.

## Architecture and Data Model

Weaviate organizes data into classes or collections with schema-defined properties. Objects can include vectors and metadata. Queries can combine semantic similarity with filters and keyword-based search, depending on configuration.

## Strengths

Weaviate is developer-friendly for AI search applications. It supports hybrid search, metadata filtering, schema management, and integrations with embedding and generative model providers. It can be useful when semantic search is part of a larger object retrieval API.

## Tradeoffs

As with other vector databases, Weaviate should not replace the durable source of truth for important business data. Schema and vectorization choices need to be managed carefully. Operational complexity is higher than an in-memory library.

## When to Choose

Choose Weaviate when object-oriented semantic search and hybrid retrieval are important. Avoid it when the application only needs a small local vector index or when PostgreSQL already satisfies the retrieval requirements with pgvector.
