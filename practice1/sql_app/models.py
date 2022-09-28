from operator import index
from sqlalchemy import Boolean, String, Integer, ForeignKey, Column, Date, DateTime
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  fullname = Column(String, index=True)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  phone_number = Column(String, index=True)
  address = Column(String)
  # birth_day = Column(Date)

  comments = relationship("Comment", back_populates="users")


class Comment(Base):
  __tablename__ = "comments"

  id = Column(Integer, primary_key=True, index=True)
  content = Column(String)
  start = Column(Integer, index=True)
  datetime = Column(DateTime)
  user_id =Column(Integer, ForeignKey("users.id"))
  book_id = Column(Integer, ForeignKey("books.id"))

  users = relationship("User", back_populates="comments")
  books = relationship("Book", back_populates="comments")


class Book(Base):
  __tablename__ = "books"

  id = Column(Integer, primary_key=True, index=True)
  book_name = Column(String, index=True)
  author = Column(String, index=True)
  description = Column(String)
  category_id = Column(Integer, ForeignKey("categories.id"))

  comments = relationship("Comment", back_populates="books")
  categories = relationship("Category", back_populates="books")


class Category(Base):
  __tablename__ = "categories"

  id = Column(Integer, primary_key=True, index=True)
  category_name = Column(String, index=True)

  books = relationship("Book", back_populates="categories")
