from sqlalchemy.orm import Session
from models.generated_models import Conversations


def create_conversation(data, db: Session):

    conversation = Conversations(
        created_by=data.created_by
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversations(db: Session):

    return db.query(Conversations).all()