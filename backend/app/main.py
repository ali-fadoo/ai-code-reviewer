from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .config import settings
from .routes.webhook import router as webhook_router
from .routes.reviews import router as reviews_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="AI Code Reviewer",
    description="Multi-agent PR review powered by Claude",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router, tags=["webhook"])
app.include_router(reviews_router, prefix="/api", tags=["reviews"])


@app.get("/health")
async def health():
    return {"status": "ok"}
