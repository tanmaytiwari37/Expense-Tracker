# 💰 Expense Management System

A full-stack expense tracking application with analytics, built using FastAPI, Streamlit, and MySQL.

## 🎯 Features

- **Dynamic Data Entry:** Add, update, and remove daily expenses seamlessly.
- **Smart Date Tracking:** Live date selection default configured to the current real date.
- **Interactive Analytics:** Category-wise spending breakdowns powered by Plotly pie charts.
- **Trend Spotting:** Monthly expense analytics utilizing aggregated bar charts.
- **Robust Architecture:** Auto-validation via Pydantic schemas and structured custom error logging.
- **Test-Driven:** Suite of automated testing configurations via pytest.


## 🛠️ Tech Stack

- **Frontend:** Streamlit, Plotly, Pandas, Requests
- **Backend:** FastAPI, Pydantic, Uvicorn
- **Database:** Managed Cloud MySQL (Aiven / Local Fallback)
- **Testing:** Pytest
- **Deployment:** Render (Unified App Container Engine)


## 📸 Screenshots

### Add/Update Tab
![Add/Update Tab](screenshots/add_update_tab.png)

### Category Analytics
![Category Analytics](screenshots/analytics_tab.png)

### Monthly Analytics
![Monthly Analytics](screenshots/monthly_analytics.png)
## 📁 Project Structure

```
Expense_tracker/
├── backend/
│   ├── server.py                 # FastAPI endpoints
│   ├── db_helper1.py             # MySQL operations
│   └── logging_steup.py          # Logger config
├── frontend/
│   ├── app.py                    # Streamlit main entry
│   ├── add_update_ui.py          # Add/Update tab
│   ├── analytics_by_category.py           # Category analytics tab
│   └── analytics_by_month.py     # Monthly analytics tab
├── tests/
│   ├── conftest.py
│   └── backend/
│       └── test_db_helper1.py
├── screenshots/                  # App screenshots for README
│   ├── add_update_tab.png
│   ├── analytics_tab.png
│   └── monthly_analytics.png
├── database/                     # SQL dump for setup
│   └── expense_db_dump.sql
├── .env.example                  # Template for environment variables
├── .gitignore                    # Files to exclude from git
├── requirements.txt              # Python dependencies
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

Frontend runs on: `http://localhost:8501`
````
#### 🧪 Running Tests

````bash
pytest -v
````
### 5. Run the Application
Instead of opening multiple terminal windows to run the backend and frontend separately, the Streamlit bootstrapper is configured to automatically spin up the FastAPI Uvicorn server in the background.

From the project root directory, simply run:

```Bash
streamlit run frontend/app.py
Interactive Frontend UI: http://localhost:8501

Automated API Documentation (FastAPI Docs): http://127.0.0.1:8000/docs
```
## ☁️ Cloud Deployment Configuration (Render + Aiven)

This application is fully production-ready and configured to deploy using a unified container architecture on **Render** paired with a managed **Aiven MySQL** cloud cluster.

### 1. Required Environment Variables
To securely decouple code from infrastructure, you must configure the following Environment Variables in your hosting platform's settings dashboard:

| Environment Variable | Description / Value |
|:---|:---|
| `DB_HOST` | Your Aiven MySQL service hostname URL |
| `DB_USER` | Database administrative username (Default: `avnadmin`) |
| `DB_PASSWORD` | Your unique generated Aiven service cleartext password |
| `DB_NAME` | The active logical database name (Default: `defaultdb`) |
| `DB_PORT` | The custom assigned cloud routing port (e.g., `24574`) |
| `API_URL` | Internal network loopback interface address: `http://127.0.0.1:8000` |

### 2. Platform Start Directive
Because the repository leverages a unified execution strategy on Render's free tier, you must point the platform's entry web service wrapper explicitly to the multi-page Streamlit controller file. 

Update the **Start Command** field in your platform settings to:
```bash
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
```
### 3. Automatic Database Initialization
* **The application contains an internal structural pipeline wrapper. When building the environment container on your host engine for the first time, tables (expenses, etc.) are securely validated against the cloud cluster target. If they are missing, the infrastructure executes your core DDL schema layouts automatically before binding local sockets.
---


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

┌────────────────────────────────────────────────────────┐
│                     RENDER CONTAINER                   │
│                                                        │
│  ┌──────────────┐     Internal Loop     ┌───────────┐  │
│  │  Streamlit   │ ────────────────────> │  FastAPI  │  │
│  │   Frontend   │ <──────────────────── │  Backend  │  │
│  │  (Port 10000)│         JSON          │(Port 8000)│  │
│  └──────────────┘                       └───────────┘  │
└───────────────────────────────────────────────│────────┘
                                                │ Secure SSL
                                                │ (Port 24574)
                                                ▼
                                          ┌───────────┐
                                          │Managed Cloud│
                                          │   MySQL   │
                                          │ (Aiven DB)│
                                          └───────────┘
````


## 👤 Author

Tanmay — [linkedin.com/in/itanmaytiwari37]

📄 License
This project is licensed under the MIT License — feel free to use, modify, and learn from it.


---

### Key Improvements Made:
1. **Accurate Execution Paths:** Updated the run instructions to reflect that running `frontend/app.py` automatically initializes the backend process wrapper, keeping local users from running into terminal binding errors.
2. **Cloud Architecture Map:** Refactored the ASCII graph layout diagram block so readers instantly grasp that Streamlit and FastAPI run inside a unified cloud container while communicating out to an external cloud database.
---

<sub>Built as part of independent study alongside coursework. 





