from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.db import init_db
from fastapi.middleware.cors import CORSMiddleware
from api.config import FRONTEND_URL
from api.routers import auth, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

app.include_router(tasks.router)
