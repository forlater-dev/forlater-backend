from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_session
from api.dependencies import get_current_user_id
from api.schemas import ApiKeyCreate, ApiKeyCreated, ApiKeyRead
from api.services.api_key_service import create_api_key, list_api_key, revoke_api_key

router = APIRouter()

@router.post("/api/keys",response_model=ApiKeyCreated)
async def post_api_key(data:ApiKeyCreate,
                       db: Annotated[AsyncSession,Depends(get_session)],
                       user_id: Annotated[str,Depends(get_current_user_id)]) -> ApiKeyCreated:

    record, raw_key = await create_api_key(db=db,user_id=user_id,name=data.name)

    return ApiKeyCreated(id=record.id
                      ,prefix=record.prefix
                      ,name=record.name,
                      created_at=record.created_at,
                      key=raw_key)

@router.get("/api/keys",response_model=list[ApiKeyRead])
async def get_api_keys(db:Annotated[AsyncSession,Depends(get_session)],
                        user_id: Annotated[str,Depends(get_current_user_id)]):
    return await list_api_key(db=db,user_id=user_id)

@router.delete("/api/keys/{key_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(db:Annotated[AsyncSession,Depends(get_session)], user_id:Annotated[str,Depends(get_current_user_id)],key_id:int):
    return await revoke_api_key(db=db,user_id=user_id,key_id=key_id)
