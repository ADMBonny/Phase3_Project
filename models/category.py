from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    transactions = relationship("Transaction", secondary="transaction_category", back_populates="categories")
