from pydantic import BaseModel, Field
from typing import Annotated, List, Optional
from pydantic.json_schema import SkipJsonSchema


# https://docs.pydantic.dev/1.10/usage/schema/#field-customization
class EventCreationPayload(BaseModel):
    name: str
    description: Optional[str] = None

    # Owner is inferred from the current user (token)
    # https://github.com/fastapi/fastapi/discussions/7585#discussioncomment-7573510
    # https://github.com/fastapi/fastapi/discussions/7585#discussioncomment-8950914
    # _owner: Optional[List[str]] = None
    owner: SkipJsonSchema[str | List[str]] = None
    join_code: SkipJsonSchema[str] = None

class Event(EventCreationPayload):
    id: str

# Maybe rename to FullEvent? In the frontend it's OwnedEvent since that's the only time a normal user should see all event information (if they own it)
class ComplexEvent(Event):
    # https://stackoverflow.com/questions/63793662/how-to-give-a-pydantic-list-field-a-default-value/63808835#63808835
    # List of record IDs, since that's what Airtable uses
    attendees: Annotated[List[str], Field(default_factory=list)]

class UserEvents(BaseModel):
    """Return information regarding what the events the user owns and what events they are attending. If they are only attending an event, don't return sensitive information like participants."""
    owned_events: List[ComplexEvent]
    attending_events: List[EventCreationPayload]
