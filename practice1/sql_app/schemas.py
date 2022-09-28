from typing import Union, List
from datetime import datetime, date
from unicodedata import category

from pydantic import BaseModel

# CommentModel
class CommentBase(BaseModel):
  content: str
  start: int
  datetime: datetime

class CommentCreate(CommentBase):
  pass

class CommentUpdate(CommentBase):
  pass

class Comment(CommentBase):
  id: int
  user_id: int
  book_id: int

  class Config: 
    orm_mode = True

# UserModel
class UserBase(BaseModel):
  fullname: str
  email: str
  phone_number: str
  address: str
  # birth_day: date

class UserCreate(UserBase):
  password: str

class UserUpdate(UserBase):
  pass

class User(UserBase):
  id: int
  comments: List[Comment] = []

  class Config: 
    orm_mode = True

# BookModel
class BookBase(BaseModel):
  book_name: str
  author: str
  description: str

class BookCreate(BookBase):
  pass

class BookUpdate(BookBase):
  category_id: int

  class Config:
    orm_mode = True

class Book(BookBase):
  id: int
  category_id: int
  comment: List[Comment] = []

  class Config:
    orm_mode = True

# CategoryModel
class CategoryBase(BaseModel):
  category_name: str

class CategoryCreate(CategoryBase):
  pass

class Category(CategoryBase):
  id: int
  books: List[Book] = []

  class Config:
    orm_mode = True
