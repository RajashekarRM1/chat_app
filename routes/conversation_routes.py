from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.conversation_schema import ConversationCreate
from services.conversation_service import create_conversation, get_conversations

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.post("/")
def create(data: ConversationCreate, db: Session = Depends(get_db)):

    return create_conversation(data, db)


@router.get("/")
def conversations(db: Session = Depends(get_db)):

    return get_conversations(db)