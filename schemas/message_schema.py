from pydantic import BaseModel
from typing import Optional


class MessageCreate(BaseModel):

    conversation_id: int
    sender_id: int
    message_text: Optional[str] = None
    message_type: Optional[str] = "text"
    file_url: Optional[str] = None


class MessageResponse(BaseModel):

    id: int
    conversation_id: int
    sender_id: int
    message_text: Optional[str]

    class Config:
        from_attributes = True