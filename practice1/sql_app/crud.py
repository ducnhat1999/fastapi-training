from sqlalchemy import and_ , or_
from sqlalchemy.orm import Session

from . import models, schemas

# get user by user_id
def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

# get user by email
def get_user_by_email(db: Session, email: str):
  return db.query(models.User).filter(models.User.email == email).first()

# get book by book_id
def get_book(db: Session, book_id:int):
  return db.query(models.Book).filter(models.Book.id == book_id).first()

# get books
def get_books(db: Session):
  return db.query(models.Book).all()

# create user
def create_user(db: Session, user: schemas.UserCreate):
  fake_hashed_password = user.password + "fake"
  db_user = models.User(**user.dict(exclude={'password'}), hashed_password=fake_hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

#create book
def create_book(db: Session, book: schemas.BookCreate, cat_id: int):
  db_book = models.Book(**book.dict(), category_id = cat_id)
  db.add(db_book)
  db.commit()
  db.refresh(db_book)
  return db_book

# get comment by user id
def get_comment_by_user(db: Session, user_id: int):
  return db.query(models.Comment).filter(models.Comment.user_id == user_id).all()

# create comment
def create_comment(db: Session, user_id:int, book_id: int,  comment: schemas.CommentCreate):
  db_comment = models.Comment(**comment.dict(), user_id=user_id, book_id=book_id)
  db.add(db_comment)
  db.commit()
  db.refresh(db_comment)
  return db_comment

# update user information
async def update_user_info(db: Session, user: schemas.UserUpdate):
  db_user = db.merge(user)
  db.commit()
  return db_user

#update book infomation
async def update_book_info(db: Session, book: schemas.BookUpdate):
  db_book = db.merge(book)
  db.commit()
  return db_book

# get category
def get_category(db: Session, category_id: int):
  return db.query(models.Category).filter(models.Category.id == category_id).first()

# create category
def create_category(db: Session, category: schemas.CategoryCreate):
  db_category = models.Category(**category.dict())
  db.add(db_category)
  db.commit()
  db.refresh(db_category)
  return db_category

# delete book
def delete_book(db: Session, book_id: int):
  db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
  db.delete(db_book)
  db.commit()

# get book name
def get_book_by_name(db: Session, book_name: str):
  return db.query(models.Book).filter(models.Book.book_name.contains(book_name)).all()

# get comments by book
def get_comments_by_book(db: Session, book_id: int):
  return db.query(models.Comment).filter(models.Comment.book_id == book_id).all()

# delete user
def delete_user(db: Session, user_id: int):
  db_user = db.query(models.User).filter(models.User.id == user_id).first()
  db.delete(db_user)
  db.commit()

# get user login
def get_user_login(db: Session, email: str, password: str):
  hashed_password = password + "fake"
  db_user = db.query(models.User).filter(models.User.email == email, models.User.hashed_password == hashed_password).first()
  if db_user:
    return db_user
  else: 
    return None

# get_comment
def get_comment(db: Session, comment_id: int):
  return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

# delete comment
def delete_comment(db: Session, comment_id: int):
  db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
  db.delete(db_comment)
  db.commit()

async def update_comment(db: Session, comment: schemas.CommentUpdate):
  db_comment = db.merge(comment)
  db.commit()
  return db_comment
