import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import workos
from workos import WorkOSClient

load_dotenv()
workos_client = WorkOSClient(api_key = os.getenv("WORKOS_API_KEY"),client_id = os.getenv("WORKOS_CLIENT_ID"))

REDIRECT_URI = os.getenv("WORKOS_REDIRECT_URI","http://localhost:3000/auth/callback")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/auth/login")
def login():
    authorization_url = workos_client.sso.get_authorization_url(
        redirect_uri=REDIRECT_URI,
        provider="authkit",
    )
    return RedirectResponse(url=authorization_url)


@app.get("/auth/callback")
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


@app.get("/api/me")
def get_current_user(request: Request):
    user_id = request.cookies.get("session_user_id")
    if not user_id:
        return {"authenticated": False, "user": None}

    return {"authenticated": True, "user_id": user_id}
