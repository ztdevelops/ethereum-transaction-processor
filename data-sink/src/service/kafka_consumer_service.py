from confluent_kafka import Consumer


class KafkaConsumerService:
    """
    A service that consumes messages from a Kafka topic.
    """
    __consumer = None

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
