import asyncio

from repository.transactions_repository import TransactionsRepository
from service.kafka_consumer_service import KafkaConsumerService
from service.transactions_service import TransactionsService
from utils.config import Config
from utils.mongodb_connector import MongoDBConnector

config = Config()

# Initialise Transactions service
db_connector = MongoDBConnector(config.get("MONGODB_URL"))
transactions_repository = TransactionsRepository(db_connector)
transactions_service = TransactionsService(transactions_repository)

# Initialise the Kafka consumer service
consumer_service = KafkaConsumerService(
    config.get("KAFKA_BROKER_URL"),
    config.get("KAFKA_GROUP_ID"),
    [config.get("KAFKA_TOPIC")]
)

# Consume messages from the Kafka topic
asyncio.run(
    consumer_service.consume_messages(
        transactions_service.handle_message
    )
)
