import requests

from src.app.dto.request.historical_transaction_request import HistoricalTransactionRequest
from src.app.utils.rest_util import RestUtil

class EtherscanService:
    ETHERSCAN_API_BASE_URL = "https://api.etherscan.io/api"
    __etherscan_api_key = None

    def __init__(self, api_key: str):
        """
        Initialize the EtherscanService with the given base URL and API key.

        Args:
            api_key (str): The API key for authenticating requests to the Etherscan API.
        """
        self.__etherscan_api_key = api_key

    def get_contract_abi(self, address: str):
        """
        Retrieve the ABI for a given contract address.

        Args:
            address (str): The address of the contract.

        Returns:
            dict or None: The JSON response from the Etherscan API if the request is successful, otherwise None.
        """
        params = {
            "module": "contract",
            "action": "getabi",
            "address": address,
            "apikey": self.__etherscan_api_key
        }

        return RestUtil.get(self.ETHERSCAN_API_BASE_URL, params=params)

    def get_historical_transactions(self, historical_transaction_request: HistoricalTransactionRequest):
        """
        Retrieve historical token transactions for a given address.

        Args:
            historical_transaction_request (HistoricalTransactionRequest): The request object containing parameters for the query.

        Returns:
            dict or None: The JSON response from the Etherscan API if the request is successful, otherwise None.
        """
        params = {
            "module": "account",
            "action": "tokentx",
            "address": "0x4e83362442b8d1bec281594cea3050c8eb01311c", # to change
            "startblock": historical_transaction_request.start_block,
            "endblock": historical_transaction_request.end_block,
            "page": historical_transaction_request.page,
            "offset": historical_transaction_request.offset,
            "sort": "asc",
            "apikey": self.__etherscan_api_key,
        }

        return RestUtil.get(self.ETHERSCAN_API_BASE_URL, params=params)

