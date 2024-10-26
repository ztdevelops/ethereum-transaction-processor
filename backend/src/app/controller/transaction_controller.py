from fastapi import APIRouter, HTTPException
from fastapi import status

from src.app.service.transaction_service import TransactionService

router = APIRouter()


class TransactionController:
    """
    Controller for handling transaction-related API endpoints.

    Attributes:
        transaction_service (TransactionService): Service for handling transaction logic.
        router (APIRouter): Router for registering API routes.
    """

    def __init__(self, transaction_service: TransactionService):
        """
        Initializes the TransactionController with the given transaction service.
        Also initializes the router with the transaction API routes.

        APIRouter is initialised with the prefix "/api/v1/transaction" and the tag "Transaction".

        Args:
            transaction_service (TransactionService): The service to handle transaction logic.
        """
        self.__transaction_service = transaction_service
        self.__router = APIRouter(
            prefix="/api/v1/transactions",
            tags=["Transaction"],
        )

        self.__router.add_api_route("/healthz", self.healthz, methods=["GET"])

    def get_router(self):
        """
         Returns the router with registered API routes.

         Returns:
             APIRouter: The router with registered API routes.
         """
        return self.__router

    async def healthz(self):
        """
        Health check endpoint to verify if the service is healthy.
        Hits the transaction service to check if it is healthy.

        Raises:
            HTTPException: If the service is unhealthy.

        Returns:
            dict: A dictionary with the status of the service.
        """
        try:
            response = self.__transaction_service.perform_healthcheck()
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service is unhealthy",
            )

