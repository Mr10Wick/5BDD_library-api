from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_current_user, get_db
from app.models import Loan, User
from app.schemas.loan import LoanOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "created_at": current_user.created_at,
    }

@router.get("/me/loans", response_model=list[LoanOut])
def read_my_loans(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    loans = db.query(Loan).filter(Loan.user_id == current_user.id).order_by(Loan.borrowed_at.desc()).all()
    return loans

@router.get("/me/loans/history", response_model=list[LoanOut])
def read_my_loans_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    loans = (
        db.query(Loan)
        .filter(Loan.user_id == current_user.id)
        .order_by(Loan.borrowed_at.desc())
        .all()
    )
    return loans
