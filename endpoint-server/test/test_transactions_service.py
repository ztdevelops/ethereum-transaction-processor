import unittest
from unittest.mock import MagicMock

from dto.get_transaction_response_dto import GetTransactionResponseDTO
from dto.get_transactions_response_dto import GetTransactionsResponseDTO
from exception.invalid_range_exception import InvalidRangeException
from exception.transaction_not_found_exception import TransactionNotFoundException
from repository.transactions_repository import TransactionsRepository
from service.transactions_service import TransactionsService


class TestTransactionsService(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=TransactionsRepository)
        self.transactions_service = TransactionsService(self.mock_repository)

    def test_performs_healthcheck_successfully(self):
        result = self.transactions_service.perform_healthcheck()
        self.assertTrue(result)

    def test_retrieves_transaction_by_hash(self):
        mock_transaction = {
            "id": 1,
            "hash": "abc123",
            "amount": 100.0,
            "transaction_hash": "abc123",
            "ethusdt_close_price": 3000.0,
            "timestamp": 1609459200,
            "transaction_fee_in_eth": 0.01,
            "transaction_fee_in_usdt": 30.0
        }
        self.mock_repository.find_transaction_by_hash.return_value = mock_transaction

        result = self.transactions_service.get_record_by_transaction_hash("abc123")
        self.assertEqual(result, GetTransactionResponseDTO(**mock_transaction))

    def test_handles_transaction_not_found_by_hash(self):
        self.mock_repository.find_transaction_by_hash.return_value = None

        with self.assertRaises(TransactionNotFoundException):
            self.transactions_service.get_record_by_transaction_hash("nonexistent_hash")

    def test_retrieves_transactions_between_timestamps(self):
        mock_transactions = [
            {
                "id": 1,
                "hash": "abc123",
                "amount": 100.0,
                "transaction_hash": "abc123",
                "ethusdt_close_price": 3000.0,
                "timestamp": 1609459200,
                "transaction_fee_in_eth": 0.01,
                "transaction_fee_in_usdt": 30.0
            },
            {
                "id": 2,
                "hash": "def456",
                "amount": 200.0,
                "transaction_hash": "def456",
                "ethusdt_close_price": 3100.0,
                "timestamp": 1609545600,
                "transaction_fee_in_eth": 0.02,
                "transaction_fee_in_usdt": 60.0
            }
        ]
        self.mock_repository.find_transactions_between_timestamps.return_value = mock_transactions

        result = self.transactions_service.get_records_between_timestamps(1609459200, 1609545600, 1, 2)
        expected_dto = GetTransactionsResponseDTO(
            transactions=[GetTransactionResponseDTO(**t) for t in mock_transactions],
            page_size=2,
            next_page=2
        )
        self.assertEqual(result, expected_dto)

    def test_handles_no_transactions_between_timestamps(self):
        self.mock_repository.find_transactions_between_timestamps.return_value = []

        result = self.transactions_service.get_records_between_timestamps(1609459200, 1609545600, 1, 2)
        expected_dto = GetTransactionsResponseDTO(
            transactions=[],
            page_size=2,
            next_page=None
        )
        self.assertEqual(result, expected_dto)

    def test_handles_invalid_range_exception(self):
        with self.assertRaises(InvalidRangeException):
            self.transactions_service.get_records_between_timestamps(1609545600, 1609459200, 1, 2)

    def test_handles_exception_during_retrieval(self):
        self.mock_repository.find_transactions_between_timestamps.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            self.transactions_service.get_records_between_timestamps(1609459200, 1609545600, 1, 2)
        self.assertEqual(str(context.exception), "Database error")


if __name__ == '__main__':
    unittest.main()
