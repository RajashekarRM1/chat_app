from pydantic import BaseModel
from typing import Optional


class CallCreate(BaseModel):

    conversation_id: int
    caller_id: int
    call_type: str
    call_status: Optional[str] = "started"