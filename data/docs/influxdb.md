# InfluxDB Notes

Category: time-series database
Primary model: measurements, tags, fields, and timestamps
Best fit: metrics, monitoring, IoT sensor data, time-window aggregations

## Use Case

InfluxDB is designed for time-series data such as infrastructure metrics, application telemetry, IoT readings, and sensor streams. It is useful when data arrives continuously and queries often group by time windows.

## Architecture and Data Model

InfluxDB organizes data around measurements, tags, fields, and timestamps. Tags are indexed metadata used for filtering and grouping, while fields store measured values. Retention policies and downsampling help manage long-term storage.

## Strengths

InfluxDB provides a purpose-built model for time-series ingestion and analysis. It supports high write rates, time-window queries, retention management, and integration with monitoring and visualization tools.

## Tradeoffs

Schema design matters, especially tag cardinality. Very high-cardinality tags can increase index and memory pressure. InfluxDB is not a general relational database and is not intended for complex joins or transactional application state.

## When to Choose

Choose InfluxDB for monitoring and sensor-style time-series workloads. Avoid it when the data is primarily relational, document-oriented, or requires complex transactional logic.
