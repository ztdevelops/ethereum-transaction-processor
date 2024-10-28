from utils.rest_util import RestUtil


class EtherscanService:
    """
    Service for interacting with the Etherscan API to retrieve contract ABI.

    Attributes:
        ETHERSCAN_API_BASE_URL (str): The base URL for the Etherscan API.
        __etherscan_api_key (str): The API key for authenticating requests to the Etherscan API.
    """
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