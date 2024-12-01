from pydantic import BaseModel
from typing import List, Optional
from pydantic.json_schema import SkipJsonSchema


# https://docs.pydantic.dev/1.10/usage/schema/#field-customization
class Event(BaseModel):
    name: str
    description: Optional[str] = None

    # Owner is inferred from the current user (token)
    # https://github.com/fastapi/fastapi/discussions/7585#discussioncomment-7573510
    # https://github.com/fastapi/fastapi/discussions/7585#discussioncomment-8950914
    # _owner: Optional[List[str]] = None
    owner: SkipJsonSchema[str | List[str]] = None
    join_code: SkipJsonSchema[str] = None