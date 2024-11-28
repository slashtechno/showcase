from pydantic import BaseModel
from typing import Optional


class Event(BaseModel):
    name: str
    description: Optional[str] = None
    owner = Optional[str] = "nevertrusttheclient@example.com"
    