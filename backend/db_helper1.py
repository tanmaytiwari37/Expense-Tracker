import os
from pathlib import Path
from contextlib import contextmanager
from backend.logging_steup import setup_logger
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

logger = setup_logger("db_helper1")


@contextmanager
def get_db_cursor(commit=False):
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
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
        return cursor.fetchall()


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
               FROM expenses
               WHERE expense_date BETWEEN %s AND %s
               GROUP BY category''',
            (start_date, end_date)
        )
        return cursor.fetchall()


def fetch_monthly_summary():
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT TO_CHAR(expense_date, 'Month') AS Month,
                      SUM(amount) AS Total
               FROM expenses
               GROUP BY TO_CHAR(expense_date, 'Month'),
                        EXTRACT(MONTH FROM expense_date)
               ORDER BY EXTRACT(MONTH FROM expense_date)'''
        )
        return cursor.fetchall()


def fetch_monthly_summary_by_year(year: int):
    logger.info(f"fetch_monthly_summary_by_year called for year: {year}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT TO_CHAR(expense_date, 'Month') AS Month,
                      SUM(amount) AS Total
               FROM expenses
               WHERE EXTRACT(YEAR FROM expense_date) = %s
               GROUP BY TO_CHAR(expense_date, 'Month'),
                        EXTRACT(MONTH FROM expense_date)
               ORDER BY EXTRACT(MONTH FROM expense_date)''',
            (year,)
        )
        return cursor.fetchall()


if __name__ == "__main__":
    result = fetch_all_records()
    print(result)