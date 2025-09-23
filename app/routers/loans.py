from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models import Loan, User, Book
from app.schemas.loan import BorrowRequest, ReturnRequest, LoanOut

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/borrow", response_model=LoanOut)
def borrow(payload: BorrowRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = current_user
    book = db.get(Book, payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.available:
        raise HTTPException(status_code=400, detail="Book not available")
    loan = Loan(user_id=user.id, book_id=book.id)
    book.available = False
    db.add(loan)
    db.add(book)
    db.commit()
    db.refresh(loan)
    return loan

@router.post("/return", response_model=LoanOut)
def return_book(payload: ReturnRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    loan = db.get(Loan, payload.loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your loan")
    if loan.returned_at:
        raise HTTPException(status_code=400, detail="Already returned")
    loan.returned_at = datetime.now(timezone.utc)
    book = db.get(Book, loan.book_id)
    if book:
        book.available = True
        db.add(book)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan
