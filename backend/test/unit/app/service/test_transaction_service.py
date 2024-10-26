import unittest
from unittest.mock import MagicMock

from src.app.dto.response.healthcheck_response_dto import HealthcheckResponseDTO
from src.app.repository.transaction_repository import TransactionRepository
from src.app.service.transaction_service import TransactionService


class TestTransactionService(unittest.TestCase):
    def setUp(self):
        self.transaction_repository = MagicMock(spec=TransactionRepository)
        self.transaction_service = TransactionService(self.transaction_repository)

    def test_perform_healthcheck(self):
        # Arrange
        expected_response = HealthcheckResponseDTO(healthy=True)

        # Act
        response = self.transaction_service.perform_healthcheck()

        # Assert
        self.assertEqual(response, expected_response)