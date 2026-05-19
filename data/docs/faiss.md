# FAISS Notes

Category: vector similarity search library
Primary model: in-process indexes for dense vectors
Best fit: custom vector search pipelines, research, offline indexing

## Use Case

FAISS is a library for efficient similarity search over dense vectors. It is often used in research, recommendation systems, semantic search experiments, and custom retrieval services where the application owns persistence and serving logic.

## Architecture and Data Model

FAISS provides index structures rather than a complete database. Applications load vectors into an index, run nearest-neighbor queries, and manage ids, metadata, storage, updates, and access control separately. Index types trade off memory, speed, recall, and build cost.

## Strengths

FAISS is fast, flexible, and widely used for vector search. It supports exact and approximate search, quantization, GPU acceleration in some setups, and many index configurations for different scale and recall targets.

## Tradeoffs

FAISS is not a database server. It does not provide document storage, metadata filtering, replication, authentication, HTTP APIs, or automatic persistence by default. Application code must build those pieces.

## When to Choose

Choose FAISS when building a custom vector retrieval component or benchmark. Choose a vector database when operational features such as filtering, persistence, monitoring, and multi-client access are required.
