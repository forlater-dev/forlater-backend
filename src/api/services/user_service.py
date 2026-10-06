from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from api.models import User


async def consume_unit(db: AsyncSession, user_id: str) -> None:
    user = await db.scalar(select(User).where(User.id==user_id).with_for_update())

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    if user.remaining_units < 1:
        raise HTTPException(status_code=400, detail="Limit of scheduling is exhausted")

    user.remaining_units -= 1



