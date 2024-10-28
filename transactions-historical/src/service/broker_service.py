import json

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic
from hexbytes import HexBytes
from web3.datastructures import AttributeDict


class BrokerService:
    """
    Service for sending messages to a broker.

    Attributes:
        __broker_url (str): The URL of the broker to connect to.
        __producer (Producer): The Kafka producer instance.
        __admin_client (AdminClient): The Kafka admin client instance.
    """
    __broker_url = None
    __producer = None
    __admin_client = None

    def __init__(self, broker_url: str):
        """
        Initializes the BrokerService with the given broker URL.

        Args:
            broker_url (str): The URL of the broker to connect to.
        """
        self.__broker_url = broker_url
        self.__producer = Producer({"bootstrap.servers": self.__broker_url})
        self.__admin_client = AdminClient({"bootstrap.servers": self.__broker_url})
        self.__create_topic_if_not_exists("transactions")

    def send(self, avro_schema_name: str, topic: str, message: dict):
        """
        Sends a message to the given topic.

        Args:
            avro_schema_name (str): The name of the Avro schema to use for serialization.
            topic (str): The topic to send the message to.
            message (dict): The message to send.
        """
        if isinstance(message, AttributeDict):
            message = self.__convert_to_dict(message)

        json_message = json.dumps(message)
        self.__producer.produce(topic, value=json_message.encode("utf-8"))

    def flush(self):
        """
        Flushes the producer, ensuring all messages are sent.
        """
        self.__producer.flush()

    def __convert_to_dict(self, attr_dict):
        """
        Recursively converts AttributeDict and HexBytes objects to regular Python dictionaries and strings.

        Args:
            attr_dict (AttributeDict or list or HexBytes): The object to convert.

        Returns:
            dict or list or str: The converted object.
        """
        if isinstance(attr_dict, AttributeDict):
            return {k: self.__convert_to_dict(v) for k, v in attr_dict.items()}
        elif isinstance(attr_dict, list):
            return [self.__convert_to_dict(i) for i in attr_dict]
        elif isinstance(attr_dict, HexBytes):
            return attr_dict.hex()
        return attr_dict

    def __create_topic_if_not_exists(self, topic: str, num_partitions: int = 1, replication_factor: int = 1):
        """
        Creates a Kafka topic if it does not exist.

        Args:
            topic (str): The name of the topic to create.
            num_partitions (int): The number of partitions for the topic.
            replication_factor (int): The replication factor for the topic.
        """
        topic_metadata = self.__admin_client.list_topics(timeout=10)
        if topic not in topic_metadata.topics:
            new_topic = NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor)
            self.__admin_client.create_topics([new_topic])
            print(f"Topic '{topic}' created.")
        else:
            print(f"Topic '{topic}' already exists.")
