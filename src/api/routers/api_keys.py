from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_session
from api.dependencies import get_current_user_id
from api.schemas import ApiKeyCreate, ApiKeyRead
from api.services.api_key_service import create_api_key

router = APIRouter()

@router.post("/api/keys",response_model=ApiKeyRead)
async def post_api_key(data:ApiKeyCreate,
                       db: Annotated[AsyncSession,Depends(get_session)],
                       user_id: Annotated[str,Depends(get_current_user_id)]) -> ApiKeyRead:

    record, raw_key = await create_api_key(db=db,user_id=user_id,name=data.name)

    return ApiKeyRead(id=record.id
                      ,prefix=record.prefix
                      ,name=record.name,
                      created_at=record.created_at,
                      key=raw_key)


