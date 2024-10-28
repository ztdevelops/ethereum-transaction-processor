from pymongo import MongoClient


class MongoDBConnector:
    def __init__(self, mongodb_url: str):
        """
        Initializes the MongoDBConnector with the given MongoDB URL.

        Args:
            mongodb_url (str): The URL of the MongoDB database to connect to.
        """
        self.client = MongoClient(mongodb_url)

    def get_database(self, database_name: str):
        """
        Retrieves a database from the MongoDB client.

        Args:
            database_name (str): The name of the database to retrieve.

        Returns:
            Database: The MongoDB database.
        """
        return self.client[database_name]

    def get_collection(self, database_name: str, collection_name: str):
        """
        Retrieves a collection from the MongoDB client.

        Args:
            database_name (str): The name of the database to retrieve.
            collection_name (str): The name of the collection to retrieve.

        Returns:
            Collection: The MongoDB collection.
        """
        return self.get_database(database_name)[collection_name]
