from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends, HTTPException, Query
from pyairtable.formulas import match
from secrets import token_urlsafe

# from showcase import db
from showcase.routers.auth import get_current_user
from showcase import db
from showcase.db import Event, events

router = APIRouter(prefix="/events")


@router.get("/")
def get_events():
    """Get a list of all events"""
    return events.all()


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
    return events.create(event.model_dump())


@router.post("/attend")
def attend_event(
    join_code: Annotated[str, Query(description="A unique code used to join an event")],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Attend an event. The client must supply a join code that matches the event's join code.
    """
    # Accomplish this by trying to match the join code against the table and if nothing matches, return a 404
    event = events.first(formula=match({"join_code": join_code}))
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    # If the event is found, add the current user to the attendees list
    # But first, ensure that the user is not already in the list
    if db.user.get_user_record_id_by_email(current_user["email"]) in event[
        "fields"
    ].get("attendees", []):
        raise HTTPException(status_code=400, detail="User already attending event")
    events.update(
        event["id"],
        {
            "attendees": event["fields"].get("attendees", [])
            + [db.user.get_user_record_id_by_email(current_user["email"])]
        },
    )
