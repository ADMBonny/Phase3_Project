from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from models.database import SessionLocal
from passlib.hash import pbkdf2_sha256 as sha256

def create_user(username: str, password: str) -> dict:
    if not username or not password:
        return {"error": "Username and password are required."}
    with SessionLocal() as db:
        try:
            if db.query(User).filter(User.username == username).first():
                return {"error": "Username already exists."}
            hashed_password = sha256.hash(password)
            user = User(username=username, password_hash=hashed_password)
            db.add(user)
            db.commit()
            return {"message": "User created successfully."}
        except SQLAlchemyError as e:
            db.rollback()
            return {"error": str(e)}

def authenticate_user(username: str, password: str) -> bool:
    with SessionLocal() as db:
        user: User = db.query(User).filter(User.username == username).first()
        if user and sha256.verify(password, user.password_hash):
            return True
        return False
