from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import secrets

from sqlmodel import col, select
from api.models import ApiKey, User
import hashlib

async def create_api_key(db:AsyncSession,
                         user_id:str,
                         name:str) -> tuple[ApiKey,str]:
    raw_key = f"fl_{secrets.token_urlsafe(32)}"
    key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
    prefix = raw_key[:11]
    
    api_key = ApiKey(name=name,user_id=user_id,key_hash=key_hash,prefix=prefix)

    async with db.begin():
        db.add(api_key)

    return api_key, raw_key

async def get_api_key_user_id(
    db: AsyncSession,
        raw_key: str,
) -> str|None:
    key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    statement = select(ApiKey.user_id).where(
        ApiKey.key_hash== key_hash,
        col(ApiKey.revoked_at).is_(None))

    return await db.scalar(statement)

async def list_api_key(db:AsyncSession,
                       user_id: str,) -> list[ApiKey]:
    statement = select(ApiKey).where(ApiKey.user_id==user_id)
    
    result = await db.scalars(statement)
    
    return list(result)

async def revoke_api_key(db: AsyncSession,
                         user_id: str,
                         key_id: int) -> None:
    statement = select(ApiKey).where(ApiKey.id==key_id,ApiKey.user_id==user_id)

    async with db.begin():
        key = await db.scalar(statement)

        if not key:
            raise HTTPException(status_code=404, detail="API key not found")

        if key.revoked_at is None:
            key.revoked_at = datetime.now(timezone.utc)


    

    



