from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Task
from api.schemas import TaskCreate

from api.services.user_service import consume_unit


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

    async with db.begin():
        await consume_unit(db=db,user_id=user_id)
        db.add(task)

    await db.refresh(task)
    return task
