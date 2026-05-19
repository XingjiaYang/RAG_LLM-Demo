# TimescaleDB Notes

Category: time-series database extension for PostgreSQL
Primary model: SQL hypertables over time-partitioned data
Best fit: metrics, telemetry, IoT, financial ticks, operational time-series

## Use Case

TimescaleDB extends PostgreSQL for time-series workloads. It is a strong fit when teams want PostgreSQL SQL and ecosystem compatibility while ingesting and querying large volumes of timestamped data.

## Architecture and Data Model

TimescaleDB uses hypertables, which automatically partition time-series data into chunks. Applications query hypertables with normal SQL, while TimescaleDB manages chunking, compression, retention, and continuous aggregates.

## Strengths

TimescaleDB keeps the relational model and PostgreSQL tooling while adding time-series optimizations. It supports joins with relational metadata, SQL analytics, indexes, compression, retention policies, and precomputed continuous aggregates.

## Tradeoffs

TimescaleDB inherits PostgreSQL operational behavior and is not the same as a distributed event warehouse. Very high-cardinality metrics at massive scale may require careful schema design or a specialized metrics system.

## When to Choose

Choose TimescaleDB when time-series data should live near relational metadata and SQL is important. Avoid it when the system mainly needs a managed metrics backend or large-scale columnar event analytics.
