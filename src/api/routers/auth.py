from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from api.config import REDIRECT_URI, workos_client

router = APIRouter()


@router.get("/auth/login")
def login():
    authorization_url = workos_client.user_management.get_authorization_url(
        redirect_uri=REDIRECT_URI,
        provider="authkit",
    )
    return RedirectResponse(url=authorization_url)


@router.get("/auth/callback")
def callback(code: str):
    authentication = workos_client.user_management.authenticate_with_code(code=code)
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
