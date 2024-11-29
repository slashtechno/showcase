from pydantic import BaseModel
from typing import List, Optional, Union


class Event(BaseModel):
    name: str
    description: Optional[str] = None
    # Owner is inferred from the current user (token)
    # owner: Optional[List[str]] = None
    owner: Optional[Union[str, List[str]]] = None