from fastapi import APIRouter, Path
from typing import Annotated, Self, Set
from fastapi import Depends, HTTPException, Query
from pyairtable.formulas import match
from pyairtable.api.types import RecordDict
from secrets import token_urlsafe

from pydantic import BaseModel, Field, model_validator
from pydantic.json_schema import SkipJsonSchema

from requests import HTTPError

# from showcase import db
from showcase.routers.auth import get_current_user
from showcase import db
from showcase.db import Event

router = APIRouter(prefix="/events", tags=["events"])


# Probably should either disable in production or just replace this with /attending
@router.get("/")
def get_events():
    """Get a list of all events"""
    return db.events.all()


@router.get("/attending")
def get_attending_events(current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Get a list of all events that the current user is attending.
    """
    user_id = db.user.get_user_record_id_by_email(current_user["email"])
    attending_events = []
    # TODO: Just check the "owned_events" and "attending_events" fields instead of iterating through all events
    for event in db.events.all():
        if user_id in event["fields"].get("attendees", []) or user_id in event[
            "fields"
        ].get("owner", []):
            attending_events.append(event)

    # TODO: Replace this with Pydantic
    okay_fields = ["name", "description"]
    to_return = [
        {
            "id": event["id"],
            **{field: event["fields"].get(field) for field in okay_fields},
        }
        for event in attending_events
    ]
    return to_return


@router.post("/")
def create_event(
    event: Event, current_user: Annotated[dict, Depends(get_current_user)]
):
    """
    Create a new event. The current user is automatically added as an owner of the event.
    """
    # No matter what email the user provides, the owner is always the current user
    event.owner = [db.user.get_user_record_id_by_email(current_user["email"])]
    # If any owner is None, raise a 404
    if any(owner is None for owner in event.owner):
        raise HTTPException(status_code=404, detail="Owner not found")

    # Generate a join code
    event.join_code = token_urlsafe(8)

    # print(event.model_dump())
    return db.events.create(event.model_dump())


@router.post("/attend")
def attend_event(
    join_code: Annotated[str, Query(description="A unique code used to join an event")],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Attend an event. The client must supply a join code that matches the event's join code.
    """
    # Accomplish this by trying to match the join code against the table and if nothing matches, return a 404
    event = db.events.first(formula=match({"join_code": join_code}))
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    # If the event is found, add the current user to the attendees list
    # But first, ensure that the user is not already in the list
    if db.user.get_user_record_id_by_email(current_user["email"]) in event[
        "fields"
    ].get("attendees", []):
        raise HTTPException(status_code=400, detail="User already attending event")
    db.events.update(
        event["id"],
        {
            "attendees": event["fields"].get("attendees", [])
            + [db.user.get_user_record_id_by_email(current_user["email"])]
        },
    )


# Voting! The client should POST to /events/{event_id}/vote with their top 3 favorite projects, in no particular order. If there are less than 20 projects in the event, only accept the top 2


class Vote(BaseModel):
    # ... signifies that the field is required: https://docs.pydantic.dev/latest/concepts/models/#required-fields
    event_id: str = Field(..., description="The ID of the event to vote in.")
    # Sets prevent duplicates so they're perfect for this use case
    projects: Set[str] = Field(
        ...,
        min_items=2,
        max_items=3,
        title="Nominees",
        description="In no particular order, the top 3 (or 2 if there are less than 20 projects) projects that the user is voting for.",
    )
    event: SkipJsonSchema[RecordDict] = None

    # ~~Putting this in kwargs instead so Swagger doesn't show it~~ shows `"additionalProp1":{}` for some reason
    # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra
    # model_config: SkipJsonSchema[ConfigDict] = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def validate_projects(self) -> Self:
        try:
            self.event = db.events.get(self.event_id)
        except HTTPError as e:
            raise (
                HTTPException(status_code=404, detail="Event not found")
                if e.response.status_code == 404
                else e
            )
        if len(self.projects) < 2:
            raise HTTPException(
                status_code=400, detail="At least 2 projects are required"
            )
        elif len(self.projects) < 3 and len(self.event["fields"]["projects"]) >= 20:
            raise HTTPException(
                status_code=400,
                detail="3 projects are required for events with 20 or more projects",
            )
        elif len(self.projects) > 3:
            raise HTTPException(
                status_code=400, detail="At most 3 projects are allowed"
            )

        # Ensure that the projects exist, they match the event, and the string starts with 'rec'
        for project_id in self.projects:
            try:
                project = db.projects.get(project_id)
            except HTTPError as e:
                raise (
                    HTTPException(status_code=404, detail="Project not found")
                    if e.response.status_code == 404
                    else e
                )
            if project["fields"]["event"][0] != self.event_id:
                raise HTTPException(
                    status_code=400, detail="Project does not belong to event"
                )
        return self


# @router.post("/{event_id}/vote")
@router.post("/vote")
def vote(vote: Vote, current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Vote for the top 3 projects in an event. The client must provide the event ID and a list of the top 3 projects. If there are less than 20 projects in the event, only the top 2 projects are required.
    """

    user = db.users.get(db.user.get_user_record_id_by_email(current_user["email"]))

    if vote.event_id in user["fields"].get("votes", []):
        raise HTTPException(status_code=400, detail="User has already voted in event")

    # Update the votes (increment the `points` field of the nominated projects by 1)
    for project_id in vote.projects:
        try:
            project = db.projects.get(project_id)
            db.projects.update(
                project_id, {"points": project["fields"].get("points", 0) + 1}
            )
        except HTTPError as e:
            raise (
                HTTPException(status_code=404, detail="Project not found")
                if e.response.status_code == 404
                else e
            )

    # Update the user's votes
    db.users.update(
        user["id"],
        {
            "votes": user["fields"].get("votes", []) + [vote.event_id],
        },
    )

    return {"message": "Vote successful"}


@router.get("/{event_id}/leaderboard")
def get_leaderboard(event_id: Annotated[str, Path(title="Event ID")]):
    """
    Get the leaderboard for an event. The leaderboard is a list of projects in the event, sorted by the number of votes they have received.
    """
    event = db.events.get(event_id)
    # projects = [project for project in event["fields"].get("projects", [])]
    projects = []
    for project_id in event["fields"].get("projects", []):
        try:
            project = db.projects.get(project_id)
            projects.append(project)
        except HTTPError as e:
            if e.response.status_code == 404:
                print(f"WARNING: Project {project_id} not found when getting leaderboard for event {event_id}")
            else:
                raise e

    # Sort the projects by the number of votes they have received
    projects.sort(key=lambda project: project["fields"].get("points", 0), reverse=True)

    # Not sure if it's best to return a list of project IDs or the project objects
    # return [project["id"] for project in projects]
    # A dict should work... for now
    return [{"id": project["id"], "name": project["fields"]["name"], "points": project["fields"].get("points", 0)} for project in projects]