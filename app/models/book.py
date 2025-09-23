from datetime import date, datetime
from sqlalchemy import Integer, String, Date, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    genre: Mapped[str | None] = mapped_column(String(100))
    published_date: Mapped[date | None] = mapped_column(Date)
    available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)

    loans: Mapped[list["Loan"]] = relationship(back_populates="book", cascade="all, delete-orphan")
