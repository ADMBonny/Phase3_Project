from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.transaction import Transaction
from models.category import Category

def add_transaction(user_id: int, amount: float, description: str, category_names: list) -> Transaction:
    db: Session = SessionLocal()
    categories = db.query(Category).filter(Category.name.in_(category_names)).all()
    transaction = Transaction(user_id=user_id, amount=amount, description=description, categories=categories)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.close()
    return transaction

def edit_transaction(transaction_id: int, amount: float = None, description: str = None, category_names: list = None):
    db: Session = SessionLocal()
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        if amount:
            transaction.amount = amount
        if description:
            transaction.description = description
        if category_names:
            categories = db.query(Category).filter(Category.name.in_(category_names)).all()
            transaction.categories = categories
        db.commit()
    db.close()

def delete_transaction(transaction_id: int):
    db: Session = SessionLocal()
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        db.delete(transaction)
        db.commit()
    db.close()
