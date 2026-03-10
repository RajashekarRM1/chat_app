from jose import jwt
import datetime

SECRET_KEY="jhbcwdhbhwcwbcfwice23ehruif4897rv"
ALGORITHM="HS256"

def create_token(user_id:int):
    payload={
        "user_id":user_id,
        "exp":datetime.datetime.utcnow()+datetime.timedelta(hours=24)

    }

    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)