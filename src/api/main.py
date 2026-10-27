from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.db import engine
from fastapi.middleware.cors import CORSMiddleware
from api.config import FRONTEND_URL
from api.routers import auth, tasks, api_keys


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await engine.dispose()

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
app.include_router(api_keys.router)
