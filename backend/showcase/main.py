from showcase.db import events, Event
from showcase import db

from fastapi import FastAPI, HTTPException, status
import uvicorn

# Stuff for authentication
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated
from pydantic import BaseModel

app = FastAPI()


# https://fastapi.tiangolo.com/tutorial/security/get-current-user/#create-a-user-model
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def fake_hash_password(password: str):
    return "fakehashed" + password


# token is a relative path
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = None
# UserInDB is a subclass of User, but with the hashed_password field as well
class UserInDB(User):
    hashed_password: str

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if user_dict is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Unpack the user_dict into a User object
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "access_token": user.username, "token_type": "bearer"
    }


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


# --- Showcase API --- #

# @app.get("/events")
# def get_events():
#     return events.all()

# @app.post("/events")
# def create_event(event: Event):
#     event.owner = [db.user.get_user_record_id_by_email(event.owner)]
#     if event.owner is None:
#         raise HTTPException(status_code=404, detail="Owner not found")
#     print(event.model_dump())
#     return events.create(event.model_dump(
#     ))


# Start the server if this file is run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
