# Personal Finance Manager CLI Application
Personal Finance Manager CLI

Author
Bonventure Maeta

License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Technologies Used

Python 3.8+: 

SQLAlchemy: 

Alembic: 

Click: 

SQLite: 


How to Use the CLI

Setup and Installation

Ensure you have Python 3.8 or higher installed on your system.
Clone the repository to your local machine.
Navigate to the project directory and install the required dependencies using pipenv or pip:

pipenv install
or if you are using pip:

pip install -r requirements.txt
Running Migrations
Before using the CLI, run the database migrations to set up your database schema:


pipenv run alembic upgrade head
Using the CLI
To interact with the CLI, use the following commands:

Register a New User


pipenv run python -m views.cli_views register --username <username> --password <password>
Login a User


pipenv run python -m views.cli_views login --username <username> --password <password>
Add a New Transaction


pipenv run python -m views.cli_views add-transaction --user_id <user_id> --amount <amount> --description "<description>" --transaction_type <income/expense> --category_names "<category1(income),category2(expense)>" --date <YYYY-MM-DD>

Edit an Existing Transaction


pipenv run python -m views.cli_views edit-transaction --transaction_id <transaction_id> --amount <new_amount> --description "<new_description>" --transaction_type <income/expense> --category_names "<category1,category2>"

Delete an Existing Transaction


pipenv run python -m views.cli_views delete-transaction --transaction_id <transaction_id>
View All Transactions for a User


pipenv run python -m views.cli_views view-transactions --user_id <user_id>

Report Total Expenses for a User


pipenv run python -m views.cli_views report-expenses --user_id <user_id>

Report Total Income for a User


pipenv run python -m views.cli_views report-income --user_id <user_id>

Report Net Savings for a User


pipenv run python -m views.cli_views report-net-savings --user_id <user_id>

View Sorted Transactions for a User

pipenv run python -m views.cli_views view-sorted-transactions --user_id <user_id> --sort_by <date/amount/type> --order <asc/desc>

For detailed help on each command, you can use the --help option:


pipenv run python -m views.cli_views --help
or for specific commands:


pipenv run python -m views.cli_views <command> --help
