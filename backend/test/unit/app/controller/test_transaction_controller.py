import asyncio
import unittest
from fastapi.exceptions import HTTPException
from unittest.mock import MagicMock

from starlette import status

from src.app.controller.transaction_controller import TransactionController
from src.app.dto.response.healthcheck_response_dto import HealthcheckResponseDTO
from src.app.service.transaction_service import TransactionService


class TestTransactionController(unittest.TestCase):
    def setUp(self):
        self.transaction_service = MagicMock(spec=TransactionService)
        self.transaction_controller = TransactionController(self.transaction_service)

    def test_get_router(self):
        # Act
        router = self.transaction_controller.get_router()

        # Assert
        self.assertIsNotNone(router)

    def test_healthz_healthy_returns_true(self):
        async def test():
            # Arrange
            self.transaction_service.perform_healthcheck.return_value = HealthcheckResponseDTO(healthy=True)
            expected_response = HealthcheckResponseDTO(healthy=True)

            # Act
            response = await self.transaction_controller.healthz()

            # Assert
            self.assertEqual(response, expected_response)

        asyncio.run(test())


    def test_healthz_unhealthy_returns_false(self):
        async def test():
            # Arrange
            self.transaction_service.perform_healthcheck.side_effect = Exception

            # Act & Assert
            with self.assertRaises(HTTPException) as context:
                await self.transaction_controller.healthz()
            self.assertEqual(context.exception.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

        asyncio.run(test())
