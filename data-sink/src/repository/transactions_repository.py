from utils.mongodb_connector import MongoDBConnector


class TransactionsRepository:
    """
    Repository class for managing transactions in the MongoDB database.
    """
    __db_connector = None

    def __init__(self, db_connector: MongoDBConnector):
        """
        Initializes the TransactionsRepository with a MongoDBConnector instance.

        Args:
            db_connector (MongoDBConnector): An instance of MongoDBConnector to interact with the MongoDB database.
        """
        self.__db_connector = db_connector

    def __get_collection(self):
        """
        Retrieves the 'transactions' collection from the MongoDB database.

        Returns:
            Collection: The 'transactions' collection.
        """
        return self.__db_connector.get_collection("transactions", "transactions")

    def write_transaction(self, transaction: dict):
        """
        Inserts a transaction document into the 'transactions' collection.

        Args:
            transaction (dict): A dictionary representing the transaction to be inserted.
        """
        collection = self.__get_collection()
        collection.insert_one(transaction)
