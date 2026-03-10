from pydantic import BaseModel


class AddParticipant(BaseModel):

    conversation_id: int
    user_id: int