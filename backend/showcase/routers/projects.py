from typing import Annotated
from showcase import db
from fastapi import APIRouter, Depends, HTTPException, Path
from pyairtable.formulas import EQ, RECORD_ID
from showcase.routers.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


# TODO: Only get projects if they are in an event that the user is attending
@router.get("/")
def get_projects():
    return db.projects.all()


# It's up to the client to provide the event record ID
@router.post("/")
def create_project(project: db.Project, current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Create a new project. The current user is automatically added as an owner of the project.
    """

    # No matter what email the user provides, the owner is always the current user
    project.owner = [db.user.get_user_record_id_by_email(current_user["email"])]

    if project.event is str:
        project.event = [project.event]

    # If the event does not exist, raise a 404
    records = db.events.all(formula=EQ(RECORD_ID(), project.event[0]))
    if not records:
        raise HTTPException(status_code=404, detail="Event not found")

    # If any owner is None, raise a 404
    if any(owner is None for owner in project.owner):
        raise HTTPException(status_code=404, detail="Owner not found")

    # If the owner is not part of the event that the project is going to be associated with, raise a 403
    # Might be good to put a try/except block here to check for a 404 but shouldn't be necessary as the event isn't user-provided, it's in the DB
    event_attendees = db.events.get(project.event[0])["fields"].get("attendees", [])
    if not any(owner in event_attendees for owner in project.owner):
        raise HTTPException(status_code=403, detail="Owner not part of event")


    return db.projects.create(project.model_dump())["fields"]

@router.get("/{project_id}")
# The regex here is to ensure that the path parameter starts with "rec" and is followed by any number of alphanumeric characters
def get_project(project_id: Annotated[str, Path(pattern="^rec\w*$")]):
    project = db.projects.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    okay_fields = ["name", "readme", "repo", "description", "event"]
    return {field: project["fields"].get(field) for field in okay_fields}