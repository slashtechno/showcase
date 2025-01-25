from typing import Annotated
from requests import HTTPError
from podium import db
from fastapi import APIRouter, Depends, HTTPException, Path
from pyairtable.formulas import EQ, RECORD_ID
from podium.routers.auth import get_current_user
from podium.db.user import CurrentUser
from podium.db.project import Project

router = APIRouter(prefix="/projects", tags=["projects"])


# Get the current user's projects
@router.get("/mine")
def get_projects(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> list[Project]:
    """
    Get the current user's projects.
    """

    user_id = db.user.get_user_record_id_by_email(current_user.email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")   
            
    projects = [
        Project.model_validate({"id": project["id"], **project["fields"]})
        for project in [
            db.projects.get(project_id)
            for project_id in db.users.get(user_id)["fields"].get("projects", [])
        ]
    ]
    return projects
    

# It's up to the client to provide the event record ID
@router.post("/")
def create_project(
    project: db.ProjectCreationPayload,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    """
    Create a new project. The current user is automatically added as an owner of the project.
    """

    # No matter what email the user provides, the owner is always the current user
    project.owner = [db.user.get_user_record_id_by_email(current_user.email)]

    # Fetch all events that have a record ID matching the project's event ID
    records = db.events.all(formula=EQ(RECORD_ID(), project.event[0]))
    if not records:
        # If the event does not exist, raise a 404
        raise HTTPException(status_code=404, detail="Event not found")

    # If any owner is None, raise a 404
    # if any(owner is None for owner in project.owner):
    #     raise HTTPException(status_code=404, detail="Owner not found")

    # If the owner is not part of the event that the project is going to be associated with, raise a 403
    # Might be good to put a try/except block here to check for a 404 but shouldn't be necessary as the event isn't user-provided, it's in the DB
    event_attendees = db.events.get(project.event[0])["fields"].get("attendees", [])
    if not any(owner in event_attendees for owner in project.owner):
        raise HTTPException(status_code=403, detail="Owner not part of event")

    return db.projects.create(project.model_dump())["fields"]


# Update project
@router.put("/{project_id}")
def update_project(
    project_id: Annotated[str, Path(pattern=r"^rec\w*$")],
    project: db.ProjectUpdate,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    """
    Update an existing project. The current user is automatically added as an owner of the project.
    """

    # No matter what email the user provides, the owner is always the current user
    project.owner = [db.user.get_user_record_id_by_email(current_user.email)]

    return db.projects.update(project_id, project.model_dump())["fields"]


@router.get("/{project_id}")
# The regex here is to ensure that the path parameter starts with "rec" and is followed by any number of alphanumeric characters
def get_project(project_id: Annotated[str, Path(pattern=r"^rec\w*$")]):
    try:
        project = db.projects.get(project_id)
    except HTTPError as e:
        raise (
            HTTPException(status_code=404, detail="Project not found")
            if e.response.status_code == 404
            else e
        )
    return Project.model_validate({id: project["id"], **project["fields"]})
