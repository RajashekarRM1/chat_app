from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.message_schema import MessageCreate
from services.message_service import send_message, get_conversation_messages

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/send")
def create_message(data: MessageCreate, db: Session = Depends(get_db)):
    return send_message(data, db)


@router.get("/{conversation_id}")
def conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    return get_conversation_messages(conversation_id, db)