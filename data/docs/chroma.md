# Chroma Notes

Category: lightweight vector database
Primary model: collections of embeddings, documents, and metadata
Best fit: prototypes, local RAG apps, notebooks, small AI tools

## Use Case

Chroma is a lightweight embedding database often used for local RAG prototypes and AI application experiments. It is convenient when a developer wants to store text chunks, embeddings, and metadata without operating a larger vector database.

## Architecture and Data Model

Chroma organizes data into collections. Items can include ids, embeddings, documents, and metadata. It can run locally in-process or as a service depending on deployment style.

## Strengths

Chroma is simple to start with and integrates with many AI tooling ecosystems. It works well for demos, notebooks, local knowledge bases, and small document retrieval systems.

## Tradeoffs

Chroma is not usually the first choice for strict production durability, multi-tenant access control, or large distributed vector workloads. Teams should validate persistence, backup, concurrency, and deployment behavior before relying on it for critical systems.

## When to Choose

Choose Chroma for fast iteration and small local RAG projects. Choose Qdrant, Milvus, Weaviate, or pgvector when production operations, scaling, or relational integration matters more.
