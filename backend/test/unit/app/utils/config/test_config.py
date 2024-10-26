import unittest
from unittest.mock import patch

from src.app.utils.config.config import Config


class TestConfig(unittest.TestCase):
    @patch('src.app.utils.config.config.load_dotenv')
    @patch('src.app.utils.config.config.os.getenv')
    def test_singleton_instance(self, mock_getenv, mock_load_dotenv):
        mock_getenv.return_value = "postgresql://test_user:test_password@localhost:5432/test_db"
        config1 = Config()
        config2 = Config()

        self.assertEqual(config1, config2)
        self.assertEqual(config1["DATABASE_URL"], "postgresql://test_user:test_password@localhost:5432/test_db")

    @patch('src.app.utils.config.config.load_dotenv')
    @patch('src.app.utils.config.config.os.getenv')
    def test_get_database_url(self, mock_getenv, mock_load_dotenv):
        mock_getenv.return_value = "postgresql://test_user:test_password@localhost:5432/test_db"
        config = Config()
        self.assertEqual(config.get("DATABASE_URL"), "postgresql://test_user:test_password@localhost:5432/test_db")

    @patch('src.app.utils.config.config.load_dotenv')
    @patch('src.app.utils.config.config.os.getenv')
    def test_get_nonexistent_key_with_default(self, mock_getenv, mock_load_dotenv):
        mock_getenv.return_value = None
        config = Config()
        self.assertEqual(config.get("NONEXISTENT_KEY", "default_value"), "default_value")

    @patch('src.app.utils.config.config.load_dotenv')
    @patch('src.app.utils.config.config.os.getenv')
    def test_get_nonexistent_key_without_default(self, mock_getenv, mock_load_dotenv):
        mock_getenv.return_value = None
        config = Config()
        with self.assertRaises(KeyError):
            config["NONEXISTENT_KEY"]