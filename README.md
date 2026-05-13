# 💰 Expense Management System

A full-stack expense tracking application with analytics, built using FastAPI, Streamlit, and MySQL.

## 🎯 Features

- ➕ Add, update, and delete daily expenses
- 📅 View expenses by specific date
- 📊 Category-wise spending breakdown with pie chart
- 📈 Monthly expense analytics with bar chart
- ✅ Auto-validation via Pydantic
- 🧪 Automated tests with pytest

## 🛠️ Tech Stack

- **Frontend:** Streamlit, Plotly, Pandas
- **Backend:** FastAPI, Pydantic, Uvicorn
- **Database:** MySQL
- **Testing:** Pytest
- **Other:** Python logging, Requests

## 📸 Screenshots

<!-- Add screenshots here -->
![Add/Update Tab](screenshots/add_update.png)
![Analytics Tab](screenshots/analytics.png)
![Monthly Analytics](screenshots/analytics_month.png)

## 📁 Project Structure

````
Expense_tracker/
├── backend/
│   ├── server.py              # FastAPI endpoints
│   ├── db_helper1.py          # MySQL operations
│   └── logging_steup.py       # Logger config
├── frontend/
│   ├── app.py                 # Streamlit main entry
│   ├── add_update_ui.py       # Add/Update tab
│   ├── analytics_ui.py        # Category analytics tab
│   └── analytics_month_ui.py  # Monthly analytics tab
├── tests/
│   ├── conftest.py
│   └── backend/
│       └── test_db_helper1.py
├── requirements.txt
└── README.md
````

## 🚀 Setup Instructions

### 1. Clone the Repository

````bash
git clone https://github.com/yourusername/expense-management-system.git
cd expense-management-system
````

### 2. Create Virtual Environment

````bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Mac/Linux
source .venv/bin/activate
````

### 3. Install Dependencies

````bash
pip install -r requirements.txt
````

### 4. Setup MySQL Database

**Option A: Quick setup using dump file (recommended)**

```bash
mysql -u root -p < database/expense_db_dump.sql
```

**Option B: Manual setup**

```sql
CREATE DATABASE expense_manager;
USE expense_manager;

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    notes TEXT
);
```

### 5. Run the FastAPI Server
````bash
cd backend
uvicorn server:app --reload
````

Backend runs on: `http://127.0.0.1:8000`
API docs: `http://127.0.0.1:8000/docs`

### 6. Run the Streamlit App

In a new terminal:

````bash
cd frontend
streamlit run app.py
```

Frontend runs on: `http://localhost:8501`

## 🧪 Running Tests

````bash
pytest -v
````

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/expenses/{date}` | Get expenses for a date |
| POST | `/expenses/{date}` | Add/update expenses for a date |
| POST | `/analytics/` | Get category breakdown for date range |
| GET | `/analytics/months` | Get monthly expense breakdown |

## 🏗️ Architecture

````
┌──────────────┐  HTTP   ┌──────────────┐  SQL   ┌──────────┐
│  Streamlit   │ ──────▶ │   FastAPI    │ ─────▶ │  MySQL   │
│  Frontend    │ ◀────── │   Backend    │ ◀───── │ Database │
│  Port 8501   │  JSON   │  Port 8000   │  Rows  │ Port 3306│
└──────────────┘         └──────────────┘        └──────────┘
````


## 👤 Author

Tanmay — [Your LinkedIn / GitHub link]

