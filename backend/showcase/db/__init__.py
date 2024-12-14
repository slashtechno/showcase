from showcase.db.db import tables
from showcase.db.event import ComplexEvent as ComplexEvent
from showcase.db.event import EventCreationPayload as EventCreationPayload
from showcase.db.event import UserEvents as UserEvents
from showcase.db.event import Event as Event
from showcase.db import user as user
from showcase.db.project import Project as Project

events = tables["events"]
users = tables["users"]
projects = tables["projects"]
