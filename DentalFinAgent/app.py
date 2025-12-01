import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import date, datetime

# Note on Configuration:
# For local testing, we rely on 'config.py'. For Streamlit Cloud deployment, 
# you should use os.environ to read the secrets configured in the cloud dashboard.

# --- CONFIGURATION (Reads from .env/config for local, or secrets for cloud) ---
# Check environment variables for deployment first, fall back to localhost for local dev
FASTAPI_BASE_URL = os.environ.get("FASTAPI_URL", "http://localhost:8000/api")

# Load secure keys from config/environment (necessary for accessing protected API endpoints)
try:
    from config import settings
    DOCTOR_API_KEY = settings.DOCTOR_API_KEY
    STAFF_API_KEY = settings.STAFF_API_KEY
except ImportError:
    # Fallback for deployed environments where config.py might not be available or 
    # for a simplified local run if config is bypassed.
    DOCTOR_API_KEY = os.environ.get("DOCTOR_API_KEY", "SECURE_DENTAL_KEY_DOCTOR")
    STAFF_API_KEY = os.environ.get("STAFF_API_KEY", "SECURE_DENTAL_KEY_STAFF")

DOCTOR_HEADERS = {"X-API-Key": DOCTOR_API_KEY} 
STAFF_HEADERS = {"X-API-Key": STAFF_API_KEY} 

# --- CORE FUNCTIONS (API WRAPPERS) ---

@st.cache_data(ttl=60) # Cache results for 60 seconds to avoid spamming the backend
def fetch_api_data(endpoint: str, headers: dict):
    """Generic function to fetch data from the FastAPI backend."""
    url = f"{FASTAPI_BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend API at {url}. Ensure server.py is running! Error: {e}")
        return None

def update_api_data(endpoint: str, invoice_id: str, payload: dict):
    """Generic function to update data in the FastAPI backend."""
    url = f"{FASTAPI_BASE_URL}/{endpoint}/{invoice_id}/status"
    try:
        response = requests.put(url, headers=STAFF_HEADERS, json=payload)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        st.error(f"Update failed: {e.response.json().get('detail', 'Unknown error')}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with backend: {e}")
        return None

# --- STREAMLIT UI LAYOUT ---

st.set_page_config(
    page_title="💰 DentalFin Agent Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🦷 DentalFin Agent: Revenue Cycle Control")
st.markdown("---")

# Use Streamlit's new Tab feature for a clean, multi-persona interface
tab_doctor, tab_staff = st.tabs(["🩺 Doctor's Financial Dashboard", "🧑‍💻 Staff: Payment Tracker"])


# ==============================================================================
# 1. DOCTOR'S DASHBOARD TAB
# ==============================================================================
with tab_doctor:
    st.header("Live Financial Insights")
    
    # Use st.expander for a cleaner display of authentication info
    with st.expander("Authentication Info (Doctor Access)"):
        st.code(f"X-API-Key: {DOCTOR_API_KEY}", language="text")
        st.warning("Only users with the Doctor key can load this data.")

    if st.button("Load Live Reports 🚀", key="load_reports"):
        st.session_state.monthly_revenue = fetch_api_data("reports/monthly-revenue", DOCTOR_HEADERS)
        st.session_state.aged_ar = fetch_api_data("reports/aged-ar", DOCTOR_HEADERS)

    # --- Display Monthly Revenue (KPI Metrics) ---
    if "monthly_revenue" in st.session_state and st.session_state.monthly_revenue:
        report = st.session_state.monthly_revenue
        st.subheader(f"Monthly Performance ({report['month_year']})")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Revenue (Gross)", f"${report['total_revenue']:,.2f}", delta="Instant Billing")
        with col2:
            st.metric("Total Cost", f"${report['total_cost']:,.2f}", delta="Real-time Tracking")
        with col3:
            # Displays the core profit metric, solving the "analysis gap"
            st.metric("Net Profit (Est.)", f"${report['net_profit']:,.2f}", delta="Immediate Insight", delta_color="inverse")

    # --- Display Aged A/R Report ---
    if "aged_ar" in st.session_state and st.session_state.aged_ar:
        st.subheader("Outstanding Patient Balances (Aged A/R)")

        # Convert the list of AgedARReport objects into a single, comprehensive DataFrame
        all_details = []
        for report_item in st.session_state.aged_ar:
            for detail in report_item['details']:
                detail['Aging Bucket'] = report_item['aging_bucket']
                all_details.append(detail)

            st.metric(f"Total in {report_item['aging_bucket']}", f"${report_item['total_amount']:,.2f}")
        
        if all_details:
            df = pd.DataFrame(all_details)
            # Reorder columns for better visualization
            df = df[['patient_name', 'invoice_id', 'outstanding_balance', 'days_past_due', 'Aging Bucket']]
            df.columns = ['Patient', 'Invoice ID', 'Balance ($)', 'Days Past Due', 'Aging Bucket']
            
            st.dataframe(df, use_container_width=True)
        else:
            st.success("✅ No outstanding balances found! Revenue cycle is clean.")


# ==============================================================================
# 2. STAFF TRACKER TAB
# ==============================================================================
with tab_staff:
    st.header("Central Invoice Tracking and Payment Confirmation")
    st.info("This is the 'central online spot' where staff track payments.")
    
    with st.expander("Authentication Info (Staff Access)"):
        st.code(f"X-API-Key: {STAFF_API_KEY}", language="text")

    st.subheader("Update Payment Status")
    
    col_input, col_status, col_date = st.columns(3)

    with col_input:
        invoice_id_input = st.text_input("Invoice ID to Update", help="E.g., The external reference ID from the billing system.")
    
    status_options = ["PAID", "PENDING", "AGING_30", "AGING_60", "AGING_90_PLUS"]
    with col_status:
        new_status = st.selectbox("New Payment Status", status_options)

    with col_date:
        # Use st.date_input which returns a datetime.date object
        payment_date_input = st.date_input("Payment Date (Required for PAID)", value=datetime.today().date())

    if st.button("Update Status in Central Tracker", key="update_status_btn"):
        if not invoice_id_input:
            st.error("Please enter an Invoice ID.")
        else:
            # Prepare payload for the PUT request
            payload = {
                "payment_status": new_status,
                # Convert date object to ISO format string expected by FastAPI schema
                "payment_date": payment_date_input.isoformat() if new_status == "PAID" else None
            }
            
            with st.spinner(f"Updating invoice {invoice_id_input}..."):
                response = update_api_data("invoices", invoice_id_input, payload)
                
                if response and response.status_code == 200:
                    st.success(f"✅ Success! Invoice {invoice_id_input} status updated to **{new_status}**.")
                    st.balloons()
                elif response:
                    # Specific error handling is done inside update_api_data
                    pass
                else:
                    st.error("Failed to receive a valid response from the backend.")