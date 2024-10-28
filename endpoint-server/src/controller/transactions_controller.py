from fastapi import APIRouter, HTTPException, Query
from fastapi import status

from service.transactions_service import TransactionsService

router = APIRouter()


class TransactionsController:
    """
    Controller for handling transaction-related API endpoints.

    Attributes:
        __transactions_service: An instance of TransactionsService.
        __router: An instance of APIRouter
    """

    __transactions_service = None
    __router = None

    def __init__(self, transactions_service: TransactionsService):
        """
        Initialize the TransactionsController with a TransactionsService instance.

        Args:
            transactions_service: An instance of TransactionsService.
        """
        self.__transactions_service = transactions_service
        self.__router = APIRouter(
            prefix="/api/v1/transactions",
            tags=["Transactions"],
        )

        # Registering routes for transaction-related endpoints
        self.__router.add_api_route("/healthz", self.healthz, methods=["GET"])
        self.__router.add_api_route("", self.get_transactions_between_timestamps, methods=["GET"])
        self.__router.add_api_route("/{transaction_hash}", self.get_transaction_by_hash, methods=["GET"])

    def get_router(self):
        """
        Get the APIRouter instance for this controller.

        Returns:
            The APIRouter instance.
        """
        return self.__router

    async def healthz(self):
        """
        Health check endpoint to verify if the service is running.

        Returns:
            A JSON response indicating the health status.

        Raises:
            HTTPException: If the service is unhealthy.
        """
        healthy = self.__transactions_service.perform_healthcheck()
        if not healthy:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service is unhealthy",
            )

        return {"status": "ok"}

    async def get_transaction_by_hash(self, transaction_hash: str):
        """
        Retrieve a transaction by its hash.

        Args:
            transaction_hash: The hash of the transaction to retrieve.

        Returns:
            The transaction data.

        Raises:
            HTTPException: If an error occurs while retrieving the transaction.
        """
        try:
            return self.__transactions_service.get_record_by_transaction_hash(transaction_hash)
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {e}",
            )

    async def get_transactions_between_timestamps(
            self,
            start_timestamp: int = Query(...),
            end_timestamp: int = Query(...),
            page: int = Query(1, gt=0),
            page_size: int = Query(10, gt=0)
    ):
        """
        Retrieve transactions between two timestamps with pagination.

        Args:
            start_timestamp: The start timestamp for filtering transactions.
            end_timestamp: The end timestamp for filtering transactions.
            page: The page number for pagination.
            page_size: The number of transactions per page.

        Returns:
            A list of transactions within the specified timestamps.

        Raises:
            HTTPException: If an error occurs while retrieving the transactions.
        """
        try:
            return self.__transactions_service.get_records_between_timestamps(start_timestamp, end_timestamp, page,
                                                                              page_size)
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {e}",
            )
