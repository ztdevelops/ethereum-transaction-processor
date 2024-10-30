import json
import unittest
from unittest.mock import MagicMock

from confluent_kafka import Message

from repository.transactions_repository import TransactionsRepository
from service.transactions_service import TransactionsService


class TestTransactionsService(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=TransactionsRepository)
        self.transactions_service = TransactionsService(self.mock_repository)

    def test_processes_valid_transaction_message(self):
        mock_message = MagicMock(spec=Message)
        mock_message.value.return_value = b'{"id": 1, "amount": 100.0, "currency": "USD"}'

        self.transactions_service.handle_message(mock_message)
        self.mock_repository.write_transaction.assert_called_once_with({"id": 1, "amount": 100.0, "currency": "USD"})

    def test_handles_invalid_json_message(self):
        mock_message = MagicMock(spec=Message)
        mock_message.value.return_value = b'invalid_json'

        with self.assertRaises(json.JSONDecodeError):
            self.transactions_service.handle_message(mock_message)

    def test_handles_empty_message(self):
        mock_message = MagicMock(spec=Message)
        mock_message.value.return_value = b''

        with self.assertRaises(json.JSONDecodeError):
            self.transactions_service.handle_message(mock_message)


if __name__ == '__main__':
    unittest.main()
