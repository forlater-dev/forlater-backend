from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Task
from api.schemas import TaskCreate


async def create_task(db: AsyncSession, user_id: str, data: TaskCreate) -> Task:
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
      await db.commit()
    except Exception:
        await db.rollback()
        raise
    await db.refresh(task)
    return task
