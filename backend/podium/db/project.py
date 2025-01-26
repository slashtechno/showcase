from podium.constants import SingleRecordField, MultiRecordField
from pydantic import BaseModel, HttpUrl, StringConstraints
from typing import Annotated, Optional


class ProjectBase(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1)]
    readme: HttpUrl
    repo: HttpUrl
    image_url: HttpUrl
    demo: HttpUrl
    description: Optional[str] = ""
    # event: Annotated[
    #     List[Annotated[str, StringConstraints(pattern=RECORD_REGEX)]],
    #     Len(min_length=1, max_length=1),
    # ]
    event: SingleRecordField

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        data["readme"] = str(self.readme)
        data["repo"] = str(self.repo)
        data["image_url"] = str(self.image_url)
        data["demo"] = str(self.demo)
        return data
    
class PublicProjectCreationPayload(ProjectBase):
    ...

class ProjectUpdate(ProjectBase):
    ...



class Project(ProjectBase):
    id: str
    points: int = 0
    collaborators: MultiRecordField = []
    owner: SingleRecordField



class PrivateProject(Project):
    join_code: str

