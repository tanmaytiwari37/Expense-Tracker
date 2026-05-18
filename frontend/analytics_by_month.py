import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# Centralized API URL configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def analytics_month_tab():
    st.title("Expense Breakdown By Months")
    
    # 1. Dynamically calculate year options from 2024 to the current year
    current_year = datetime.today().year
    year_options = list(range(2024, current_year + 1))
    
    # Year selector dropdown (Defaults to 2024)
    selected_year = st.selectbox(
        "Select Year for Comparison", 
        options=year_options, 
        index=year_options.index(2024)
    )
    
    # 2. Query your backend monthly endpoint with the selected year parameter
    try:
        response = requests.get(f"{API_URL}/analytics/months", params={"year": selected_year})
        
        if response.status_code == 200:
            data = response.json()
            
            if not data:
                st.info(f"No expense transactions logged for the year {selected_year}.")
                return
                
            df = pd.DataFrame(data)
            
            # Map columns safely based on backend response keys
            month_col = "Month" if "Month" in df.columns else df.columns[0]
            total_col = "Total" if "Total" in df.columns else df.columns[1]
            
            # Ensure numbers are treated as floats for graphing
            df[total_col] = pd.to_numeric(df[total_col])

            # 3. Render Month-over-Month Comparison Pie Chart using Plotly Express
            fig = px.pie(
                df, 
                names=month_col, 
                values=total_col, 
                title=f"Share of Annual Expenses by Month — {selected_year}",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)
             
            # 4. Display original formatted summary grid table underneath
            table_df = df.copy()
            table_df[total_col] = table_df[total_col].map("{:.2f}".format)
            st.table(table_df)
            
        else:
            st.error(f"Backend API returned an error code: {response.status_code}")
            
    except Exception as e:
        st.error(f"Could not connect to backend engine: {e}")