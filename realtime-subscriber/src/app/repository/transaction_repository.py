from src.app.utils.database.db_connector import DatabaseConnector


class TransactionRepository:
    """
    Repository class for handling transaction-related database operations.

    Attributes:
        db_connector (DatabaseConnector): The database connector instance for database interactions.
    """
    def __init__(self, db_connector: DatabaseConnector):
        """
        Initializes the TransactionRepository with the given database connector.

        Args:
            db_connector (DatabaseConnector): The database connector instance for database interactions.
        """
        self.__db_connector = db_connector

