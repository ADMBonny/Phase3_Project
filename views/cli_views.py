import click
from controllers.user_controller import UserController
from controllers.transaction_controller import TransactionController
from models.database import init_db
from sqlalchemy.exc import SQLAlchemyErrors

init_db()


# Initialize Click group for organizing CLI commands
@click.group()
def cli():
    """Personal Finance Manager CLI"""
    pass

@cli.command(help="Register a new user")
@click.option('--username', prompt=True, help="Username for the new account")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="Password for the new account")
def register(username, password):
    """Handles user registration"""
    UserController.create_user(username, password)

@cli.command(help="Login a user")
@click.option('--username', prompt=True, help="Your username")
@click.option('--password', prompt=True, hide_input=True, help="Your password")
def login(username, password):
    """Handles user login"""
    UserController.login_user(username, password)

@cli.command(help="Add a new transaction")
@click.option('--amount', type=float, prompt=True, help="Transaction amount")
@click.option('--description', default='', help="Description of the transaction")
@click.option('--category', default='', help="Category of the transaction")
def add_transaction(amount, description, category):
    """Adds a new transaction for the logged-in user"""
    TransactionController.add_transaction(amount, description, category)


@cli.command(help="Edit an existing transaction")
@click.option('--transaction_id', type=int, prompt=True, help="ID of the transaction to edit")
@click.option('--amount', type=float, help="New amount for the transaction")
@click.option('--description', help="New description of the transaction")
@click.option('--category', help="New category of the transaction")
def edit_transaction(transaction_id, amount, description, category):
    """Edits an existing transaction"""
    TransactionController.edit_transaction(transaction_id, amount, description, category)
    click.echo(f"Transaction {transaction_id} has been updated.")

@cli.command(help="Delete an existing transaction")
@click.option('--transaction_id', type=int, prompt=True, help="ID of the transaction to delete")
def delete_transaction(transaction_id):
    """Deletes an existing transaction"""
    TransactionController.delete_transaction(transaction_id)
    click.echo(f"Transaction {transaction_id} has been deleted.")

@cli.command(help="View all transactions")
@click.option('--user_id', type=int, prompt=True, help="User ID to view transactions for")
def view_transactions(user_id):
    """Views all transactions for a user"""
    transactions = TransactionController.view_transactions(user_id)
    for transaction in transactions:
        click.echo(f"ID: {transaction.id}, Amount: {transaction.amount}, Description: {transaction.description}, Category: {transaction.category}")


if __name__ == '__main__':
    cli()
