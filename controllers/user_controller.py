from sqlalchemy.orm import Session
from models.user import User
from models.database import SessionLocal
from passlib.hash import pbkdf2_sha256 as sha256

def create_user(username: str, password: str) -> User:
    db: Session = SessionLocal()
    hashed_password = sha256.hash(password)
    user = User(username=username, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def authenticate_user(username: str, password: str) -> bool:
    db: Session = SessionLocal()
    user: User = db.query(User).filter(User.username == username).first()
    db.close()
    if user and sha256.verify(password, user.password_hash):
        return True
    return False
