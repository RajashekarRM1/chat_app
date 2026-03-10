from sqlalchemy.orm import Session
from models.generated_models import ConversationParticipants


def add_participant(data, db: Session):

    participant = ConversationParticipants(
        conversation_id=data.conversation_id,
        user_id=data.user_id
    )

    db.add(participant)
    db.commit()
    db.refresh(participant)

    return participant