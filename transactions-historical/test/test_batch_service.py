import asyncio
import json
import unittest
from unittest.mock import patch

from service.batch_service import BatchService


class TestBatchService(unittest.TestCase):
    sample_historical_transaction = json.loads(
        """
        {
            "blockNumber": "4730207",
            "timeStamp": "1513240363",
            "hash": "0xe8c208398bd5ae8e4c237658580db56a2a94dfa0ca382c99b776fa6e7d31d5b4",
            "nonce": "406",
            "blockHash": "0x022c5e6a3d2487a8ccf8946a2ffb74938bf8e5c8a3f6d91b41c56378a96b5c37",
            "from": "0x642ae78fafbb8032da552d619ad43f1d81e4dd7c",
            "contractAddress": "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2",
            "to": "0x4e83362442b8d1bec281594cea3050c8eb01311c",
            "value": "5901522149285533025181",
            "tokenName": "Maker",
            "tokenSymbol": "MKR",
            "tokenDecimal": "18",
            "transactionIndex": "81",
            "gas": "940000",
            "gasPrice": "32010000000",
            "gasUsed": "77759",
            "cumulativeGasUsed": "2523379",
            "input": "deprecated",
            "confirmations": "16341697"
        }
        """
    )

    @patch('service.batch_service.Config')
    @patch('service.batch_service.EtherscanService')
    @patch('service.batch_service.BrokerService')
    @patch('service.batch_service.BinanceService')
    def setUp(self, MockBinanceService, MockBrokerService, MockEtherscanService, MockConfig):
        self.mock_etherscan_service = MockEtherscanService()
        self.mock_broker_service = MockBrokerService()
        self.mock_binance_service = MockBinanceService()
        self.mock_config = MockConfig()

        self.mock_config.get.side_effect = lambda key: {
            "ETHERSCAN_HISTORICAL_FIRST_BLOCK": "0",
            "ETHERSCAN_HISTORICAL_LAST_BLOCK": "100",
            "ETHERSCAN_HISTORICAL_BATCH_SIZE": "10",
            "ETHERSCAN_CONTRACT_ADDRESS": "0x1234567890abcdef"
        }[key]

        self.batch_service = BatchService(
            etherscan_service=self.mock_etherscan_service,
            broker_service=self.mock_broker_service,
            binance_service=self.mock_binance_service,
            config=self.mock_config
        )

    def test_start_no_historical_data(self):
        asyncio.run(self.batch_service.start())
        self.assertEqual(self.mock_etherscan_service.get_historical_data.call_count, 10)
        self.assertEqual(self.mock_broker_service.send.call_count, 0)
        self.assertEqual(self.mock_binance_service.get_ethusdt_price.call_count, 0)
        self.assertEqual(self.mock_broker_service.flush.call_count, 10)

    def test_start_calls_etherscan_service_get_historical_data_returns_transactions(self):
        self.mock_binance_service.get_ethusdt_price.return_value = asyncio.Future()
        self.mock_binance_service.get_ethusdt_price.return_value.set_result(1.0)

        self.mock_etherscan_service.get_historical_data.return_value = {
            "status": "1",
            "message": "OK",
            "result": [
                self.sample_historical_transaction,
                self.sample_historical_transaction,
                self.sample_historical_transaction
            ]
        }

        asyncio.run(self.batch_service.start())
        self.assertEqual(self.mock_etherscan_service.get_historical_data.call_count, 10)
        self.assertEqual(self.mock_broker_service.send.call_count, 30)
        self.assertEqual(self.mock_binance_service.get_ethusdt_price.call_count, 30)
        self.assertEqual(self.mock_broker_service.flush.call_count, 10)
