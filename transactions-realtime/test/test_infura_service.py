import asyncio
import unittest
from unittest.mock import patch, AsyncMock

from hexbytes import HexBytes
from service.infura_service import InfuraService
from web3._utils.filters import AsyncLogFilter
from web3.datastructures import AttributeDict


class TestInfuraService(unittest.TestCase):
    sample_event = AttributeDict({
        'args': AttributeDict({
            'sender': '0x68d3A973E7272EB388022a5C6518d9b2a2e66fBf',
            'recipient': '0x68d3A973E7272EB388022a5C6518d9b2a2e66fBf',
            'amount0': 7589647311700407623639,
            'amount1': -3118854356,
            'sqrtPriceX96': 50849625991721712974164,
            'liquidity': 8053172399126249259,
            'tick': -285194
        }),
        'event': 'Swap',
        'logIndex': 415,
        'transactionIndex': 124,
        'transactionHash': HexBytes('0xcca50659129b93837d2f04132cd67d42d9df4105e34286460bb0979e25167a31'),
        'address': '0x6AC6B053a2858bEa8AD758Db680198c16E523184',
        'blockHash': HexBytes('0x3dfeed720668e7e3b2abf6dc1b7550dc3f636486882d8921f1eb61c4a50e1396'),
        'blockNumber': 21055790
    })

    @patch('service.infura_service.Config')
    @patch('service.infura_service.EtherscanService')
    @patch('service.infura_service.BrokerService')
    @patch('service.infura_service.BinanceService')
    @patch('service.infura_service.AsyncWeb3')
    def setUp(self, MockAsyncWeb3, MockBinanceService, MockBrokerService, MockEtherscanService, MockConfig):
        self.mock_etherscan_service = MockEtherscanService()
        self.mock_broker_service = MockBrokerService()
        self.mock_binance_service = MockBinanceService()
        self.mock_config = MockConfig()
        self.mock_async_web3 = MockAsyncWeb3()

        self.mock_config.get.side_effect = lambda key: {
            "ETHERSCAN_CONTRACT_ADDRESS": "0x1234567890abcdef",
            "ETHERSCAN_CONTRACT_ABI_ADDRESS": "0xabcdef1234567890",
            "INFURA_POLL_INTERVAL": "10",
            "INFURA_PROJECT_ID": "abcdef1234567890"
        }[key]

        self.infura_service = InfuraService(
            etherscan_service=self.mock_etherscan_service,
            broker_service=self.mock_broker_service,
            binance_service=self.mock_binance_service,
            config=self.mock_config,
            async_web3=self.mock_async_web3
        )

    def test_listen_no_transactions(self):
        async def test():
            self.mock_binance_service.get_ethusdt_price.return_value = 1.0

            mock_filter = AsyncMock(spec=AsyncLogFilter)
            mock_filter.get_new_entries.return_value = []
            create_filter_mock = AsyncMock()
            create_filter_mock.return_value = mock_filter
            self.mock_async_web3.eth.contract.return_value.events.Swap.create_filter = create_filter_mock

            try:
                await asyncio.wait_for(self.infura_service.listen(), timeout=5)
            except asyncio.exceptions.TimeoutError:
                pass

            self.assertEqual(self.mock_etherscan_service.get_contract_abi.call_count, 0)
            self.assertEqual(self.mock_async_web3.eth.contract.call_count, 1)
            self.assertEqual(self.mock_async_web3.eth.get_transaction.call_count, 0)
            self.assertEqual(self.mock_async_web3.eth.get_block.call_count, 0)
            self.assertEqual(self.mock_binance_service.get_ethusdt_price.call_count, 0)
            self.assertEqual(self.mock_broker_service.send.call_count, 0)

        asyncio.run(test())

    def test_listen_with_transactions(self):
        async def test():
            self.mock_binance_service.get_ethusdt_price.return_value = asyncio.Future()
            self.mock_binance_service.get_ethusdt_price.return_value.set_result(1.0)
            mock_filter = AsyncMock(spec=AsyncLogFilter)
            mock_filter.get_new_entries.return_value = [self.sample_event]
            create_filter_mock = AsyncMock()
            create_filter_mock.return_value = mock_filter
            self.mock_async_web3.eth.contract.return_value.events.Swap.create_filter = create_filter_mock
            self.mock_async_web3.eth.get_transaction.return_value = asyncio.Future()
            self.mock_async_web3.eth.get_transaction.return_value.set_result({
                "gas": 123,
                "gasPrice": 123,
                "blockNumber": 123
            })
            self.mock_async_web3.eth.get_block.return_value = asyncio.Future()
            self.mock_async_web3.eth.get_block.return_value.set_result({
                "timestamp": 123
            })

            try:
                await asyncio.wait_for(self.infura_service.listen(), timeout=5)
            except asyncio.exceptions.TimeoutError:
                pass

            self.assertEqual(self.mock_etherscan_service.get_contract_abi.call_count, 0)
            self.assertEqual(self.mock_async_web3.eth.contract.call_count, 1)
            self.assertEqual(self.mock_async_web3.eth.get_transaction.call_count, 1)
            self.assertEqual(self.mock_async_web3.eth.get_block.call_count, 1)
            self.assertEqual(self.mock_binance_service.get_ethusdt_price.call_count, 1)
            self.assertEqual(self.mock_broker_service.send.call_count, 1)

        asyncio.run(test())
