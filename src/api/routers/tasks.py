from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_session
from api.dependencies import get_current_user_id,get_task_user_id
from api.models import Task
from api.schemas import TaskCreate, TaskRead
from api.services.task_service import create_task

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def post_task(
    data: TaskCreate,
    db: Annotated[AsyncSession, Depends(get_session)],
    user_id: Annotated[str, Depends(get_task_user_id)],
) -> Task:
    return await create_task(db, user_id, data)
