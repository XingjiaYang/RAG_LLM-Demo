# Elasticsearch Notes

Category: search and analytics engine
Primary model: JSON documents indexed with inverted indexes
Best fit: full-text search, log search, relevance ranking, document retrieval

## Use Case

Elasticsearch is used for full-text search, log analytics, application search, observability, and document retrieval. It is strong when users need keyword search, filters, facets, relevance scoring, and near-real-time indexing.

## Architecture and Data Model

Elasticsearch stores JSON documents in indexes that are split into shards and replicas. It builds inverted indexes for text fields and column-oriented doc values for filtering, sorting, and aggregations. Queries can combine full-text relevance, structured filters, aggregations, and highlighting.

## Strengths

Elasticsearch is powerful for text search and operational exploration. It supports analyzers, tokenization, synonyms, fuzzy matching, aggregations, and distributed search. It can complement a relational source of truth by indexing denormalized searchable documents.

## Tradeoffs

Elasticsearch is not an OLTP database. It provides near-real-time indexing, not strict transactional behavior across arbitrary updates. Mapping design, shard sizing, refresh intervals, and heap management affect reliability and performance.

## When to Choose

Choose Elasticsearch when keyword search and relevance ranking are core requirements. Avoid using it as the only database for transactional records that require relational constraints and strong consistency.
