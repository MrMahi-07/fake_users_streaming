# 🚀 fake_users_streaming

A real-time streaming data pipeline that generates fake user data, streams it via Kafka, processes it using Spark Structured Streaming, and writes the final output into PostgreSQL — all orchestrated with Airflow and containerized with Docker.

---

## 🧠 Overview

This project simulates a production-grade streaming architecture for experimentation and learning. It integrates:

- Python + Faker for synthetic data generation  
- Apache Kafka (in KRaft mode) for real-time event streaming  
- Apache Spark Structured Streaming for stream processing  
- PostgreSQL as the destination for processed data  
- Apache Airflow to schedule and orchestrate workflows  
- Docker Compose for local deployment  

---

## ⚡ Kafka in KRaft Mode

This setup uses KRaft mode (Kafka without Zookeeper), which simplifies the architecture and is fully supported in Kafka 3.5+.

### 🛠️ KRaft Configuration Notes

- Kafka is running with KRaft mode enabled, eliminating the need for Zookeeper.
- Sample configuration highlights:
  
```properties
process.roles=controller,broker
controller.listener.names=CONTROLLER
listeners=INTERNAL://:29092,EXTERNAL://:9092,CONTROLLER://:9093
advertised.listeners=INTERNAL://kafka:29092,EXTERNAL://localhost:9092
listener.security.protocol.map=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT
inter.broker.listener.name=INTERNAL
```
---

## ⚙️ How It Works

1. A script generates fake user data using the Faker library  
2. The data is published to a Kafka topic  
3. Spark Structured Streaming reads the Kafka stream, processes the data, and writes the result to PostgreSQL  
4. Airflow schedules and manages the entire pipeline  

---

## 🚀 Getting Started

### 1. Clone the repository

    git clone https://github.com/MrMahi-07/fake_users_streaming.git
    cd fake_users_streaming

### 2. Start the stack with Docker Compose

    cd docker
    docker-compose up --build

Services launched:
- Kafka (KRaft mode)
- Spark (master + worker)
- PostgreSQL (with pre-created database)
- Airflow (webserver & scheduler)

---

## 👨‍💻 Author

Built with ☕ and containers by MrMahi-07

---

## 📜 License

MIT License — see LICENSE for more info.
