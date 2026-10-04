from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session

from api.models import Task
from api.schemas import TaskCreate


def create_task(db: Session, user_id: str, data: TaskCreate) -> Task:
    target_date = data.due_date.astimezone(timezone.utc)
    if target_date <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="The date provided is not in the future")

    task = Task(
        name=data.name,
        url=str(data.url),
        due_date=target_date,
        user_id=user_id,
    )
    db.add(task)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(task)
    return task
