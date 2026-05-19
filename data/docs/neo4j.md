# Neo4j Notes

Category: graph database
Primary model: property graph with nodes, relationships, labels, and properties
Best fit: relationship-heavy queries, graph traversal, recommendations, knowledge graphs

## Use Case

Neo4j is used when relationships are central to the data model. Examples include fraud detection, identity graphs, recommendation systems, network analysis, knowledge graphs, dependency graphs, and access-control relationships.

## Architecture and Data Model

Neo4j stores nodes and relationships as first-class entities. Both can have properties. Labels classify nodes, and relationship types classify edges. The Cypher query language expresses graph patterns and traversals directly.

## Strengths

Neo4j makes multi-hop relationship queries easier to write and often faster than equivalent join-heavy relational models. It is useful when the query asks how entities are connected, what path exists between them, or what subgraph matches a pattern.

## Tradeoffs

Neo4j is specialized. It is not the best choice for simple key-value access, large analytical scans, or workloads that are mostly tabular. Graph models can also become hard to maintain if the application does not clearly define relationship semantics.

## When to Choose

Choose Neo4j when graph traversal is a primary workload, not an occasional feature. Avoid it when a relational database with a few join tables would be simpler.
