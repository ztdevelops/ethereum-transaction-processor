from pydantic import BaseModel


class GetTransactionResponseDTO(BaseModel):
    """
    Data Transfer Object (DTO) for the response of a transaction retrieval.

    Attributes:
        transaction_hash (str): The hash of the transaction.
        ethusdt_close_price (float): The closing price of ETH/USDT at the time of the transaction.
        timestamp (int): The timestamp of the transaction.
        transaction_fee_in_eth (float): The transaction fee in ETH.
        transaction_fee_in_usdt (float): The transaction fee in USDT.
    """
    transaction_hash: str
    ethusdt_close_price: float
    timestamp: int
    transaction_fee_in_eth: float
    transaction_fee_in_usdt: float
