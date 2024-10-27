from pydantic import BaseModel


class HistoricalTransactionRequest(BaseModel):
    start_block: str
    end_block: str
    page: int
    offset: int