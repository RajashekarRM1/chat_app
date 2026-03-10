from sqlalchemy.orm import Session
from models.generated_models import Users
from utils.password import hash_password, verify_password
from utils.jwt_handler import create_token


def register_user(data, db: Session):

    user = Users(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(data, db: Session):

    user = db.query(Users).filter(Users.email == data.email).first()

    if not user:
        return None

    if not verify_password(data.password, user.password):
        return None

    token = create_token(user.id)

    return token

def get_all_users(db: Session):

    return db.query(Users).all()


def get_user(user_id: int, db: Session):

    return db.query(Users).filter(Users.id == user_id).first()