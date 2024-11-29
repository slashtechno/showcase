from typing import Annotated
import uvicorn
from fastapi import Depends, FastAPI, HTTPException


# from showcase import db
from showcase.auth import get_current_user, router as auth_router
from showcase import db
from showcase.db import Event, events

app = FastAPI()

@app.get("/events")
def get_events():
    return events.all()

@app.post("/events")
def create_event(event: Event, current_user: Annotated[dict, Depends(get_current_user)]):
    # No matter what email the user provides, the owner is always the current user
    event.owner = [db.user.get_user_record_id_by_email(current_user['email'])]
    # If any owner is None, raise a 404
    if any(owner is None for owner in event.owner):
        raise HTTPException(status_code=404, detail="Owner not found")
    print(event.model_dump())
    return events.create(event.model_dump(
    ))


app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
