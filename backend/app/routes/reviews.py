from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from pydantic import BaseModel
from datetime import datetime

from ..database import get_db
from ..models import Review

router = APIRouter()


class ReviewSummary(BaseModel):
    id: int
    pr_number: int
    repo_full_name: str
    pr_title: str
    pr_url: str
    pr_author: str
    severity: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewDetail(ReviewSummary):
    security_review: str | None
    logic_review: str | None
    style_review: str | None
    final_review: str | None


class Stats(BaseModel):
    total: int
    high: int
    medium: int
    low: int


@router.get("/reviews", response_model=List[ReviewSummary])
async def list_reviews(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Review).order_by(Review.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get("/reviews/stats", response_model=Stats)
async def get_stats(db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count(Review.id)))
    high = await db.scalar(select(func.count(Review.id)).where(Review.severity == "high"))
    medium = await db.scalar(select(func.count(Review.id)).where(Review.severity == "medium"))
    low = await db.scalar(select(func.count(Review.id)).where(Review.severity == "low"))
    return Stats(total=total or 0, high=high or 0, medium=medium or 0, low=low or 0)


@router.get("/reviews/{review_id}", response_model=ReviewDetail)
async def get_review(review_id: int, db: AsyncSession = Depends(get_db)):
    review = await db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review
