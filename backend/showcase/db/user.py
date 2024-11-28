from typing import Optional

from requests import HTTPError
from showcase.db import tables
from pyairtable.formulas import match

def get_user_record_id_by_email(email: str) -> Optional[str]:
    users_table = tables['users']
    # Use formula filtering to search by email
    try:
        formula = match({'Email': email})
        records = users_table.all(formula=formula)
        return records[0]['id'] if records else None
    except HTTPError as e:
        if '404' in str(e):  # Check specifically for 404 error
            return None
        raise  # Re-raise other HTTP errors