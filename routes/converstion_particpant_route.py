from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.conversions_particpants_schema import AddParticipant
from services.conversation_particpant_service import add_participant

router = APIRouter(prefix="/participants", tags=["Participants"])


@router.post("/add")
def add_user(data: AddParticipant, db: Session = Depends(get_db)):
    return add_participant(data, db)