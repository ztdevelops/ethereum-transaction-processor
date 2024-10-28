import asyncio
import json
import uuid

import websockets
from cachetools import TTLCache


class BinanceService:
    """
    A service class to interact with the Binance API using websockets.

    Attributes:
        BINANCE_API_BASE_URL (str): The base URL for the Binance API.
        __api_key (str): The API key for authenticating requests to the Binance API.
        __ws (websockets.WebSocketClientProtocol): The WebSocket connection to the Binance API.
        __pending_requests (dict): A dictionary of pending requests.
        __ethusdt_cache (TTLCache): A cache for storing ETH/USDT prices.
    """
    BINANCE_API_BASE_URL = "wss://ws-api.binance.com:443/ws-api/v3"
    __api_key = None
    __ws = None
    __pending_requests = None
    __ethusdt_cache = None

    def __init__(self, cache_ttl: int = 60):
        """
        Initializes the BinanceService instance.

        Args:
            cache_ttl (int): Time-to-live for cache entries in seconds. Defaults to 60 seconds.
        """
        self.__pending_requests = {}
        self.__ethusdt_cache = TTLCache(maxsize=100, ttl=cache_ttl)

    async def __ws_connect(self):
        """
        Establishes a WebSocket connection to the Binance API if not already connected.
        """
        if self.__ws:
            return

        self.__ws = await websockets.connect(self.BINANCE_API_BASE_URL)
        asyncio.create_task(self.__listen())

    async def get_ethusdt_price(self, timestamp: int):
        """
        Fetches the ETH/USDT price at a given timestamp.

        Args:
            timestamp (int): The timestamp for which to fetch the price.

        Returns:
            float: The close price of ETH/USDT at the given timestamp.
        """
        if timestamp in self.__ethusdt_cache:
            return self.__ethusdt_cache[timestamp]

        await self.__ws_connect()
        request_id = uuid.uuid4()
        payload = {
            "id": str(request_id),
            "method": "klines",
            "params": {
                "symbol": "ETHUSDT",
                "interval": "1m",
                "limit": 1
            }
        }

        self.__pending_requests[request_id] = asyncio.Future()
        await self.__ws.send(json.dumps(payload))
        response = await self.__pending_requests[request_id]
        close_price = float(response["result"][0][4])

        self.__ethusdt_cache[timestamp] = close_price
        return close_price

    async def __listen(self):
        """
        Listens for incoming messages from the WebSocket and processes them.
        """
        while True:
            response = await self.__ws.recv()
            response = json.loads(response)
            request_id = uuid.UUID(response["id"])
            self.__pending_requests[request_id].set_result(response)
            del self.__pending_requests[request_id]
