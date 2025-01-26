from pydantic import BaseModel
from podium.constants import SingleRecordField

class ReferralBase(BaseModel):
    content: str = ""
    event: SingleRecordField
    user: SingleRecordField

