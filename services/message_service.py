from sqlalchemy.orm import Session
from models.generated_models import Messages


def send_message(data, db: Session):

    message = Messages(
        conversation_id=data.conversation_id,
        sender_id=data.sender_id,
        message_text=data.message_text,
        message_type=data.message_type,
        file_url=data.file_url
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_conversation_messages(conversation_id: int, db: Session):

    return db.query(Messages).filter(
        Messages.conversation_id == conversation_id
    ).all()