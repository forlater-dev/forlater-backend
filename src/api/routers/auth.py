from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from workos.session import seal_session_from_auth_response

from api.config import REDIRECT_URI, WORKOS_COOKIE_PASSWORD, workos_client
from api.dependencies import get_session_user_id
from api.models import User
from api.db import get_session
from starlette.concurrency import run_in_threadpool
router = APIRouter()


@router.get("/auth/login")
def login():
    authorization_url = workos_client.user_management.get_authorization_url(
        redirect_uri=REDIRECT_URI,
        provider="authkit",
    )
    return RedirectResponse(url=authorization_url)


@router.get("/auth/callback")
async def callback(db: Annotated[AsyncSession,Depends(get_session)],code: str):
    authentication = await run_in_threadpool(
        workos_client.user_management.authenticate_with_code,
        code=code,
    )
    sealed_session = seal_session_from_auth_response(
        access_token=authentication.access_token,
        refresh_token=authentication.refresh_token,
        user=authentication.user.to_dict(),
        cookie_password=WORKOS_COOKIE_PASSWORD,
    )
    async with db.begin():
        user = await db.get(User,authentication.user.id)
        if not user:
            db.add(User(id=authentication.user.id))

    redirect = RedirectResponse(url="/docs")
    redirect.set_cookie(
        key="session",
        value=sealed_session,
        httponly=True,
        samesite="lax",
        secure=False,
        path="/",
    )
    return redirect


@router.get("/api/me")
def get_current_user(
    user_id: Annotated[str | None, Depends(get_session_user_id)],
):
    if not user_id:
        return {"authenticated": False, "user": None}
    return {"authenticated": True, "user_id": user_id}
