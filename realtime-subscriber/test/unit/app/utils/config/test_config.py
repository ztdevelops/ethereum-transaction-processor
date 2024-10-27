import unittest
from unittest.mock import patch

from src.app.utils.config.config import Config


class TestConfig(unittest.TestCase):

    @patch('src.app.utils.config.config.load_dotenv')
    @patch('src.app.utils.config.config.os.getenv')
    def setUp(self, mock_getenv, mock_load_dotenv):
        mock_load_dotenv.side_effect = None
        mock_getenv.return_value = "postgresql://postgres:password@localhost:5432/postgres"
        Config()

    def test_singleton_instance(self):
        config1 = Config()
        config2 = Config()

        self.assertEqual(config1, config2)

    def test_get_database_url(self):
        config = Config()
        self.assertEqual(config.get("DATABASE_URL"), "postgresql://postgres:password@localhost:5432/postgres")

    def test_get_nonexistent_key_without_default(self):
        config = Config()
        with self.assertRaises(KeyError):
            config["NONEXISTENT_KEY"]
