# BigQuery Notes

Category: serverless cloud data warehouse
Primary model: SQL analytics over columnar managed storage
Best fit: large-scale analytics, log analysis, ELT, data lake queries

## Use Case

BigQuery is a managed serverless data warehouse. It is used for large analytical queries, reporting, log exploration, machine learning feature preparation, and data pipelines where teams do not want to manage warehouse clusters.

## Architecture and Data Model

BigQuery stores data in managed columnar storage and separates query execution from storage. Users submit SQL queries, and the service allocates execution resources. Tables can be partitioned, clustered, or queried through external table definitions depending on the workload.

## Strengths

BigQuery is strong for scanning large datasets with minimal operational work. It integrates well with cloud storage, streaming ingestion, scheduled queries, and data governance features. Its serverless model is convenient for teams that prefer usage-based analytics over cluster administration.

## Tradeoffs

BigQuery is not an OLTP system. It is not designed for high-rate small transactional writes or low-latency point lookups in request paths. Query cost and latency depend on bytes scanned, partition pruning, clustering, and SQL design.

## When to Choose

Choose BigQuery for managed large-scale analytics, especially in cloud-native pipelines. Avoid it for primary application state, user sessions, or workloads that need local embedded execution.
