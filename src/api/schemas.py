from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import AwareDatetime, HttpUrl, StringConstraints
from sqlmodel import SQLModel


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskBase(SQLModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    url: HttpUrl
    due_date: AwareDatetime


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    status: TaskStatus
    created_at: datetime

class ApiKeyCreate(SQLModel):
    name: Annotated[str,StringConstraints(strip_whitespace=True, min_length=1,max_length=100)]

class ApiKeyRead(SQLModel):
    id: int| None
    name: str
    prefix: str
    created_at: datetime
    key: str
