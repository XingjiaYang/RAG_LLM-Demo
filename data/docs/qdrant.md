# Qdrant Notes

Category: vector database
Primary model: vector points with payload metadata and filtering
Best fit: RAG retrieval, semantic search, recommendation, similarity search

## Use Case

Qdrant stores embeddings and performs similarity search. It is a practical choice for RAG applications because each point can combine a vector with payload metadata such as source path, chunk id, title, tenant, timestamp, or document type.

## Architecture and Data Model

Qdrant organizes data into collections. A collection contains points, and each point has an id, vector, and payload. Queries can search by vector similarity and apply payload filters. HNSW indexing supports approximate nearest-neighbor retrieval.

## Strengths

Qdrant has a clear API, strong filtering support, and simple local deployment. It works well for document chunks, product embeddings, user preference vectors, and hybrid metadata filtering. It can run as a single node for prototypes and scale to larger deployments when needed.

## Tradeoffs

Qdrant is not a full relational source of truth. Applications usually keep original documents and business records elsewhere, then store embeddings and retrieval metadata in Qdrant. Embedding quality, chunking, and metadata design often matter more than raw vector database choice.

## When to Choose

Choose Qdrant for semantic retrieval where vector search and filters are both important. Avoid using it as the only store for transactional application data.
