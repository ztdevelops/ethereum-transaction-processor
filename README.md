# Ethereum Transaction Processing System
## Overview
This project involves building a system that processes Ethereum blockchain transactions, both in real-time and historical data, and integrates with external blockchain-related services to enrich transaction details. It includes the development of a RESTful API, enabling users to query and analyse the processed data efficiently. The system demonstrates a full-stack implementation, showcasing backend processing for data ingestion, external API integration, and API design for data retrieval.

## Table of Contents
1. [Requirements](#requirements)
2. [Environment Setup](#environment-setup)
3. [Running the Application](#running-the-application)
4. [Design Considerations](#design-considerations)

## Requirements
Ensure that the following are installed on your device:
1. [Docker](https://docs.docker.com/get-docker/)
2. [Docker Compose](https://docs.docker.com/compose/install/)

## Environment Setup
1. Clone the repository:
```bash
git clone https://github.com/ztdevelops/ethereum-transaction-processor.git
```
2. Change directory to the project root:
```bash
cd ethereum-transaction-processor
```
3. Create a `.env` file in the project root and add the following environment variables:
```bash
MONGODB_URL=mongodb://root:password@db:27017
KAFKA_BROKER_URL=broker:9092
KAFKA_GROUP_ID=kafka-consumer-group
KAFKA_TOPIC=transactions
ETHERSCAN_CONTRACT_ADDRESS=0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640
ETHERSCAN_CONTRACT_ABI_ADDRESS=0x8f8EF111B67C04Eb1641f5ff19EE54Cda062f163
ETHERSCAN_HISTORICAL_FIRST_BLOCK=0
ETHERSCAN_HISTORICAL_LAST_BLOCK=27025780
ETHERSCAN_HISTORICAL_BATCH_SIZE=10000
INFURA_POLL_INTERVAL=3
INFURA_PROJECT_ID=
ETHERSCAN_API_KEY=
```
Alternatively, copy and paste the `.env.example` file and rename it to `.env`.
Fill in the variables for `INFURA_PROJECT_ID` and `ETHERSCAN_API_KEY`.

## Running the Application
1. Start the application:
```bash
docker-compose -p etp up -d --build
```
2. Verify that the application has started successfully:
```bash
docker ps -a

# Output
CONTAINER ID   IMAGE                             COMMAND                  CREATED              STATUS                        PORTS                          NAMES
bf3b935250ed   etp-endpoint-server             "fastapi run src/mai…"   About a minute ago   Up 42 seconds (healthy)       0.0.0.0:8000->8000/tcp         etp-endpoint-server-1
3f35e0e7f66d   etp-message-consumer            "python3 src/main.py"    About a minute ago   Up 12 seconds                                                etp-message-consumer-1
a7cdcdcd6191   etp-db-indexing-sidecar         "python3 main.py"        About a minute ago   Exited (0) 43 seconds ago                                    etp-db-indexing-sidecar-1
4208ad9a2223   etp-transactions-realtime       "python3 src/main.py"    9 minutes ago        Up 12 seconds                                                etp-transactions-realtime-1
1a035e996412   etp-transactions-historical     "python3 src/main.py"    About an hour ago    Up 12 seconds                                                etp-transactions-historical-1
f6b9ad98f60a   confluentinc/cp-kafka:7.6.3       "/etc/confluent/dock…"   About an hour ago    Up 43 seconds (healthy)       9092/tcp                       etp-broker-1
dcedb40378c2   confluentinc/cp-zookeeper:7.6.3   "/etc/confluent/dock…"   About an hour ago    Up About a minute (healthy)   2181/tcp, 2888/tcp, 3888/tcp   etp-zookeeper-1
f93d247fb660   mongo:8.0.3                       "docker-entrypoint.s…"   About an hour ago  
```
3. Access the API documentation at `http://localhost:8000/docs`.
4. Tear down the application:
```bash
docker compose -p etp down -v
```
5. Testing the application:
   The tests can be viewed as part of GitHub Actions.

## Design Considerations
The application is designed to process Ethereum transactions in real-time and historical data.
It is composed of the following components:
1. **Message Consumer**: Consumes messages from a Kafka topic and processes them.
2. **Transactions (Historical)**: Fetches historical transactions in batches from an external API and writes them to Kafka.
3. **Transactions (Realtime)**: Fetches real-time transactions from an API and writes them to Kafka.
4. **Endpoint Server**: Provides a RESTful interface to query the processed data.
5. **Database Indexing Sidecar**: Indexes fields that are read frequently in MongoDB and exits after indexing is complete.

### Architecture Diagram
![Architecture Diagram](./assets/overview.png)

### Decoupled Components
The system was designed with decoupled components to ensure that each component is responsible for its own task. This ensures that the components can be scaled individually and perform independently. This is achieved through event-driven architecture using Kafka as the bridge for communication, allowing asynchronous processing.

### NoSQL Database (MongoDB)
This system requires heavy read-write operations without the need to join records from different collections. MongoDB was chosen for its flexibility and scalability. It stores data in JSON-like documents, making it easy to store and retrieve data. It also supports horizontal scaling, which is important for handling large volumes of data.

### Message Broker (Kafka)
Kafka was chosen as the message broker for its partitioning capabilities, which allow parallel processing of messages across multiple consumers. Kafka provides fault tolerance and high availability, ensuring messages are not lost in the event of a failure.

### Websockets
Websockets were used to handle continuous data ingestion, such as with real-time events and fetching exchange rates. This minimises the overhead of establishing new connections for each request, allowing for real-time updates.

### In-Memory Caching
When receiving a batch of transactions, the system caches frequently accessed data such as exchange rates to reduce external API calls. This caching mechanism improves performance by acting as a lightweight, efficient store for transient data.
