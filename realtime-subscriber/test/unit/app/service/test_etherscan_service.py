import unittest
from unittest.mock import MagicMock

from etherscan import Etherscan

from src.app.service.etherscan_service import EtherscanService


class TestEtherscanService(unittest.TestCase):
    def setUp(self):
        etherscan_wrapper = Etherscan("asd")
        self.etherscan = MagicMock(spec=Etherscan)
        self.etherscan_service = EtherscanService(self.etherscan)