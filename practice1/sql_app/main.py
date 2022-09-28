from urllib import response
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, SessionLocal
from fastapi.encoders import jsonable_encoder

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# create user
@app.post("/users/", response_model=schemas.User, tags=['Users'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_email(db, email=user.email)
  if db_user:
    HTTPException(status_code=400, detail="Email already registered")
  return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User, tags=['Users'])
def read_user(user_id: int, db: Session = Depends(get_db)):
  db_user = crud.get_user(db, user_id=user_id)
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")
  return db_user

@app.post("/categories/{category_id}/book/", response_model=schemas.Book, tags=["Books"])
def create_book_for_category(category_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
  return crud.create_book(db=db, book=book, cat_id=category_id)

@app.get("/comments/{user_id}", response_model=List[schemas.Comment], tags=["Comments"])
def get_comment_by_user(user_id: int, db: Session = Depends(get_db)):
  db_user = crud.get_user(db, user_id=user_id)
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")
  db_comment = crud.get_comment_by_user(db, user_id=user_id)
  return db_comment

@app.post("/users/{user_id}/books/{book_id}/comment", response_model=schemas.Comment, tags=["Comments"])
def create_comment(user_id:int, book_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
  db_user = crud.get_user(db, user_id=user_id)
  db_book = crud.get_book(db, book_id=book_id)
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")
  if not db_book:
    raise HTTPException(status_code=404, detail="Book not found")
  db_comment = crud.create_comment(db=db, user_id=user_id, book_id=book_id, comment=comment)
  return db_comment

@app.put("/users/{user_id}", response_model=schemas.User, tags=['Users'])
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
  db_user = crud.get_user(db, user_id=user_id)
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")
  update_item_encoder = jsonable_encoder(user)
  db_user.fullname = update_item_encoder["fullname"]
  db_user.email = update_item_encoder["email"]
  db_user.phone_number = update_item_encoder["phone_number"]
  db_user.address = update_item_encoder["address"]
  return await crud.update_user_info(db=db, user=db_user)
  
@app.put("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
async def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
  db_book = crud.get_book(db, book_id=book_id)
  db_category = crud.get_category(db, category_id=book.category_id)
  if not db_book:
    raise HTTPException(status_code=404, detail="Book not found")
  if not db_category:
    raise HTTPException(status_code=404, detail="Category not found")
  update_book_endoder = jsonable_encoder(book)
  db_book.book_name = update_book_endoder["book_name"]
  db_book.author = update_book_endoder["author"]
  db_book.description = update_book_endoder["description"]
  db_book.category_id = update_book_endoder["category_id"]
  return await crud.update_book_info(db=db, book=db_book)

@app.post("/categories/", response_model=schemas.Category, tags=["Categories"])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
  return crud.create_category(db=db, category=category)

@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
  db_book = crud.get_book(db, book_id=book_id)
  if not db_book:
    HTTPException(status_code=404, detail="Book not found")
  return crud.delete_book(db=db, book_id=book_id)

@app.get("/books/", response_model = List[schemas.Book], tags=["Books"])
def get_books_by_name(book_name: str, db: Session = Depends(get_db)):
  return crud.get_book_by_name(db, book_name=book_name)

@app.get("/books/{book_id}/comments", response_model=List[schemas.Comment], tags=["Comments"])
def get_comments_by_book(book_id: int, db: Session = Depends(get_db)):
  db_book = crud.get_book(db, book_id=book_id)
  if not db_book:
    raise HTTPException(status_code=404, detail="Book not found")
  return crud.get_comments_by_book(db, book_id=book_id)

@app.delete("/users/{user_id}", tags=['Users'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
  db_user = crud.get_user(db, user_id=user_id)
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")
  return crud.delete_user(db=db, user_id=user_id)

@app.get("/users", response_model=schemas.User, tags=['Users'])
def get_user_login(email: str, password: str, db: Session = Depends(get_db)):
  db_user =  crud.get_user_login(db, email=email, password=password)
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")
  return db_user 

@app.delete("/comment/{comment_id}", tags=["Comments"])
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
  db_comment = crud.get_comment(db, comment_id=comment_id)
  if not db_comment:
    raise HTTPException(status_code=404, detail="Comment not found")
  return crud.delete_comment(db, comment_id=comment_id)

@app.put("/comments/{comment_id}", response_model=schemas.Comment, tags=["Comments"])
async def update_comment(comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db)):
  db_comment = crud.get_comment(db, comment_id=comment_id)
  if not db_comment:
    raise HTTPException(status_code = 404, detail = "Comment not found")
  comment_update = jsonable_encoder(comment)
  db_comment.content = comment_update["content"]
  db_comment.start = comment_update["start"]
  db_comment.datetime = comment.datetime
  return await crud.update_comment(db=db, comment=db_comment)

