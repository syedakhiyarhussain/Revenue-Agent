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

# --- CORS CONFIGURATION (CRITICAL FIX) ---
# ⚠️ ACTION REQUIRED: Replace the placeholder below with the actual public URL 
# of your deployed Streamlit app (e.g., https://my-dental-agent.streamlit.app).
origins = [
    "http://localhost:8000",
    "http://localhost:8501", 
    "https://your-streamlit-app-name.streamlit.app", # <--- UPDATE THIS LINE
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*", "X-API-Key"], # Allows your custom authentication header
)
# -----------------------------------

# Include the API routes
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """
    Event that runs when the application starts up.
    """
    logger.info(f"{settings.APP_NAME} is starting up...")


# Standard way to run the application (e.g., 'python server.py')
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
