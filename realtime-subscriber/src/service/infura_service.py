import asyncio

from service.broker_service import BrokerService
from service.etherscan_service import EtherscanService
from utils.config import Config
from web3 import AsyncWeb3
from web3.providers import WebSocketProvider

config = Config()


class InfuraService:
    """
    A service class to interact with the Infura Web3 provider using websockets.
    """

    INFURA_URL = "wss://mainnet.infura.io/ws/v3"
    __etherscan_service = None
    __broker_service = None

    async_web3 = None
    __contract_address = None
    __contract_abi_address = None
    __infura_project_id = None

    def __init__(self,
                 etherscan_service: EtherscanService,
                 broker_service: BrokerService,
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
            infura_project_id (str): The API key for authenticating requests to the Infura API.
            contract_address (str, optional): The address of the contract to listen for events. Defaults to None.
            contract_abi_address (str, optional): The address to fetch the contract ABI from. Defaults to None.
        """
        self.__etherscan_service = etherscan_service
        self.__broker_service = broker_service
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
        web3_provider_url = self.__create_web3_provider_url()
        async_web3 = AsyncWeb3(WebSocketProvider(web3_provider_url))
        await async_web3.provider.connect()
        return async_web3

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
        contract = self.async_web3.eth.contract(address=address, abi=contract_abi)
        swap_event_filter = await contract.events.Swap.create_filter(from_block='latest')

        while True:
            try:
                new_events = await swap_event_filter.get_new_entries()
                print(f"Received {len(new_events)} new events")
                for event in new_events:
                    self.__broker_service.send("transaction_message", "transactions", event)
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
        self.async_web3 = await self.__ws_connect()

        contract_abi_response = self.__etherscan_service.get_contract_abi(self.__contract_abi_address)
        if contract_abi_response is None:
            print("Failed to retrieve contract ABI, aborting async listening...")
            return

        contract_abi = contract_abi_response.get("result")
        await self.__listen_for_swaps(
            address=self.__contract_address,
            contract_abi=contract_abi,
        )
