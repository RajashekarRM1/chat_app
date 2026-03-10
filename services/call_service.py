from sqlalchemy.orm import Session
from models.generated_models import Calls
import datetime


def start_call(data, db: Session):

    call = Calls(
        conversation_id=data.conversation_id,
        caller_id=data.caller_id,
        call_type=data.call_type,
        call_status=data.call_status,
        started_at=datetime.datetime.utcnow()
    )

    db.add(call)
    db.commit()
    db.refresh(call)

    return call