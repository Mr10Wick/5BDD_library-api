from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.deps import get_db, get_current_user
from app.models import Book, User
from app.schemas.book import BookCreate, BookUpdate, BookOut

router = APIRouter(prefix="/books", tags=["books"])

@router.post("", response_model=BookOut)
def add_book(payload: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = Book(
        title=payload.title,
        author=payload.author,
        genre=payload.genre,
        published_date=payload.published_date,
        available=True,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(book, k, v)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"deleted": True}

@router.get("", response_model=list[BookOut])
def search_books(q: str | None = Query(default=None), author: str | None = None, title: str | None = None, genre: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if q:
        query = query.filter(or_(Book.title.ilike(f"%{q}%"), Book.author.ilike(f"%{q}%"), Book.genre.ilike(f"%{q}%")))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    return query.order_by(Book.id).all()
