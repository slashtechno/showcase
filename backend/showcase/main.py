from showcase.db import events

from fastapi import FastAPI
import uvicorn




app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/events")
def get_events():
    return events.all()