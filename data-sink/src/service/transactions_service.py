import json

from confluent_kafka import cimpl
from repository.transactions_repository import TransactionsRepository


class TransactionsService:
    """
    Service class for handling transactions.
    """
    __transactions_repository = None

    def __init__(self, transactions_repository: TransactionsRepository):
        """
        Initializes the TransactionsService with a TransactionsRepository instance.

        Args:
            transactions_repository (TransactionsRepository): An instance of TransactionsRepository to interact with the MongoDB database.
        """
        self.__transactions_repository = transactions_repository

    def handle_message(self, transaction: cimpl.Message):
        """
        Processes and writes a transaction message to the MongoDB database.

        Args:
            transaction (cimpl.Message): A Kafka message containing the transaction data.
        """
        transaction_json_string = transaction.value().decode("utf-8")
        transaction = json.loads(transaction_json_string)
        self.__transactions_repository.write_transaction(transaction)
