import json

from confluent_kafka import Producer
from hexbytes import HexBytes
from web3.datastructures import AttributeDict


class BrokerService:
    def __init__(self, broker_url: str):
        """
        Initializes the BrokerService with the given broker URL.

        Args:
            broker_url (str): The URL of the broker to connect to.
        """
        self.__broker_url = broker_url
        self.producer = Producer({"bootstrap.servers": self.__broker_url})

    def send(self, avro_schema_name: str, topic: str, message: dict):
        """
        Sends a message to the given topic.

        Args:
            avro_schema_name (str): The name of the Avro schema to use for serialisation.
            topic (str): The topic to send the message to.
            message (dict): The message to send.
        """

        if isinstance(message, AttributeDict):
            message = self.__convert_to_dict(message)

        json_message = json.dumps(message)
        self.producer.produce(topic, value=json_message.encode("utf-8"))

    def flush(self):
        self.producer.flush()

    def __convert_to_dict(self, attr_dict):
        if isinstance(attr_dict, AttributeDict):
            return {k: self.__convert_to_dict(v) for k, v in attr_dict.items()}
        elif isinstance(attr_dict, list):
            return [self.__convert_to_dict(i) for i in attr_dict]
        elif isinstance(attr_dict, HexBytes):
            return attr_dict.hex()
        return attr_dict
