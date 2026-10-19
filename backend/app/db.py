import os
from sqlalchemy import create_engine, String, Float, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from datetime import datetime, timezone

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agromind.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class PredictionRecord(Base):
    __tablename__ = "predictions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    crop: Mapped[str] = mapped_column(String(80))
    confidence: Mapped[float] = mapped_column(Float)
    inputs_json: Mapped[str] = mapped_column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)
