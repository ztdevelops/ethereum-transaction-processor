import os

from dotenv import load_dotenv


class Config:
    """
    Singleton class for managing application configuration.

    This class loads environment variables from a .env file and provides
    access to configuration values.
    """
    __instance = None
    __configs = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance of the Config class is created.

        Returns:
            Config: The singleton instance of the Config class.
        """
        if not cls.__instance:
            cls.__instance = super(Config, cls).__new__(cls)
            load_dotenv()

            cls.__instance.__configs = {
                "KAFKA_BROKER_URL": os.getenv("KAFKA_BROKER_URL", "localhost:9092"),
                "DATABASE_URL": os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/postgres"),
                "ETHERSCAN_API_KEY": os.getenv("ETHERSCAN_API_KEY", "default-etherscan-api-key"),
                "ETHERSCAN_CONTRACT_ABI_ADDRESS": os.getenv("ETHERSCAN_CONTRACT_ABI_ADDRESS", "default-etherscan-contract-address"),
                "INFURA_PROJECT_ID": os.getenv("INFURA_PROJECT_ID", "default-infura-project-id"),
                "INFURA_POLL_INTERVAL": os.getenv("INFURA_POLL_INTERVAL", 5)
            }

        return cls.__instance

    def __getitem__(self, key):
        """
        Gets the value of the specified configuration key.

        Args:
            key (str): The configuration key.

        Returns:
            str: The value of the configuration key.
        """
        return self.__configs[key]

    def get(self, key, default=None):
        """
        Gets the value of the specified configuration key, with an optional default.

        Args:
            key (str): The configuration key.
            default (any, optional): The default value to return if the key is not found.

        Returns:
            any: The value of the configuration key, or the default value if the key is not found.
        """
        return self.__configs.get(key, default)
