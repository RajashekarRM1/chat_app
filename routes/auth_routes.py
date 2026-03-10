from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.user_schema import UserCreate
from schemas.user_schema import LoginSchema
from services.auth_service import get_all_users, get_user, register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):

    return register_user(data, db)


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    token = login_user(data, db)

    if not token:
        return {"error": "Invalid credentials"}

    return {"access_token": token}


@router.get("/")
def users(db: Session = Depends(get_db)):

    return get_all_users(db)


@router.get("/{user_id}")
def user(user_id: int, db: Session = Depends(get_db)):

    return get_user(user_id, db)