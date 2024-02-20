from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base
from passlib.hash import pbkdf2_sha256 as sha256

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(100))

    transactions = relationship("Transaction", back_populates="user")

    def set_password(self, password):
        self.password_hash = sha256.hash(password)

    def check_password(self, password):
        return sha256.verify(password, self.password_hash)
