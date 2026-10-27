from typing import Annotated

from api.db import session_factory

from fastapi import Depends, HTTPException, Request
from workos.session import AuthenticateWithSessionCookieSuccessResponse

from api.config import WORKOS_COOKIE_PASSWORD, workos_client
from api.services.api_key_service import get_api_key_user_id
from starlette.concurrency import run_in_threadpool


def get_session_user_id(request: Request) -> str | None:
    cookie = request.cookies.get("session")
    if not cookie:
        return None

    session = workos_client.user_management.load_sealed_session(
        session_data=cookie,
        cookie_password=WORKOS_COOKIE_PASSWORD,
    )
    result = session.authenticate()
    if not isinstance(result, AuthenticateWithSessionCookieSuccessResponse):
        return None
    if not result.authenticated or not result.user:
        return None
    user_id = result.user.get("id")
    return user_id if isinstance(user_id, str) and user_id else None


def get_current_user_id(
    user_id: Annotated[str | None, Depends(get_session_user_id)],
) -> str:
    if user_id is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return user_id

async def get_task_user_id(request: Request) -> str:
    authorization = request.headers.get("Authorization")

    if authorization is not None:
        parts = authorization.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        raw_key = parts[1]

        async with session_factory() as db:
            user_id = await get_api_key_user_id(db=db,raw_key=raw_key)

    else: 
        user_id = await run_in_threadpool(get_session_user_id,request)
            
    if user_id is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    return user_id
