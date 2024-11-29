from datetime import datetime, timedelta, timezone
import smtplib
from email.mime.text import MIMEText
from typing import Annotated

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from showcase.db import events, Event
from showcase import db

from fastapi import FastAPI, HTTPException, status, Depends
import uvicorn

# Magic link authentication
from pydantic import BaseModel
import jwt
from jwt.exceptions import PyJWTError

app = FastAPI()


# TODO: Store this stuff in .secrets and settings.toml
SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: str

# Create a JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None, token_type: str = "access"):
    to_encode = data.copy()
    to_encode.update({"token_type": token_type})
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Send a JWT via email. This JWT is only valid for 15 minutes and only serves to verify the user's email.
async def send_magic_link(email: str):
    token_data = {"sub": email}
    token = create_access_token(data=token_data, expires_delta=timedelta(minutes=15), token_type="magic_link")
    magic_link = f"http://localhost:8000/verify?token={token}"
    
    from_email = "showcase@showcase"
    msg = MIMEText(f"Click the link to verify: {magic_link}\nIt will expire in 15 minutes.")
    msg["Subject"] = "Login to Showcase"
    msg["From"] = from_email
    msg["To"] = email

    with smtplib.SMTP("localhost", 1025) as server:
        server.sendmail(from_email, email, msg.as_string())

# Initiate the login process
@app.post("/request-login")
async def request_login(user: User):
    await send_magic_link(user.email)
    return {"message": "Magic link sent to your email"}


@app.get("/verify")
async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("token_type")
        if email is None or token_type != "magic_link":
            raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    access_token = create_access_token(
        data={"sub": email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), token_type="access"
    )
    return {"access_token": access_token, "token_type": "bearer"}

security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("token_type")
        if email is None or token_type != "access":
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return {"email": email}

@app.get("/protected-route")
async def protected_route(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"message": f"Hello, {current_user['email']}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
