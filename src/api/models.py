from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

from api.schemas import TaskStatus


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    url: str
    due_date: datetime = Field(sa_type=DateTime(timezone=True), index=True)
    user_id: str = Field(foreign_key="user.id",index=True)
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )
    user: "User" = Relationship(back_populates="tasks")

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    remaining_units: int = Field(default=5)
    tasks: list["Task"] = Relationship(back_populates="user")

class ApiKey(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    name: str
    user_id: str = Field(foreign_key="user.id",index=True)
    key_hash: str = Field(unique=True, index=True)
    prefix: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                 sa_type=DateTime(timezone=True),
                                 nullable=False)
    revoked_at: datetime|None = Field(default=None,
                                      sa_type=DateTime(timezone=True))

