import asyncio
import json
import unittest
import uuid
from unittest.mock import AsyncMock, patch

from service.binance_service import BinanceService


class TestBinanceService(unittest.TestCase):

    @patch('service.binance_service.websockets.WebSocketClientProtocol', new_callable=AsyncMock)
    @patch('service.binance_service.websockets.connect', new_callable=AsyncMock)
    def setUp(self, MockWebSocketConnect, MockWebSocketClientProtocol):
        self.mock_ws_connect = MockWebSocketConnect
        self.mock_ws = MockWebSocketClientProtocol
        self.mock_ws_connect.return_value = self.mock_ws
        self.binance_service = BinanceService(ws=self.mock_ws)

    def test_get_ethusdt_price_cached(self):
        timestamp = 1513240363
        expected_price = 1000.0
        self.binance_service._BinanceService__ethusdt_cache[timestamp] = expected_price

        async def test():
            price = await self.binance_service.get_ethusdt_price(timestamp)
            self.assertEqual(price, expected_price)
            self.mock_ws_connect.assert_not_called()

        asyncio.run(test())

    def test_get_ethusdt_price_not_cached(self):
        timestamp = 1513240363
        expected_price = 1000.0
        request_id = uuid.uuid4()
        response = {
            "id": str(request_id),
            "result": [
                [timestamp * 1000, "0", "0", "0", str(expected_price), "0", "0", "0", "0", "0", "0"]
            ]
        }
        self.mock_ws.recv = AsyncMock(return_value=json.dumps(response))
        self.mock_ws_connect.return_value = self.mock_ws

        async def test():
            try:
                await asyncio.wait_for(self.binance_service._BinanceService__listen(), timeout=5)
            except asyncio.TimeoutError:
                pass

            price = await self.binance_service.get_ethusdt_price(timestamp, request_id)
            self.assertEqual(price, expected_price)
            self.mock_ws.send.assert_called_once()
            self.mock_ws.recv.assert_called()

        asyncio.run(test())
