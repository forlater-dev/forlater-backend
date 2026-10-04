from fastapi import APIRouter
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from api.config import workos_client, REDIRECT_URI, FRONTEND_URL


router = APIRouter()

@router.get("/auth/login")
def login():
    authorization_url = workos_client.sso.get_authorization_url(
        redirect_uri=REDIRECT_URI,
        provider="authkit",
    )
    return RedirectResponse(url=authorization_url)


@router.get("/auth/callback")
def callback(code: str, response: Response):
    profile_and_token = workos_client.sso.get_profile_and_token(code=code)
    profile = profile_and_token.profile

    redirect = RedirectResponse(url=f"{FRONTEND_URL}/dashboard")

    redirect.set_cookie(
        key="session_user_id",
        value=profile.id,
        httponly=True,
        samesite="lax",
        secure=False,  
        domain="localhost",
    )

    return redirect


@router.get("/api/me")
def get_current_user(request: Request):
    user_id = request.cookies.get("session_user_id")
    if not user_id:
        return {"authenticated": False, "user": None}

    return {"authenticated": True, "user_id": user_id}
