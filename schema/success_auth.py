from pydantic import BaseModel
from uuid import UUID

class SuccessAuth(BaseModel):
    login: str
    id: int

