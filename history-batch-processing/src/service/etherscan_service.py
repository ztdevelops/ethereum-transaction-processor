from dto.historical_transaction_request_dto import HistoricalTransactionRequestDTO
from utils.rest_util import RestUtil


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

    def get_historical_data(self, request: HistoricalTransactionRequestDTO):
        """
        Retrieve historical Ethereum transactions within the given block range.

        Args:
            request (HistoricalTransactionRequestDTO): The request object containing the block range.

        Returns:
            dict or None: The JSON response from the Etherscan API if the request is successful, otherwise None.
        """

        params = {
            "module": "account",
            "action": "tokentx",
            "contractaddress": request.address,
            "page": request.page,
            "offset": request.offset,
            "startblock": request.start_block,
            "endblock": request.end_block,
            "sort": "asc",
            "apikey": self.__etherscan_api_key
        }

        return RestUtil.get(self.ETHERSCAN_API_BASE_URL, params=params)
