import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

# Centralized API URL configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# API_URL = "http://localhost:8000"

def analytics_month_tab():
    response = requests.get(f"{API_URL}/analytics/months")
    response = response.json()

    df= pd.DataFrame(response)
    
    st.title("Expense Breakdown By Months")
    
    st.bar_chart(data=df.set_index("Month")["Total"],
                     use_container_width=True)
     
    df['Total']= df['Total'].map("{:.2f}".format)
    st.table(df)

