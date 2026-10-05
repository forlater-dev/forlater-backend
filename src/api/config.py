import os
from dotenv import load_dotenv
from workos import WorkOSClient
from sqlalchemy import URL

load_dotenv()

WORKOS_API_KEY = os.getenv("WORKOS_API_KEY")
WORKOS_CLIENT_ID = os.getenv("WORKOS_CLIENT_ID")
REDIRECT_URI = os.getenv("WORKOS_REDIRECT_URI", "http://localhost:8000/auth/callback")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
DATABASE_URL = os.getenv("DATABASE_URL") or URL.create(
    "postgresql+asyncpg",
    username=os.getenv("POSTGRES_USER", "forlater"),
    password=os.getenv("POSTGRES_PASSWORD", "change-me"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    database=os.getenv("POSTGRES_DB", "forlater"),
)

workos_client = WorkOSClient(api_key=WORKOS_API_KEY, client_id=WORKOS_CLIENT_ID)

