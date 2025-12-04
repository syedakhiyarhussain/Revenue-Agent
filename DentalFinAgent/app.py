# app.py

import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import date, datetime

# --- CONFIGURATION ---
# Base URL for the running FastAPI service
# It must read the raw host URL (NO /api) from the environment variable set in Streamlit Cloud.
FASTAPI_BASE_URL = os.environ.get("FASTAPI_URL", "http://localhost:8000") 

# Load secure keys from config/environment 
try:
    from config import settings
    DOCTOR_API_KEY = settings.DOCTOR_API_KEY
    STAFF_API_KEY = settings.STAFF_API_KEY
except ImportError:
    # Fallback for deployed environments
    DOCTOR_API_KEY = os.environ.get("DOCTOR_API_KEY", "SECURE_DENTAL_KEY_DOCTOR")
    STAFF_API_KEY = os.environ.get("STAFF_API_KEY", "SECURE_DENTAL_KEY_STAFF")

DOCTOR_HEADERS = {"X-API-Key": DOCTOR_API_KEY} 
STAFF_HEADERS = {"X-API-Key": STAFF_API_KEY} 

# --- CORE FUNCTIONS (API WRAPPERS) ---

@st.cache_data(ttl=60) # Cache results for 60 seconds to avoid spamming the backend
def fetch_api_data(endpoint: str, headers: dict):
    """Generic function to fetch data from the FastAPI backend."""
    
    # 🔑 CRITICAL: Explicitly combine the base host, the mandatory /api prefix, and the endpoint.
    url = f"{FASTAPI_BASE_URL}/api/{endpoint}" 
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend API at {url}. Ensure server.py is running! Error: {e}")
        return None

def update_api_data(endpoint: str, invoice_id: str, payload: dict):
    """Generic function to update data in the FastAPI backend."""
    # 🔑 CRITICAL: Use the corrected path structure here too.
    url = f"{FASTAPI_BASE_URL}/api/{endpoint}/{invoice_id}/status"
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

# ... (rest of the Streamlit UI code remains the same)
