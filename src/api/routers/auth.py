from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from api.config import REDIRECT_URI, workos_client
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
    authentication = await run_in_threadpool(workos_client.user_management.authenticate_with_code
                                             ,code=code,)
    async with db.begin():
        user = await db.get(User,authentication.user.id)
        if not user:
            db.add(User(id=authentication.user.id))

    redirect = RedirectResponse(url="/docs")
    redirect.set_cookie(
        key="session_user_id",
        value=authentication.user.id,
        httponly=True,
        samesite="lax",
        secure=False,
        path="/",
    )
    return redirect


@router.get("/api/me")
def get_current_user(request: Request):
    user_id = request.cookies.get("session_user_id")
    if not user_id:
        return {"authenticated": False, "user": None}
    return {"authenticated": True, "user_id": user_id}
