from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.database import SessionLocal
from models.transaction import Transaction
from models.category import Category

def add_transaction(user_id: int, amount: float, description: str, category_names: list) -> dict:
    if amount <= 0:
        return {"error": "Amount must be greater than zero."}
    with SessionLocal() as db:
        try:
            categories = db.query(Category).filter(Category.name.in_(category_names)).all() if category_names else []
            transaction = Transaction(user_id=user_id, amount=amount, description=description, categories=categories)
            db.add(transaction)
            db.commit()
            return {"message": "Transaction added successfully."}
        except SQLAlchemyError as e:
            db.rollback()
            return {"error": str(e)}

def edit_transaction(transaction_id: int, amount: float = None, description: str = None, category_names: list = None) -> dict:
    with SessionLocal() as db:
        try:
            transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
            if not transaction:
                return {"error": "Transaction not found."}
            if amount:
                if amount <= 0:
                    return {"error": "Amount must be greater than zero."}
                transaction.amount = amount
            if description:
                transaction.description = description
            if category_names:
                categories = db.query(Category).filter(Category.name.in_(category_names)).all()
                transaction.categories = categories
            db.commit()
            return {"message": "Transaction updated successfully."}
        except SQLAlchemyError as e:
            db.rollback()
            return {"error": str(e)}

def delete_transaction(transaction_id: int) -> dict:
    with SessionLocal() as db:
        try:
            transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
            if not transaction:
                return {"error": "Transaction not found."}
            db.delete(transaction)
            db.commit()
            return {"message": "Transaction deleted successfully."}
        except SQLAlchemyError as e:
            db.rollback()
            return {"error": str(e)}
