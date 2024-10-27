class HistoricalTransactionRequestDTO:
    def __init__(self, address: str, start_block: int, end_block: int, page: int, offset: int):
        self.address = address
        self.start_block = start_block
        self.end_block = end_block
        self.page = page
        self.offset = offset
