from pydantic import BaseModel


class HealthcheckResponseDTO(BaseModel):
    healthy: bool