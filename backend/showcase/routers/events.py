from fastapi import APIRouter, Path
from typing import Annotated, Self, Set, Union, List
from fastapi import Depends, HTTPException, Query
from pyairtable.formulas import match
from pyairtable.api.types import RecordDict
from secrets import token_urlsafe

from pydantic import BaseModel, Field, model_validator
from pydantic.json_schema import SkipJsonSchema

from requests import HTTPError

from showcase.routers.auth import get_current_user
from showcase import db
from showcase.db import EventCreationPayload, ComplexEvent, UserEvents, Event
from showcase.db.project import Project

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/{event_id}")
def get_event(
    event_id: Annotated[str, Path(title="Event ID")],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Union[ComplexEvent, Event]:
    """
    Get an event by its ID. If the user owns it, return a complex event. Otherwise, return a regular event.
    """

    user_id = db.user.get_user_record_id_by_email(current_user["email"])
    if user_id is None:
        raise HTTPException(status_code=500, detail="User not found")
    
    user = db.users.get(user_id)
    event = db.events.get(event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    if user["id"] in event["fields"].get("owner", []):
        return ComplexEvent.model_validate({"id": event["id"], **event["fields"]})
    elif user["id"] in event["fields"].get("attendees", []):
        return Event.model_validate({"id": event["id"], **event["fields"]})
    else:
        raise HTTPException(status_code=403, detail="User does not have access to event")

# Used to be /attending
@router.get("/")
def get_attending_events(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> UserEvents:
    """
    Get a list of all events that the current user is attending.
    """
    user_id = db.user.get_user_record_id_by_email(current_user["email"])
    if user_id is None:
        raise HTTPException(status_code=500, detail="User not found")
    user = db.users.get(user_id)


    # Eventually it might be better to return a user object. Otherwise, the client that the event owner is using would need to fetch the user. Since user emails probably shouldn't be public with just a record ID as a parameter, we would need to check if the person calling GET /users?user=ID has an event wherein that user ID is present. To avoid all this, the user object could be returned.
    owned_events = [
        ComplexEvent.model_validate({"id": event["id"], **event["fields"]})
        for event in [
            db.events.get(event_id)
            for event_id in user["fields"].get("owned_events", [])
        ]
    ]
    attending_events = [
        Event.model_validate({"id": event["id"], **event["fields"]})
        for event in [
            db.events.get(event_id)
            for event_id in db.users.get(user_id)["fields"].get("attending_events", [])
        ]
    ]


    return UserEvents(owned_events=owned_events, attending_events=attending_events)


@router.post("/")
def create_event(
    event: EventCreationPayload, current_user: Annotated[dict, Depends(get_current_user)]
):
    """
    Create a new event. The current user is automatically added as an owner of the event.
    """
    # No matter what email the user provides, the owner is always the current user
    event.owner = [db.user.get_user_record_id_by_email(current_user["email"])]
    # If the owner is not found, return a 404. Since there might eventually be multiple owners, just check if any of them are None
    if None in event.owner:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a unique join code by continuously generating a new one until it doesn't match any existing join codes
    while True:
        join_code = token_urlsafe(8)
        if not db.events.first(formula=match({"join_code": join_code})):
            event.join_code = join_code
            break

    db.events.create(event.model_dump())


    # The issue with the approach below was that ComplexEvent requires an ID, which isn't available until the event is created. It might be better to just do it and reoplace model_validate with model_construct to prevent validation errors
    # return db.events.create(
    #     ComplexEvent.model_validate(
    #         {
    #             # Use information the user provided
    #             **event.model_dump(),
    #             # Add the owner and join code
    #             "owner": owner,
    #             "join_code": join_code,
    #         }
    #     ).model_dump(
    #         exclude_unset=True
    #     )  
    # )


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
        if len(self.projects) < 3 and len(self.event["fields"]["projects"]) >= 20:
            raise HTTPException(
                status_code=400,
                detail="3 projects are required for events with 20 or more projects",
            )
        elif len(self.projects) > 2 and len(self.event["fields"]["projects"]) < 20:
            raise HTTPException(
                status_code=400,
                detail="Only 2 projects are allowed for events with less than 20 projects",
            )
        if len(self.projects) > 3:
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
                print(
                    f"WARNING: Project {project_id} not found when getting leaderboard for event {event_id}"
                )
            else:
                raise e

    # Sort the projects by the number of votes they have received
    projects.sort(key=lambda project: project["fields"].get("points", 0), reverse=True)
    
    projects = [Project.model_validate({"id": project["id"], **project["fields"]}) for project in projects]
    return projects

@router.get("/{event_id}/projects")
def get_event_projects(event_id: Annotated[str, Path(title="Event ID")]) -> List[Project]:
    """
    Get the projects for a specific event.
    """
    try: 
        event = db.events.get(event_id)
    except HTTPError as e:
        raise (
            HTTPException(status_code=404, detail="Event not found")
            if e.response.status_code == 404
            else e
        )

    projects = [Project.model_validate({"id": project["id"], **project["fields"]}) for project in [db.projects.get(project_id) for project_id in event["fields"].get("projects", [])]]
    return projects