from podium.constants import RECORD_REGEX
from pydantic import BaseModel, HttpUrl, Field, StringConstraints
from pydantic.json_schema import SkipJsonSchema
from typing import Annotated, List, Optional
from annotated_types import Len


class ProjectBase(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1)]
    readme: HttpUrl
    repo: HttpUrl
    image_url: HttpUrl
    demo: HttpUrl
    description: Optional[str] = None
    owner: Annotated[SkipJsonSchema[List[str]], Field()] = None

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        data["readme"] = str(self.readme)
        data["repo"] = str(self.repo)
        data["image_url"] = str(self.image_url)
        data["demo"] = str(self.demo)
        return data
    
class ProjectUpdate(ProjectBase):
    ...


# https://docs.pydantic.dev/1.10/usage/schema/#field-customization
class ProjectCreationPayload(ProjectBase):
    # https://docs.pydantic.dev/latest/api/types/#pydantic.types.constr--__tabbed_1_2
    event: Annotated[
        List[Annotated[str, StringConstraints(pattern=RECORD_REGEX)]],
        Len(min_length=1, max_length=1),
    ]


class Project(ProjectCreationPayload):
    id: str
    points: int = 0