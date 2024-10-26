from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseConnector:
    """
    Database connector class for managing database sessions.

    Attributes:
        __engine (Engine): SQLAlchemy engine instance for database connections.
        __SessionLocal (sessionmaker): SQLAlchemy session factory.
    """

    def __init__(self, database_url: str):
        """
        Initializes the DatabaseConnector with the given database URL.

        Args:
            database_url (str): The database URL for creating the engine.
        """
        self.__engine = create_engine(database_url)
        self.__SessionLocal = sessionmaker(
            autocommit=False, autoflush=True, bind=self.__engine)

    @contextmanager
    def get_db(self):
        """
        Provides a transactional scope for database operations.

        Yields:
            Session: A SQLAlchemy session object.
        """
        db = self.__SessionLocal()
        try:
            yield db
        finally:
            db.close()
