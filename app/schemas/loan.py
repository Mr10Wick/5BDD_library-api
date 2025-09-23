from datetime import datetime
from pydantic import BaseModel

class BorrowRequest(BaseModel):
    book_id: int

class ReturnRequest(BaseModel):
    loan_id: int

class LoanOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    returned_at: datetime | None = None

    class Config:
        from_attributes = True
