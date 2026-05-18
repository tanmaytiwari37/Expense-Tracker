import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from calendar import month_name, monthrange
from datetime import datetime

# Centralized API URL configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def analytics_month_tab():
    st.title("Monthly Expense Breakdown by Category")
    
    # 1. Selection inputs for Year and Month
    current_year = datetime.today().year
    current_month = datetime.today().month
    
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox(
            "Select Year", 
            options=[current_year, current_year - 1, current_year - 2], 
            index=0
        )
        
    with col2:
        # Generates a clean list of months: ["Select Month", "January", "February", ...]
        month_options = list(month_name)[1:] 
        selected_month_name = st.selectbox(
            "Select Month", 
            options=month_options, 
            index=current_month - 1  # Defaults to the current active month
        )

    # 2. Calculate the exact start and end dates under the hood
    month_index = month_options.index(selected_month_name) + 1
    # monthrange returns (first_day_weekday, number_of_days_in_month)
    _, total_days = monthrange(selected_year, month_index)
    
    start_date = f"{selected_year}-{month_index:02d}-01"
    end_date = f"{selected_year}-{month_index:02d}-{total_days:02d}"

    # 3. Request category data for this specific month range
    # Reusing your backend's range-based endpoint: POST /analytics/
    try:
        payload = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        response = requests.post(f"{API_URL}/analytics/", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            if not data:
                st.info(f"No transactions found for {selected_month_name} {selected_year}.")
                return
                
            df = pd.DataFrame(data)
            
            # Ensure your backend response columns match (e.g., 'category' and 'total_amount')
            # Adjust these string keys if your API returns different casing like 'Category' / 'Total'
            category_col = "category" if "category" in df.columns else df.columns[0]
            amount_col = "total_amount" if "total_amount" in df.columns else df.columns[1]

            # 4. Render the beautiful interactive Plotly Pie Chart
            fig = px.pie(
                df, 
                names=category_col, 
                values=amount_col, 
                title=f"Spending Structure — {selected_month_name} {selected_year}",
                hole=0.3  # Creates a modern donut-style look
            )
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)
             
            # Display formatted data table underneath
            df[amount_col] = df[amount_col].map("{:.2f}".format)
            st.table(df)
            
        else:
            st.error(f"Backend API error: {response.status_code}")
            
    except Exception as e:
        st.error(f"Could not connect to backend engine: {e}")