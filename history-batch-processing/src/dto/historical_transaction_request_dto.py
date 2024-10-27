class HistoricalTransactionRequestDTO:
    """
    Data Transfer Object (DTO) for historical transaction requests.

    Attributes:
        address (str): The contract address for the transaction.
        start_block (int): The starting block number for the transaction history.
        end_block (int): The ending block number for the transaction history.
        page (int): The page number for paginated results.
        offset (int): The number of transactions to skip for pagination.
    """

    def __init__(self, address: str, start_block: int, end_block: int, page: int, offset: int):
        """
        Initializes a new instance of the HistoricalTransactionRequestDTO class.

        Args:
            address (str): The contract address for the transaction.
            start_block (int): The starting block number for the transaction history.
            end_block (int): The ending block number for the transaction history.
            page (int): The page number for paginated results.
            offset (int): The number of transactions to skip for pagination.
        """
        self.address = address
        self.start_block = start_block
        self.end_block = end_block
        self.page = page
        self.offset = offset