from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_repo
from db.schemas import Book, BookCreate, BookPatch


router = APIRouter()


@router.post("/", response_model=Book, status_code=201)
def create(item: BookCreate, item_repo: Session = Depends(get_book_repo)):
    book = item_repo.create(item)
    
    return book


@router.get("/pending", response_model=list[Book | None], status_code=200)
def read_pending(item_repo: Session = Depends(get_book_repo)):
    books = item_repo.read_pending()
    
    return books


@router.get("/{item_id}", response_model=Book, status_code=200)
def read_by_id(item_id: int, item_repo: Session = Depends(get_book_repo)):
    book = item_repo.read_by_id(item_id)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book


@router.get("/", response_model=list[Book | None], status_code=200)
def read(item_repo: Session = Depends(get_book_repo)):
    books = item_repo.read()
    
    return books


@router.patch("/{item_id}", status_code=204)
def patch(item: BookPatch, item_id: int, item_repo: Session = Depends(get_book_repo)):
    response = item_repo.patch(item=item, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, item_repo: Session = Depends(get_book_repo)):
    response = item_repo.delete(item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")