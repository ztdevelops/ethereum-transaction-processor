from pydantic import BaseModel


class BaseDTO(BaseModel):
    """
    Base Data Transfer Object (DTO) class.

    This class serves as a base for all DTOs in the application,
    inheriting from Pydantic's BaseModel to provide data validation and serialization.
    """
    pass
