import streamlit as st
import subprocess
import os
import sys
import time

# 1. Force Python to recognize the current folder for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 2. Start the FastAPI backend if it isn't running
if "FASTAPI_STARTED" not in st.session_state:
    st.session_state["FASTAPI_STARTED"] = True
    
    # Move up one level to find the backend folder cleanly
    root_dir = os.path.dirname(current_dir)
    
    print("Launching background Uvicorn server...")
    subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.server:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=root_dir, # Run from the project root folder
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    # Give the FastAPI application 3 seconds to fully connect to Aiven and bind port 8000
    time.sleep(3)

# 3. Clean local imports now that sys.path is updated
from add_update_ui import add_update_tab
from analytics_by_category import analytics_cat_tab
from analytics_by_month import analytics_month_tab

# Set up the page layout
st.set_page_config(page_title="Expense Tracking System", layout="wide")
st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics By Category", "Analytics By Months"])

with tab1:
    try:
        add_update_tab()
    except Exception as e:
        st.error(f"Waiting for backend connection... Try refreshing the page in a moment. (Error: {e})")

with tab2:
    try:
        analytics_cat_tab()
    except Exception as e:
        st.warning("Could not load analytics components.")

with tab3:
    try:
        analytics_month_tab()
    except Exception as e:
        st.warning("Could not load monthly metrics.")