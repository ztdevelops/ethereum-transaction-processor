import traceback

from dto.get_transaction_response_dto import GetTransactionResponseDTO
from dto.get_transactions_response_dto import GetTransactionsResponseDTO
from exception.invalid_range_exception import InvalidRangeException
from exception.transaction_not_found_exception import TransactionNotFoundException
from repository.transactions_repository import TransactionsRepository


class TransactionsService:
    """
    Service for handling transaction-related operations.

    Attributes:
        __transactions_repository: An instance of TransactionsRepository.
    """
    __transactions_repository = None

    def __init__(self, transactions_repository: TransactionsRepository):
        """
        Initialize the TransactionsService with a TransactionsRepository instance.

        Args:
            transactions_repository: An instance of TransactionsRepository.
        """
        self.__transactions_repository = transactions_repository

    def perform_healthcheck(self):
        """
        Perform a health check to verify if the service is running.

        Returns:
            bool: True if the service is healthy, False otherwise.
        """
        return True

    def get_record_by_transaction_hash(self, transaction_hash: str):
        """
        Retrieve a transaction record by its hash.

        Args:
            transaction_hash: The hash of the transaction to retrieve.

        Returns:
            GetTransactionResponseDTO: The transaction data transfer object.
        """

        transaction = self.__transactions_repository.find_transaction_by_hash(transaction_hash)
        if transaction is None:
            raise TransactionNotFoundException(f"Transaction with hash {transaction_hash} not found")

        return GetTransactionResponseDTO(**transaction)

    def get_records_between_timestamps(self, start_timestamp: int, end_timestamp: int, page: int, page_size: int):
        """
        Retrieve transactions between two timestamps with pagination.

        Args:
            start_timestamp: The start timestamp for filtering transactions.
            end_timestamp: The end timestamp for filtering transactions.
            page: The page number for pagination.
            page_size: The number of transactions per page.

        Returns:
            GetTransactionsResponseDTO: A data transfer object containing the transactions and pagination info.

        Raises:
            Exception: If an error occurs while retrieving the transactions.
        """
        try:
            if start_timestamp > end_timestamp:
                raise InvalidRangeException("Start timestamp must be less than or equal to end timestamp")

            limit = page_size
            offset = (page - 1) * page_size

            transactions = self.__transactions_repository.find_transactions_between_timestamps(start_timestamp,
                                                                                               end_timestamp, limit,
                                                                                               offset)
            transaction_dtos = [GetTransactionResponseDTO(**transaction) for transaction in transactions if
                                transaction is not None]
            next_page = page + 1 if len(transactions) == page_size else None

            return GetTransactionsResponseDTO(
                transactions=transaction_dtos,
                page_size=page_size,
                next_page=next_page
            )
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            raise e
