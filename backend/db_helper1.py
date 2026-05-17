import mysql.connector
import os
from pathlib import Path
from contextlib import contextmanager
from backend.logging_steup import setup_logger
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

logger = setup_logger("db_helper1")

@contextmanager
def get_db_cursor(commit=False):
    # These os.getenv() calls pull the real values from your .env file
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_all_records():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        return cursor.fetchall()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data
    
def fetch_monthly_summary():
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
            SELECT MONTHNAME(expense_date) as Month , SUM(amount) as Total
            FROM expenses
            GROUP BY MONTHNAME(expense_date) 
            '''
        )
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    # fetch_all_records()
    # fetch_expenses_for_date("2024-08-01")
    # insert_expense("2024-08-20", 300, "Food", "Panipuri")
    # delete_expenses_for_date("2024-08-20")
    # fetch_expenses_for_date("2024-08-20")
    # summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    # print(summary)
    # summary = fetch_monthly_summary()
    # print(summary)
    pass