# Kafka-Like Message Broker

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **lightweight**, *Python-based* message broker that emulates the core functionality of **Apache Kafka**. This project implements a simple **publish-subscribe** messaging system using **TCP/IP sockets**, where a broker stores messages in a persistent log file, producers send messages over the network, and consumers poll for messages. It serves as an **educational tool** to understand Kafka’s architecture and distributed messaging principles.

---

## Features

- **Broker**: Runs a TCP server on `localhost:9092`, storing messages in a log file and serving them to consumers.
- **Producer**: Sends messages to the broker over TCP/IP with acknowledgments.
- **Consumer**: Polls the broker using a persistent TCP connection, tracking offsets.
- **Persistent Storage**: Saves messages in `kafka_log.txt` with offset-based indexing.
- **Network Communication**: Leverages Python’s `socket` library for distributed TCP/IP communication.
- **Simple Protocol**: Uses `PRODUCE` and `CONSUME` commands for messaging.

---

## How It Works

This project replicates Kafka’s **decoupled producer-consumer** pattern in a simplified form:

1. **Broker** (`broker.py`):
   - Listens on `localhost:9092` for TCP connections.
   - Appends `PRODUCE` messages to `kafka_log.txt` (e.g., `offset:0 message:hello`).
   - Serves `CONSUME` requests with messages at the requested offset.
   - Supports **persistent consumer connections** for efficient polling.

2. **Producer** (`producer.py`):
   - Connects to the broker via TCP.
   - Sends messages prefixed with `PRODUCE` (e.g., `PRODUCE hello`).
   - Receives `ACK` responses (e.g., `ACK offset:0`).

3. **Consumer** (`consumer.py`):
   - Maintains a single TCP connection for polling.
   - Sends `CONSUME` requests with offsets (e.g., `CONSUME 0`).
   - Processes messages (e.g., `MESSAGE offset:0 hello`) and increments offsets.

The system operates over a **TCP/IP network**, enabling **distributed operation** across machines. Messages are stored **persistently** in a log file, and consumers use **offsets** to read messages sequentially, mirroring Kafka’s core mechanics.

---

## Comparison to Apache Kafka

### Similarities
- **Decoupled Architecture**: Producers and consumers interact via the broker, not shared memory.
- **Persistent Storage**: Messages are stored in a log file, like Kafka’s partition logs.
- **Offset-Based Consumption**: Consumers track positions with offsets.
- **Network-Based**: Uses TCP/IP for distributed communication.
- **Publish-Subscribe**: Supports message publishing and subscription.

### Differences
- **Single Log File**: No topics or partitions.
- **No Replication**: Lacks fault-tolerant data replication.
- **No Consumer Groups**: Supports one consumer, not parallel processing.
- **Simple Protocol**: Text-based `PRODUCE`/`CONSUME` vs. Kafka’s binary protocol.
- **Scalability**: Less optimized for high throughput.

This project is a **minimal foundation** for learning Kafka and can be extended with advanced features.

---

## Installation

### Prerequisites
- **Python 3.6+**
- No external dependencies (uses standard library: `socket`, `threading`, `os`)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/kafka-like-broker.git
   cd kafka-like-broker
   ```

2. Ensure the working directory is writable for `kafka_log.txt`.

---

## Usage

Run each component in a **separate terminal**:

1. **Start the Broker**:
   ```bash
   python broker.py
   ```
   **Output**:
   ```
   Broker started on localhost:9092
   ```

2. **Start the Consumer**:
   ```bash
   python consumer.py
   ```
   **Output**:
   ```
   Consumer started. Waiting for data...
   Connected to broker at localhost:9092
   ```

3. **Start the Producer**:
   ```bash
   python producer.py
   ```
   Enter messages (e.g., `hello`, `world`) and type `exit` to quit.

### Example Output
- **Producer**:
  ```
  What do you want to add? (type 'exit' to quit): hello
  Broker response: ACK offset:0
  What do you want to add? (type 'exit' to quit): world
  Broker response: ACK offset:1
  ```

- **Consumer**:
  ```
  Consumer started. Waiting for data...
  Connected to broker at localhost:9092
  Consumed: hello (offset: 0)
  Consumed: world (offset: 1)
  ```

- **Log File** (`kafka_log.txt`):
  ```
  offset:0 message:hello
  offset:1 message:world
  ```

---

## Project Structure

- **`broker.py`**: TCP server for storing and serving messages.
- **`producer.py`**: Client for sending messages to the broker.
- **`consumer.py`**: Client for polling messages with a persistent connection.
- **`kafka_log.txt`**: Log file for message storage (created by broker).
- **`requirements.txt`**: Empty (no external dependencies).
- **`LICENSE`**: MIT License.

---

## ⚠️ Limitations

- Single log file (no topics/partitions).
- No replication or fault tolerance.
- In-memory consumer offsets (reset on restart).
- Basic error handling, no consumer groups.

---

## 🔮 Future Enhancements

- Add **topics** with multiple log files.
- Persist **consumer offsets** for resumable consumption.
- Support **consumer groups** for parallel processing.
- Use a **binary/JSON protocol** for structured messages.
- Implement **replication** across multiple brokers.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

Report bugs or suggest features via [GitHub Issues](https://github.com/<your-username>/kafka-like-broker/issues).

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Inspired by **Apache Kafka**’s distributed streaming platform.
- Built as a learning project to explore **message brokers** and **network programming**.

---

*Created by [Your Name]*