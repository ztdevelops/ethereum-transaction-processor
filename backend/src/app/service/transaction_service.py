from src.app.dto.response.healthcheck_response_dto import HealthcheckResponseDTO
from src.app.repository.transaction_repository import TransactionRepository


class TransactionService:
    """
    Service class for handling transaction-related business logic.

    Attributes:
        transaction_repository (TransactionRepository): The repository instance for database interactions.
    """

    def __init__(self, transaction_repository: TransactionRepository):
        """
        Initializes the TransactionService with the given transaction repository.

        Args:
            transaction_repository (TransactionRepository): The repository instance for database interactions.
        """
        self.__transaction_repository = transaction_repository

    def perform_healthcheck(self):
        """
        Performs a health check to verify if the service is operational.

        Returns:
            HealthcheckResponseDTO: A DTO with the status of the service.
        """
        return HealthcheckResponseDTO(healthy=True)
