from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from models.database import SessionLocal
from passlib.hash import pbkdf2_sha256 as sha256

class UserController:
    @staticmethod
    def create_user(username: str, password: str) -> dict:
        """Create a new user with the given username and password."""
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
    
    @staticmethod
    def login_user(username: str, password: str) -> bool:
        """Authenticate a user by their username and password."""
        with SessionLocal() as db:
            user: User = db.query(User).filter(User.username == username).first()
            if user and sha256.verify(password, user.password_hash):
                return True
            return False
    
    @staticmethod
    def get_user(username: str) -> dict:
        """Retrieve user information by username."""
        with SessionLocal() as db:
            user = db.query(User).filter(User.username == username).first()
            if user:
                return {"username": user.username}
            return {"error": "User not found."}
