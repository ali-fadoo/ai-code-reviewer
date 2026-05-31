import hashlib
import hmac
import logging
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks

from ..config import settings
from ..database import AsyncSessionLocal
from ..services.reviewer import process_pull_request

logger = logging.getLogger(__name__)
router = APIRouter()


def verify_signature(payload: bytes, signature: str) -> bool:
    expected = hmac.new(
        settings.github_webhook_secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


async def run_review(payload: dict) -> None:
    async with AsyncSessionLocal() as db:
        try:
            await process_pull_request(payload, db)
        except Exception as e:
            logger.error(f"Review pipeline failed: {e}", exc_info=True)


@router.post("/webhook")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
):
    signature = request.headers.get("X-Hub-Signature-256", "")
    body = await request.body()

    if not verify_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = request.headers.get("X-GitHub-Event")
    if event != "pull_request":
        return {"status": "ignored", "event": event}

    payload = await request.json()
    action = payload.get("action")

    if action not in ("opened", "synchronize", "reopened"):
        return {"status": "ignored", "action": action}

    background_tasks.add_task(run_review, payload)
    return {"status": "processing", "pr": payload["pull_request"]["number"]}
