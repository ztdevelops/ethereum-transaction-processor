from dto.historical_transaction_request_dto import HistoricalTransactionRequestDTO
from service.broker_service import BrokerService
from service.etherscan_service import EtherscanService
from utils.config import Config

config = Config()


class BatchService:
    """
    Service for processing historical Ethereum transactions in batches.

    Attributes:
        __etherscan_service (EtherscanService): Service for interacting with Etherscan API.
        __broker_service (BrokerService): Service for sending messages to a broker.
        __first_block (int): The first block number to start processing from.
        __last_block (int): The last block number to process up to.
        __batch_size (int): The number of blocks to process in each batch.
    """
    __etherscan_service = None
    __broker_service = None
    __first_block = None
    __last_block = None
    __batch_size = None

    def __init__(self,
                 etherscan_service: EtherscanService,
                 broker_service: BrokerService,
                 first_block: int = None,
                 last_block: int = None,
                 batch_size: int = None,
                 ):
        """
        Initializes the BatchService with the given EtherscanService and BrokerService.

        Args:
            etherscan_service (EtherscanService): An instance of the EtherscanService.
            broker_service (BrokerService): An instance of the BrokerService.
            first_block (int, optional): The first block number to start processing from. Defaults to None.
            last_block (int, optional): The last block number to process up to. Defaults to None.
            batch_size (int, optional): The number of blocks to process in each batch. Defaults to None.
        """
        self.__etherscan_service = etherscan_service
        self.__broker_service = broker_service

        if first_block is None:
            self.__first_block = int(config.get("ETHERSCAN_HISTORICAL_FIRST_BLOCK"))
        else:
            self.__first_block = first_block

        if last_block is None:
            self.__last_block = int(config.get("ETHERSCAN_HISTORICAL_LAST_BLOCK"))
        else:
            self.__last_block = last_block

        if batch_size is None:
            self.__batch_size = int(config.get("ETHERSCAN_HISTORICAL_BATCH_SIZE"))
        else:
            self.__batch_size = batch_size

    async def start(self):
        """
        Processes historical Ethereum transactions in batches.
        """
        print(
            f"Processing historical Ethereum transactions from block {self.__first_block} to block {self.__last_block} in batches of {self.__batch_size} blocks.")

        start_block = self.__first_block
        end_block = self.__first_block + self.__batch_size

        while start_block < self.__last_block:
            batch_request = HistoricalTransactionRequestDTO(
                address=config.get("ETHERSCAN_CONTRACT_ADDRESS"),
                start_block=start_block,
                end_block=end_block,
                page=1,
                offset=self.__batch_size
            )

            self.__handle_batch(batch_request)

            start_block = end_block
            end_block = min(start_block + self.__batch_size, self.__last_block)

    def __handle_batch(self, batch_request: HistoricalTransactionRequestDTO):
        """
        Handles a batch of historical Ethereum transactions.

        Args:
            batch_request (HistoricalTransactionRequestDTO): The request DTO for fetching a batch of historical Ethereum transactions.
        """
        historical_data = self.__etherscan_service.get_historical_data(batch_request)
        print(
            f"Found {len(historical_data.get('result'))} transactions in block range {batch_request.start_block} to {batch_request.end_block}.")

        for transaction in historical_data.get("result"):
            self.__broker_service.send("", "history", transaction)
        self.__broker_service.flush()