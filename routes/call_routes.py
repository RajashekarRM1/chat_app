from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.call_schema import CallCreate
from services.call_service import start_call

router = APIRouter(prefix="/calls", tags=["Calls"])


@router.post("/start")
def create_call(data: CallCreate, db: Session = Depends(get_db)):
    return start_call(data, db)