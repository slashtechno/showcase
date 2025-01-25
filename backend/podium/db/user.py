from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, StringConstraints

from podium.db import tables
from pyairtable.formulas import match


class UserSignupPayload(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    street_1: str
    street_2: Optional[str] = None
    city: str
    state: str
    # str but only allow digits
    zip_code: Annotated[str, StringConstraints(pattern=r"^\d*$")]
    # https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    country: Annotated[str, StringConstraints(pattern=r"^[A-Z]{2}$")]

class CurrentUser(BaseModel):
    email: str
    
# TODO: make this part of CurrentUser or something, since this is used way too much
def get_user_record_id_by_email(email: str) -> Optional[str]:
    users_table = tables["users"]
    # Use formula filtering to search by email
    # try:
    #     formula = match({'Email': email})
    #     records = users_table.all(formula=formula)
    #     return records[0]['id'] if records else None
    # except HTTPError as e:
    #     if '404' in str(e):  # Check specifically for 404 error
    #         return None
    #     raise  # Re-raise other HTTP errors
    formula = match({"email": email})
    records = users_table.all(formula=formula)
    return records[0]["id"] if records else None
