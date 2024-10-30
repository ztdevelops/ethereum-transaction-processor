import asyncio
import unittest
from unittest.mock import patch, MagicMock

from service.kafka_consumer_service import KafkaConsumerService


class TestKafkaConsumerService(unittest.TestCase):

    @patch('service.kafka_consumer_service.Config')
    @patch('service.kafka_consumer_service.Consumer')
    @patch('service.kafka_consumer_service.AdminClient')
    def setUp(self, MockAdminClient, MockConsumer, MockConfig):
        self.config = MockConfig.return_value
        self.consumer = MockConsumer.return_value
        self.admin_client = MockAdminClient.return_value
        self.config.get.side_effect = lambda key: {
            "KAFKA_BOOTSTRAP_SERVERS": "mock_bootstrap_servers",
            "KAFKA_GROUP_ID": "mock_group_id",
            "KAFKA_TOPIC": "mock_topic"
        }[key]

        self.kafka_consumer_service = KafkaConsumerService(self.config, self.consumer, self.admin_client)

    def test_consumes_messages_successfully(self):
        callback = MagicMock()
        mock_message = MagicMock()
        mock_message.error.return_value = None
        self.consumer.poll.return_value = mock_message

        async def test():
            try:
                await asyncio.wait_for(self.kafka_consumer_service.consume_messages(callback), timeout=5)
            except asyncio.TimeoutError:
                pass

        asyncio.run(test())
        callback.assert_called_with(mock_message)

    def test_handles_no_messages(self):
        self.consumer.poll.return_value = None
        callback = MagicMock()

        async def test():
            try:
                await asyncio.wait_for(self.kafka_consumer_service.consume_messages(callback), timeout=5)
            except asyncio.TimeoutError:
                pass

        asyncio.run(test())
        callback.assert_not_called()

    def test_handles_message_error(self):
        mock_message = MagicMock()
        mock_message.error.return_value = "mock_error"
        self.consumer.poll.return_value = mock_message
        callback = MagicMock()

        async def test():
            try:
                await asyncio.wait_for(self.kafka_consumer_service.consume_messages(callback), timeout=5)
            except asyncio.TimeoutError:
                pass

        asyncio.run(test())
        callback.assert_not_called()

    def test_creates_topics_if_not_exists(self):
        self.admin_client.list_topics.return_value.topics = {}
        self.kafka_consumer_service._KafkaConsumerService__create_topics_if_not_exists(["mock_topic"])
        self.assertEqual(self.admin_client.create_topics.call_count,
                         2)  # in constructor and in create_topics_if_not_exists

    def test_does_not_create_existing_topics(self):
        self.admin_client.list_topics.return_value.topics = {"mock_topic": None}
        self.kafka_consumer_service._KafkaConsumerService__create_topics_if_not_exists(["mock_topic"])
        self.admin_client.create_topics.assert_called_once()
