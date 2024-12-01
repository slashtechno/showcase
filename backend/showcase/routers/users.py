from showcase import db
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


# DISABLE THIS IN PRODUCTION
@router.get("/")
def get_users():
    return db.users.all()
