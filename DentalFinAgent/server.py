# server.py (Add the CORS configuration)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <-- NEW IMPORT
import uvicorn
import logging

# Import configuration and endpoints
from config import settings
from api.endpoints import router as api_router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="Intelligent Agent for Dental Billing & Financial Analysis."
)

# --- CORS CONFIGURATION (THE FIX) ---
# ⚠️ IMPORTANT: Replace 'https://your-streamlit-app-name.streamlit.app' 
# with the actual public domain of your Streamlit Cloud app.
# Use [] when running locally to allow all origins
origins = [
    "http://localhost:8000",
    "http://localhost:8501", # Streamlit local dev port
    "https://your-streamlit-app-name.streamlit.app", # <-- YOUR DEPLOYED STREAMLIT URL
    # Add any other deployment URLs here (e.g., Render preview URLs)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, PUT, DELETE
    allow_headers=["*", "X-API-Key"], # Allows all headers, including your custom API key header
)
# -----------------------------------

# Include the API routes
app.include_router(api_router, prefix="/api")

# ... (rest of server.py remains the same)
