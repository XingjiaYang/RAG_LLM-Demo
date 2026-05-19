# MongoDB Notes

Category: document database
Primary model: BSON documents in collections
Best fit: flexible JSON-like data, application documents, evolving schemas

## Use Case

MongoDB is a document database used for application data with flexible schemas. It works well when records are naturally represented as nested documents, such as user profiles, content objects, catalogs, event metadata, and product configurations.

## Architecture and Data Model

MongoDB stores BSON documents in collections. Documents can contain nested objects and arrays. Indexes support common filters, unique constraints, geospatial queries, text search, and compound access patterns. Replica sets provide high availability, and sharding distributes data across nodes.

## Strengths

MongoDB lets developers store data in a shape close to application objects. This can reduce joins and simplify iteration when schemas evolve. It supports aggregation pipelines, change streams, transactions, and flexible indexing.

## Tradeoffs

Flexible schemas can become inconsistent if the application does not enforce validation. Joins are less central than in relational databases, and highly normalized relational workloads may fit PostgreSQL or MySQL better. Shard key choice is important for distributed performance.

## When to Choose

Choose MongoDB when documents are the natural unit of access and schema flexibility is valuable. Avoid it when strong relational constraints, complex joins, and SQL-first analytics dominate the workload.
