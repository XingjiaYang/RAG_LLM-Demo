# Redis Notes

Category: in-memory data structure store
Primary model: keys mapped to strings, hashes, lists, sets, streams, and other structures
Best fit: caching, rate limits, queues, sessions, ephemeral coordination

## Use Case

Redis is commonly used as a cache, session store, message broker, rate limiter, leaderboard engine, and lightweight real-time data structure server. It is popular because operations are fast and data structures are directly useful to application code.

## Architecture and Data Model

Redis stores data in memory and exposes commands over a network protocol. It supports strings, hashes, lists, sets, sorted sets, bitmaps, HyperLogLogs, streams, and pub/sub. Persistence options include snapshots and append-only files, depending on durability needs.

## Strengths

Redis is extremely useful for reducing load on primary databases and implementing low-latency application primitives. Expiration, atomic commands, Lua scripts, streams, and sorted sets make it practical for many infrastructure tasks.

## Tradeoffs

Redis is not a replacement for a durable relational database in most product systems. Memory cost, eviction policy, persistence configuration, and failover behavior must be understood. Data modeling is command-oriented rather than SQL-oriented.

## When to Choose

Choose Redis for cache and coordination workloads where low latency matters. Avoid using it as the only source of truth unless the durability and recovery model has been designed explicitly.
