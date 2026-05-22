from fastapi import FastAPI, HTTPException
from datetime import date
from backend import db_helper1
from typing import List
from pydantic import BaseModel

app = FastAPI()


class Expense(BaseModel):
    amount: float
    category: str
    notes: str


class DateRange(BaseModel):
    start_date: date
    end_date: date


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper1.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")

    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses:List[Expense]):
    db_helper1.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper1.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {"message": "Expenses updated successfully"}


@app.post("/analytics/")
def get_analytics_category(date_range: DateRange):
    data = db_helper1.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")

    total = sum([float(row['total']) for row in data])  # ← add float()

    breakdown = {}
    for row in data:
        percentage = (float(row['total']) / total) * 100 if total != 0 else 0  # ← add float()
        breakdown[row['category']] = {
            "total": float(row['total']),        # ← add float()
            "percentage": percentage
        }

    return breakdown

from fastapi import HTTPException

@app.get("/analytics/months")
def get_analytics_month(year: int = 2024):
    data = db_helper1.fetch_monthly_summary_by_year(year)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")
    return data

# to run: uvicorn server:app --reload