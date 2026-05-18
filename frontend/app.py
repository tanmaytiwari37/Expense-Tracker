import streamlit as st
from add_update_ui import add_update_tab
from analytics_by_category import analytics_cat_tab
from analytics_by_month import analytics_month_tab
import subprocess
import os
import time
import sys

# Spin up the FastAPI backend in a background process if it isn't running
if not os.environ.get("FASTAPI_STARTED"):
    os.environ["FASTAPI_STARTED"] = "1"
    
    # Locates your backend server.py inside the backend directory
    backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend")
    
    print("Launching FastAPI Backend in the background...")
    subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.server:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)

st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics By Category", "Analytics By Months"])

with tab1:
    add_update_tab()

with tab2:
    analytics_cat_tab()

with tab3:
    analytics_month_tab()

# to run = streamlit run .\app.py
