from utils.mongodb_connector import MongoDBConnector


class TransactionsRepository:
    """
    Repository class for handling transactions in the database.

    Attributes:
        __db_connector: An instance of MongoDBConnector to interact with the database.
    """
    __db_connector = None

    def __init__(self, db_connector: MongoDBConnector):
        """
        Initialize the TransactionsRepository with a MongoDBConnector instance.

        Args:
            db_connector: An instance of MongoDBConnector to interact with the database.
        """
        self.__db_connector = db_connector

    def __get_collection(self):
        """
        Get the transactions collection from the database.

        Returns:
            The transactions collection.
        """
        return self.__db_connector.get_collection("transactions", "transactions")

    def find_transaction_by_hash(self, transaction_hash: str):
        """
        Find a transaction by its hash.

        Args:
            transaction_hash: The hash of the transaction to find.

        Returns:
            The transaction document if found, otherwise None.
        """
        collection = self.__get_collection()
        return collection.find_one(
            {"transaction_hash": transaction_hash}
        )

    def find_transactions_between_timestamps(self, start_timestamp: int, end_timestamp: int, limit: int, offset: int):
        """
        Find transactions between two timestamps with pagination.

        Args:
            start_timestamp: The start timestamp for filtering transactions.
            end_timestamp: The end timestamp for filtering transactions.
            limit: The maximum number of transactions to return.
            offset: The number of transactions to skip.

        Returns:
            A list of transactions within the specified timestamps.
        """
        collection = self.__get_collection()
        return list(collection.find(
            {"timestamp":
                {
                    "$gte": start_timestamp,
                    "$lte": end_timestamp
                }
            }
        ).skip(offset).limit(limit))
