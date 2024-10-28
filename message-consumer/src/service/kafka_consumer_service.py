from typing import List

from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic


class KafkaConsumerService:
    """
    A service that consumes messages from a Kafka topic.

    Attributes:
        __consumer (Consumer): The Kafka consumer instance.
        __admin_client (AdminClient): The Kafka admin client instance.
    """
    __consumer = None
    __admin_client = None

    def __init__(self, broker_url: str, group_id: str, topics: list):
        """
        Initializes the KafkaConsumerService with the given broker URL, group ID, topics, and Avro schema.

        Args:
            broker_url (str): The URL of the Kafka broker to connect to.
            group_id (str): The consumer group ID.
            topics (list): The list of topics to subscribe to.
            schema (dict): The Avro schema for deserialization.
        """
        self.__consumer = Consumer({
            'bootstrap.servers': broker_url,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.__admin_client = AdminClient({'bootstrap.servers': broker_url})
        self.__create_topics_if_not_exists(topics)

        self.__consumer.subscribe(topics)

    async def consume_messages(self, callback):
        """
        Consumes messages from the subscribed topics and processes them.
        """
        while True:
            message = self.__consumer.poll(timeout=1.0)

            if message is None:
                print("No messages received")
                continue

            if message.error():
                print(f"Consumer error: {message.error()}")
                continue

            callback(message)

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
