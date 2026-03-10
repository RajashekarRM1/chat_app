from pydantic import BaseModel


class ConversationCreate(BaseModel):

    created_by: int