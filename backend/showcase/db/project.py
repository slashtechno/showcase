from pydantic import BaseModel, HttpUrl, Field
from pydantic.json_schema import SkipJsonSchema
from typing import Annotated, List, Optional

# https://docs.pydantic.dev/1.10/usage/schema/#field-customization
class Project(BaseModel):
    name: str
    readme: HttpUrl
    repo: HttpUrl
    description: Optional[str] = None
    
    owner: Annotated[SkipJsonSchema[str | List[str]], Field(frozen=False, exclude=True)] = None
    event: List[str] | str 
    # join_code: SkipJsonSchema[str] = None

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        data['readme'] = str(self.readme)
        data['repo'] = str(self.repo)
        return data