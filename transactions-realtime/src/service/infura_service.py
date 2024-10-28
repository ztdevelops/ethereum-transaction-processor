import asyncio

from hexbytes import HexBytes
from service.binance_service import BinanceService
from service.broker_service import BrokerService
from service.etherscan_service import EtherscanService
from utils.config import Config
from utils.eth_util import EthUtil
from web3 import AsyncWeb3
from web3.datastructures import AttributeDict
from web3.providers import WebSocketProvider

config = Config()


class InfuraService:
    """
    A service class to interact with the Infura Web3 provider using websockets.

    Attributes:
        INFURA_URL (str): The base URL for the Infura Web3 provider.
        __async_web3 (AsyncWeb3): An instance of AsyncWeb3 connected to the Infura provider.
        __etherscan_service (EtherscanService): Service for interacting with the Etherscan API.
        __broker_service (BrokerService): Service for sending messages to a broker.
        __contract_address (str): The address of the contract to listen for events.
        __contract_abi_address (str): The address to fetch the contract ABI from.
        __infura_project_id (str): The API key for authenticating requests to the Infura API.
    """

    INFURA_URL = "wss://mainnet.infura.io/ws/v3"
    __async_web3 = None
    __etherscan_service = None
    __broker_service = None
    __binance_service = None
    __contract_address = None
    __contract_abi_address = None
    __infura_project_id = None

    def __init__(self,
                 etherscan_service: EtherscanService,
                 broker_service: BrokerService,
                 binance_service: BinanceService,
                 infura_project_id: str,
                 contract_address: str = None,
                 contract_abi_address: str = None,
                 poll_interval: int = None
                 ):
        """
        Initialize the InfuraService with the given API key.

        Args:
            etherscan_service (EtherscanService): An instance of the EtherscanService.
            broker_service (BrokerService): An instance of the BrokerService.
            binance_service (BinanceService): An instance of the BinanceService.
            infura_project_id (str): The API key for authenticating requests to the Infura API.
            contract_address (str, optional): The address of the contract to listen for events. Defaults to None.
            contract_abi_address (str, optional): The address to fetch the contract ABI from. Defaults to None.
            poll_interval (int, optional): The interval in seconds to poll for new events. Defaults to None.
        """
        self.__etherscan_service = etherscan_service
        self.__broker_service = broker_service
        self.__binance_service = binance_service
        self.__infura_project_id = infura_project_id
        self.__poll_interval = poll_interval

        if contract_address is None:
            self.__contract_address = config.get("ETHERSCAN_CONTRACT_ADDRESS")
        else:
            self.__contract_address = contract_address

        if contract_abi_address is None:
            self.__contract_abi_address = config.get("ETHERSCAN_CONTRACT_ABI_ADDRESS")
        else:
            self.__contract_abi_address = contract_abi_address

        if poll_interval is None:
            self.__poll_interval = int(config.get("INFURA_POLL_INTERVAL"))
        else:
            self.__poll_interval = poll_interval

    async def __ws_connect(self):
        """
        Connect to the Infura Web3 provider with websockets.

        Returns:
            AsyncWeb3: A Web3 instance connected to the Infura provider.
        """
        if self.__async_web3:
            return

        web3_provider_url = self.__create_web3_provider_url()
        async_web3 = AsyncWeb3(WebSocketProvider(web3_provider_url))
        await async_web3.provider.connect()
        self.__async_web3 = async_web3

    def __create_web3_provider_url(self):
        """
        Create the URL for the Infura Web3 provider.

        Returns:
            str: The URL for the Infura Web3 provider.
        """
        return f"{self.INFURA_URL}/{self.__infura_project_id}"

    async def __listen_for_swaps(self, address: str, contract_abi: list):
        """
        Listen for swap events on the given address.

        Args:
            address (str): The address to listen for swap events.
            contract_abi (list): The ABI of the contract to listen for swap events.
        """
        contract = self.__async_web3.eth.contract(address=address, abi=contract_abi)
        swap_event_filter = await contract.events.Swap.create_filter(from_block='latest')

        while True:
            try:
                new_events = await swap_event_filter.get_new_entries()
                print(f"Received {len(new_events)} new events")
                for event in new_events:
                    processed_transaction = await self.__process_transaction(event)
                    print(f"Writing to broker: {processed_transaction}")
                    self.__broker_service.send("", "transactions", processed_transaction)
                self.__broker_service.flush()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                await asyncio.sleep(self.__poll_interval)

    async def listen(self):
        """
        Start listening for swap events on the contract address.

        Fetches the contract ABI from the Etherscan service and starts the event listener.
        """
        await self.__ws_connect()

        contract_abi_response = self.__etherscan_service.get_contract_abi(self.__contract_abi_address)
        if contract_abi_response is None:
            print("Failed to retrieve contract ABI, aborting async listening...")
            return

        contract_abi = contract_abi_response.get("result")
        await self.__listen_for_swaps(
            address=self.__contract_address,
            contract_abi=contract_abi,
        )

    async def __process_transaction(self, event):
        """
        Process the transaction data from the event.
        """
        if isinstance(event, AttributeDict):
            event = self.__convert_to_dict(event)

        transaction_hash = event.get("transactionHash")
        transaction = await self.__async_web3.eth.get_transaction(transaction_hash)

        gas_used = transaction.get("gas")
        gas_price = transaction.get("gasPrice")
        eth_spent = EthUtil.gas_to_eth(gas_used, gas_price)

        block_number = transaction.get("blockNumber")
        block = await self.__async_web3.eth.get_block(block_number)

        timestamp = block.get("timestamp")
        ethusdt_close_price = await self.__binance_service.get_ethusdt_price(timestamp)
        eth_spent_usdt = eth_spent * ethusdt_close_price

        return {
            "ethusdt_close_price": ethusdt_close_price,
            "transaction_fee_in_eth": eth_spent,
            "transaction_fee_in_usdt": eth_spent_usdt,
            "timestamp": timestamp,
            "transaction_hash": transaction_hash,
        }

    def __convert_to_dict(self, attr_dict):
        """
        Recursively converts AttributeDict and HexBytes objects to regular Python dictionaries and strings.

        Args:
            attr_dict (AttributeDict or list or HexBytes): The object to convert.

        Returns:
            dict or list or str: The converted object.
        """
        if isinstance(attr_dict, AttributeDict):
            return {k: self.__convert_to_dict(v) for k, v in attr_dict.items()}
        elif isinstance(attr_dict, list):
            return [self.__convert_to_dict(i) for i in attr_dict]
        elif isinstance(attr_dict, HexBytes):
            return attr_dict.hex()
        return attr_dict
