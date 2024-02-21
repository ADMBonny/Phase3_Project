
from sqlalchemy.exc import SQLAlchemyError

import click
from controllers.user_controller import UserController
from controllers.transaction_controller import TransactionController
from sqlalchemy import desc, asc
from datetime import datetime
from models.database import SessionLocal
from models.transaction import Transaction
from models.database import init_db

# Initialize the database
init_db()

@click.group()
def cli():
    """Personal Finance Manager CLI"""
    pass

@cli.command(help="Register a new user")
@click.option('--username', prompt=True, help="Username for the new account")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="Password for the new account")
def register(username, password):
    response = UserController.create_user(username, password)
    click.echo(response.get("message") or response.get("error"))

@cli.command(help="Login a user")
@click.option('--username', prompt=True, help="Your username")
@click.option('--password', prompt=True, hide_input=True, help="Your password")
def login(username, password):
    """Handle user login"""
    if UserController.login_user(username, password):
        click.echo("Login successful.")
    else:
        click.echo("Login failed. Please check your username and password.")


@click.command(help="Add a new transaction")
@click.option('--user_id', type=int, prompt=True, help="Your user ID")
@click.option('--amount', type=float, prompt=True, help="Transaction amount")
@click.option('--description', prompt=True, default='', help="Description of the transaction")
@click.option('--transaction_type', prompt=True, type=click.Choice(['income', 'expense'], case_sensitive=False), help="Type of the transaction")
@click.option('--category_names', prompt=True, help="Comma-separated category names")
@click.option('--date', prompt=True, help="Transaction date in YYYY-MM-DD format", default=str(datetime.now().date()))
def add_transaction(user_id, amount, description, transaction_type, category_names, date):
    
    transaction_date = datetime.strptime(date, "%Y-%m-%d").date()
    category_list = category_names.split(',')
    response = TransactionController.add_transaction(user_id, amount, description, transaction_type, category_list, transaction_date)
    click.echo(response.get("message") or response.get("error"))
    
cli.add_command(add_transaction)  


@cli.command(help="Edit an existing transaction")
@click.option('--transaction_id', type=int, prompt=True, help="ID of the transaction to edit")
@click.option('--amount', type=float, help="New amount for the transaction")
@click.option('--description', help="New description of the transaction")
@click.option('--transaction_type', help="Type of the transaction (income or expense)")
@click.option('--category_names', help="Comma-separated new category names")
def edit_transaction(transaction_id, amount, description, transaction_type, category_names):
    category_list = category_names.split(',') if category_names else None
    response = TransactionController.edit_transaction(transaction_id, amount, description, transaction_type, category_list)
    click.echo(response.get("message") or response.get("error"))

@cli.command(help="Delete an existing transaction")
@click.option('--transaction_id', type=int, prompt=True, help="ID of the transaction to delete")
def delete_transaction(transaction_id):
    response = TransactionController.delete_transaction(transaction_id)
    click.echo(response.get("message") or response.get("error"))

@cli.command(help="View all transactions for a user")
@click.option('--user_id', type=int, prompt=True, help="User ID to view transactions for")
def view_transactions(user_id):
    transactions = TransactionController.view_transactions(user_id)
    if isinstance(transactions, str):
        click.echo(transactions)
    else:
        for transaction in transactions:
            click.echo(f"ID: {transaction.id}, Amount: {transaction.amount}, Description: {transaction.description}, Type: {transaction.transaction_type}")

@cli.command(help="Report total expenses for a user")
@click.option('--user_id', type=int, prompt=True, help="User ID to calculate expenses for")
def report_expenses(user_id):
    expenses = TransactionController.report_expenses(user_id)
    click.echo(f"Total Expenses: {expenses}")

@cli.command(help="Report total income for a user")
@click.option('--user_id', type=int, prompt=True, help="User ID to calculate income for")
def report_income(user_id):
    income = TransactionController.report_income(user_id)
    click.echo(f"Total income for user {user_id}: {income}")

@cli.command(help="Report net savings for a user")
@click.option('--user_id', type=int, prompt=True, help="User ID to calculate net savings for")
def report_net_savings(user_id):
    net_savings = TransactionController.report_net_savings(user_id)
    click.echo(f"Net savings for user {user_id}: {net_savings}")




@click.command('view-sorted-transactions', help="View transactions sorted by a specified field")
@click.option('--user_id', required=True, type=int, help="User ID to view transactions for")
@click.option('--sort_by', type=click.Choice(['date', 'amount', 'type'], case_sensitive=False), default='date', help="Sort transactions by this field")
@click.option('--order', type=click.Choice(['asc', 'desc'], case_sensitive=False), default='asc', help="Order of sorting (ascending or descending)")
def view_sorted_transactions(user_id, sort_by, order):
    """View transactions sorted by date, amount, or type."""
    with SessionLocal() as db:
        query = db.query(Transaction).filter(Transaction.user_id == user_id)
        
        if sort_by == 'date':
            query = query.order_by(asc(Transaction.date) if order == 'asc' else desc(Transaction.date))
        elif sort_by == 'amount':
            query = query.order_by(asc(Transaction.amount) if order == 'asc' else desc(Transaction.amount))
        elif sort_by == 'type':
            query = query.order_by(asc(Transaction.transaction_type) if order == 'asc' else desc(Transaction.transaction_type))
        
        transactions = query.all()
        
        for transaction in transactions:
            click.echo(f"ID: {transaction.id}, Amount: {transaction.amount}, Type: {transaction.transaction_type}, Date: {transaction.date}, Description: {transaction.description}")

cli.add_command(view_sorted_transactions)
if __name__ == '__main__':
    cli()


