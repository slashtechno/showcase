from showcase import db
from fastapi import APIRouter
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