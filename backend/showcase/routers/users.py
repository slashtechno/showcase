from typing import Annotated
from pydantic import BaseModel, EmailStr
from showcase import db
from fastapi import APIRouter, Query
from showcase.db.user import UserSignupPayload

router = APIRouter(prefix="/users", tags=["users"])


# DISABLE THIS IN PRODUCTION
# @router.get("/")
# def get_users():
#     return db.users.all()


# Eventually, this should probably be rate-limited
@router.post("/")
def create_user(user: UserSignupPayload): 
    db.users.create(user.model_dump())

class UserExistsResponse(BaseModel):
    exists: bool

@router.get("/exists")
def user_exists(email: Annotated[EmailStr, Query(...)]) -> UserExistsResponse:
    exists = True if db.user.get_user_record_id_by_email(email) else False
    return UserExistsResponse(exists=exists)