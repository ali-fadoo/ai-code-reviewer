from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    pr_number = Column(Integer, nullable=False)
    repo_full_name = Column(String, nullable=False)
    pr_title = Column(String, nullable=False)
    pr_url = Column(String, nullable=False)
    pr_author = Column(String, nullable=False)
    security_review = Column(Text)
    logic_review = Column(Text)
    style_review = Column(Text)
    final_review = Column(Text)
    severity = Column(String, default="low")
    status = Column(String, default="completed")
    created_at = Column(DateTime, server_default=func.now())
