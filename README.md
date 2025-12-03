# gRPC Client-Streaming Demo in Python

This repository contains a minimal but practical demonstration of gRPC client-streaming implemented in Python. It models a simplified version of a high-throughput ingestion pipeline, where a client continuously streams WorkItem messages to a server that processes them using throttled background workers.

The project reflects the real-world patterns I worked with at Oddsview, where we migrated internal ingestion infrastructure from Kafka to gRPC. The architecture there supported flexible communication modes—one-to-one, one-to-many, many-to-one, and many-to-many—between producers and consumers, while ensuring that load was distributed fairly across all active consumers. This demo provides a simplified, open-source-friendly version of those ideas.

The entire system is built using Python’s asyncio ecosystem, making all components—from streaming ingestion to queue handling and worker processing—fully asynchronous. This allows the server to handle high-throughput client streams efficiently even when worker speeds vary or multiple consumers are active.

It demonstrates production-grade concepts such as asynchronous ingestion, queueing, worker pools, priority handling, message drops under load, balanced consumer processing, and structured streaming using gRPC.

---

## Overview

The architecture consists of:

1. **Client**
   Continuously generates and streams `WorkItem` messages to the server using a single long-lived client-streaming RPC.

2. **Server**
   Accepts the stream, buffers incoming items into a queue, and processes them using two workers running at different throttle speeds. This simulates uneven processing capacity and backpressure scenarios.

3. **Workers**
   Dummy worker threads that consume messages from the queue. Each worker has its own configurable delay to simulate slow and fast consumers.

4. **Response Summary**
   Once the client closes the stream, the server returns a `StreamResponse` summarizing:

   * total messages received
   * messages dropped due to queue overflow
   * status message

This demo focuses on clarity and replicability, keeping the implementation lightweight and easy to understand.

---

## Features

* Fully implemented **client-streaming RPC** using grpcio
* Structured message format with:

  * id, username, payload
  * message metadata
  * priority handling
  * server-side timestamping
* Internal server queue with configurable capacity
* Two workers with independent throttle speeds
* Message dropping logic when ingestion outpaces processing
* Clean separation of client, server, and shared proto definitions
* Simple, reproducible Python code without external complexity

---

## File Structure

```
.
├── README.md
├── client
│   ├── client.py        # gRPC client implementation
│   ├── data.py          # WorkItem generator / sample payloads
│   ├── main.py          # Client entrypoint
│   ├── requirements.txt # Client dependencies
│   └── producer.py      # Streaming producer logic
├── proto
│   ├── data_model.proto # WorkItem definition and enums
│   └── service.proto    # Service definition and StreamWork RPC
└── server
    ├── consumer.py      # gRPC service implementation
    ├── main.py          # Server entrypoint
    ├── requirements.txt # Server dependencies
    └── processor.py        # dummy message processor
```

---

## Protocol Buffers

Protocol Buffers (Protobuf) is a language-neutral, platform-neutral mechanism for serializing structured data. It is designed by Google to be compact, fast, and schema-driven. Instead of sending JSON or XML over the network, Protobuf uses a binary format that is significantly smaller and faster to encode/decode. Each `.proto` file defines the structure of messages and services in a strongly typed, version-safe way.

Protobuf enables:

* strict schemas for all request and response messages
* backward- and forward-compatible data evolution
* efficient serialization for high-throughput systems
* automatic code generation for multiple languages

In this project, all message types such as `WorkItem` and `StreamResponse` are defined in `.proto` files and compiled into Python classes used by the client and server.

---

## gRPC

gRPC is a high-performance, open-source RPC framework built on top of HTTP/2 and Protocol Buffers. It enables clients and servers to communicate using strongly typed, contract-driven APIs. gRPC supports multiple communication patterns, including unary, server-streaming, client-streaming, and bidirectional streaming.

Key features:

* efficient binary transport over HTTP/2
* built-in support for streaming
* automatic client and server code generation
* type-safe APIs guided by `.proto` contracts
* designed for microservices, real-time systems, and internal APIs

This project uses **client-streaming RPC**, where the client sends a sequence of `WorkItem` messages over a single stream, and the server returns a consolidated response when the stream ends. It demonstrates how streaming can be combined with worker queues, throttled processing, and controlled ingestion in Python.

## What This Demonstration Shows

* How to build a Python gRPC client-streaming RPC
* How to handle continuous ingestion on the server side
* Queue management and backpressure
* Worker pool behavior with uneven processing speeds
* Dropped message detection under load
* Clean separation of responsibilities in a streaming architecture

This project provides a simple but realistic foundation for ingestion pipelines used in analytics platforms, event processors, and high-throughput distributed systems.

