import unittest
from unittest.mock import patch

from service.broker_service import BrokerService


class TestBrokerService(unittest.TestCase):

    @patch('service.broker_service.Producer')
    @patch('service.broker_service.AdminClient')
    def setUp(self, MockAdminClient, MockProducer):
        self.mock_producer = MockProducer.return_value
        self.mock_admin_client = MockAdminClient.return_value
        self.broker_service = BrokerService('mock_broker_url', self.mock_producer, self.mock_admin_client)

    def test_send_message_to_topic(self):
        message = {"key": "value"}
        self.broker_service.send("mock_schema", "mock_topic", message)
        self.mock_producer.produce.assert_called_once_with("mock_topic", value=b'{"key": "value"}')

    def test_send_message_with_attribute_dict(self):
        from web3.datastructures import AttributeDict
        message = AttributeDict({"key": "value"})
        self.broker_service.send("mock_schema", "mock_topic", message)
        self.mock_producer.produce.assert_called_once_with("mock_topic", value=b'{"key": "value"}')

    def test_flush_producer(self):
        self.broker_service.flush()
        self.mock_producer.flush.assert_called_once()

    def test_create_topic_if_not_exists(self):
        self.mock_admin_client.list_topics.return_value.topics = {}
        self.broker_service._BrokerService__create_topic_if_not_exists("new_topic")
        self.assertEqual(self.mock_admin_client.create_topics.call_count,
                         2)  # in constructor and in create_topic_if_not_exists

    def test_topic_already_exists(self):
        self.mock_admin_client.list_topics.return_value.topics = {"existing_topic": None}
        self.broker_service._BrokerService__create_topic_if_not_exists("existing_topic")
        self.mock_admin_client.create_topics.assert_called_once()  # in constructor
