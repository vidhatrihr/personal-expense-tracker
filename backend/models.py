from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  email = Column(String, unique=True)
  password = Column(String)

  budget = relationship('Budget', back_populates='user', uselist=False)
  expenses = relationship('Expense', back_populates='user')


class Budget(db.Model):
  __tablename__ = 'budgets'
  id = Column(Integer, primary_key=True, autoincrement=True)
  amount = Column(Float, default=0)
  user_id = Column(Integer, ForeignKey('users.id'))

  user = relationship('User', back_populates='budget')


class Expense(db.Model):
  __tablename__ = 'expenses'
  id = Column(Integer, primary_key=True, autoincrement=True)
  amount = Column(Float)
  category = Column(String)
  description = Column(String)
  user_id = Column(Integer, ForeignKey('users.id'))

  user = relationship('User', back_populates='expenses')
