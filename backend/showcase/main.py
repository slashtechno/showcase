from showcase.db import events, Event
from showcase import db


from fastapi import FastAPI, HTTPException
import uvicorn




app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/events")
def get_events():
    return events.all()

@app.post("/events")
def create_event(event: Event):
    event.owner = [db.user.get_user_record_id_by_email(event.owner)]
    if event.owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    print(event.model_dump())
    return events.create(event.model_dump(
    ))