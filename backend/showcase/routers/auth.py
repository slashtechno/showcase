from datetime import datetime, timedelta, timezone
# import smtplib
# from email.mime.text import MIMEText
from typing import Annotated

from showcase import settings

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from jwt.exceptions import PyJWTError

router = APIRouter(tags=["auth"])

SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_expire_minutes
MAGIC_LINK_EXPIRE_MINUTES = 15


DEBUG_EMAIL = "angad+debug@hackclub.com"


class User(BaseModel):
    email: str


def create_access_token(
    data: dict, expires_delta: timedelta | None = None, token_type: str = "access"
):
    to_encode = data.copy()

    # Set the token type. Otherwise, a magic link could be used as an access token. Probably not the end of the world, but would mess with stuff like 2FA
    # Potentially, a version could be set that once incremented would invalidate all old tokens
    to_encode.update({"token_type": token_type})
    # Set the expirationt ime
    # Not sure if this needs to be UTC, but why not?
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=MAGIC_LINK_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def send_magic_link(email: str):
    token_data = {"sub": email}
    token = create_access_token(
        data=token_data, expires_delta=timedelta(minutes=15), token_type="magic_link"
    )

    # magic_link = f"http://localhost:8000/verify?token={token}"
    # from_email = "showcase@showcase"
    # msg = MIMEText(
    #     f"Click the link to verify: {magic_link}\nIt will expire in 15 minutes."
    # )
    # msg["Subject"] = "Login to Showcase"
    # msg["From"] = from_email
    # msg["To"] = email
    # python -m aiosmtpd -n -l localhost:1025
    # with smtplib.SMTP("localhost", 1025) as server:
    #     server.sendmail(from_email, email, msg.as_string())

    print(f"Token for {email}: {token} | magic_link: http://localhost:5173/login?token={token}")


@router.post("/request-login")
async def request_login(user: User):
    await send_magic_link(user.email)
    # The message is probably unnecessary since there will be a nice frontend for this eventually
    return {"message": "Magic link sent to your email"}


@router.get("/verify")
async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("token_type")
        # Check if the token is a magic link, otherwise it's invalid
        # Otherwise a JWT that's about to expire might be used as an access token
        if email is None or token_type != "magic_link":
            raise HTTPException(status_code=400, detail="Invalid token")
    except PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )
    return {"access_token": access_token, "token_type": "bearer"}


security = HTTPBearer()


# This serves two purposes: it checks if the token is valid and returns the user's email
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
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


@router.get("/protected-route")
async def protected_route(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"email": current_user["email"]}


if __name__ == "__main__":
    # create a dev JWT
    debug_token = create_access_token(
        data={"sub": DEBUG_EMAIL},
        expires_delta=timedelta(days=365),  # Token valid for 1 year
        token_type="access",
    )
    print(debug_token)
