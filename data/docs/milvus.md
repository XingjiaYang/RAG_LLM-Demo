# Milvus Notes

Category: vector database
Primary model: distributed vector collections and ANN indexes
Best fit: large-scale embedding search, semantic retrieval, multimodal search

## Use Case

Milvus is a vector database designed for large embedding collections and approximate nearest-neighbor search. It is used for semantic search, image search, recommendation, anomaly detection, and RAG systems with growing vector volume.

## Architecture and Data Model

Milvus stores vectors in collections with scalar fields for metadata. It supports several index types for approximate search and can separate components for coordination, query execution, indexing, and storage in distributed deployments.

## Strengths

Milvus is suitable when vector scale and distributed architecture matter. It supports high-dimensional vectors, metadata filtering, partitions, multiple index strategies, and integration with embedding frameworks.

## Tradeoffs

Milvus can be more operationally complex than lightweight options such as Chroma, FAISS, or single-node Qdrant. Teams should understand index build time, memory usage, search parameters, compaction, and deployment topology.

## When to Choose

Choose Milvus when vector volume, throughput, or distributed deployment requirements exceed simple local stores. Avoid it for very small prototypes where a single-process library or PostgreSQL extension is enough.
