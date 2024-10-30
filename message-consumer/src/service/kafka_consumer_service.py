import asyncio
from typing import List

from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

from utils.config import Config


class KafkaConsumerService:
    """
    A service that consumes messages from a Kafka topic.

    Attributes:
        __consumer (Consumer): The Kafka consumer instance.
        __admin_client (AdminClient): The Kafka admin client instance.
    """
    __consumer = None
    __admin_client = None

    def __init__(self, config: Config, consumer: Consumer = None, admin_client: AdminClient = None):
        """
        Initializes the KafkaConsumerService with the given broker URL, group ID, topics, and Avro schema.

        Args:
            config (Config): The application configuration.
            consumer (Consumer): The Kafka consumer instance.
            admin_client (AdminClient): The Kafka admin client instance.
        """
        self.__consumer = consumer if consumer is not None else Consumer({
            'bootstrap.servers': config.get("KAFKA_BROKER_URL"),
            'group.id': config.get("KAFKA_GROUP_ID"),
            'auto.offset.reset': 'earliest'
        })

        self.__admin_client = admin_client if admin_client is not None else AdminClient({
            'bootstrap.servers': config.get("KAFKA_BROKER_URL")
        })

        topics = config.get("KAFKA_TOPIC").split(",")
        self.__create_topics_if_not_exists(topics)
        self.__consumer.subscribe(topics)

    async def consume_messages(self, callback):
        """
        Consumes messages from the subscribed topics and processes them.
        """
        while True:
            try:
                message = self.__consumer.poll(timeout=1.0)

                if message is None:
                    print("No messages received")
                    continue

                if message.error():
                    raise Exception(f"Consumer error: {message.error()}")

                callback(message)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                await asyncio.sleep(0.1)

        self.close()

    def close(self):
        """
        Closes the Kafka consumer.
        """
        self.__consumer.close()

    def __create_topics_if_not_exists(self, topics: List[str], num_partitions: int = 1, replication_factor: int = 1):
        topic_metadata = self.__admin_client.list_topics(timeout=10)
        for topic in topics:
            if topic not in topic_metadata.topics:
                new_topic = NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor)
                self.__admin_client.create_topics([new_topic])
                print(f"Topic '{topic}' created.")
            else:
                print(f"Topic '{topic}' already exists.")
