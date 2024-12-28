from typing import Optional
from pydantic import BaseModel, EmailStr

from showcase.db import tables
from pyairtable.formulas import match


class UserSignupPayload(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    # Might eventually add validation for mailing address, although it's not necessary for the MVP
    mailing_address: str


# It may help to create a lookup field later, although this works fine for now
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
