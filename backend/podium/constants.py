from typing import Annotated, List
from annotated_types import Len
from pydantic import StringConstraints



RECORD_REGEX = r"^rec\w*$"
MultiRecordField = List[Annotated[str, StringConstraints(pattern=RECORD_REGEX)]]