from typing import List, Optional

from dto.get_transaction_response_dto import GetTransactionResponseDTO
from pydantic import BaseModel


class GetTransactionsResponseDTO(BaseModel):
    """
    Data Transfer Object (DTO) for the response of multiple transaction retrievals.

    Attributes:
        transactions (List[GetTransactionResponseDTO]): A list of transaction response DTOs.
        page_size (int): The number of transactions per page.
        next_page (Optional[int]): The page number for the next set of transactions, if available.
    """
    transactions: List[GetTransactionResponseDTO]
    page_size: int
    next_page: Optional[int]
