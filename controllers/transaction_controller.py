from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.database import SessionLocal
from models.transaction import Transaction
from models.category import Category

class TransactionController:

    @staticmethod
    def add_transaction(user_id: int, amount: float, description: str, transaction_type: str, category_names: list) -> dict:
        with SessionLocal() as db:
            try:
                # Ensure amount is positive
                if amount <= 0:
                    return {"error": "Amount must be greater than zero."}

                # Resolve categories, creating them if necessary
                categories = []
                for name in category_names:
                    category = db.query(Category).filter_by(name=name).first()
                    if not category:
                        category = Category(name=name)
                        db.add(category)
                        db.flush()  # Flush here to ensure category is persisted before adding to transaction
                    categories.append(category)

                transaction = Transaction(
                    user_id=user_id,
                    amount=amount,
                    description=description,
                    transaction_type=transaction_type,
                    categories=categories
                )
                db.add(transaction)
                db.commit()
                return {"message": "Transaction added successfully."}
            except SQLAlchemyError as e:
                db.rollback()
                return {"error": f"Failed to add transaction: {e}"}

    @staticmethod
    def edit_transaction(transaction_id: int, amount: float = None, description: str = None, category_names: list = None) -> dict:
        with SessionLocal() as db:
            try:
                transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
                if not transaction:
                    return {"error": "Transaction not found."}

                if amount is not None:
                    if amount <= 0:
                        return {"error": "Amount must be greater than zero."}
                    transaction.amount = amount
                
                if description is not None:
                    transaction.description = description

                if category_names is not None:
                    categories = db.query(Category).filter(Category.name.in_(category_names)).all()
                    transaction.categories = categories

                db.commit()
                return {"message": "Transaction updated successfully."}
            except SQLAlchemyError as e:
                db.rollback()
                return {"error": f"Failed to edit transaction: {e}"}

    @staticmethod
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
                return {"error": f"Failed to delete transaction: {e}"}

    @staticmethod
    def view_transactions(user_id: int):
        with SessionLocal() as db:
            transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
            return transactions if transactions else {"error": "No transactions found."}

    @staticmethod
    def report_expenses(user_id: int):
        with SessionLocal() as db:
            total_expenses = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == user_id, Transaction.transaction_type == 'expense').scalar() or 0
            return total_expenses

    @staticmethod
    def report_income(user_id: int):
        with SessionLocal() as db:
            total_income = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == user_id, Transaction.transaction_type == 'income').scalar() or 0
            return total_income

    @staticmethod
    def report_net_savings(user_id: int):
        with SessionLocal() as db:
            income = TransactionController.report_income(user_id)
            expenses = TransactionController.report_expenses(user_id)
            net_savings = income - expenses
            return net_savings
