# main.py

from fastapi import FastAPI
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

# Include the API routes
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """
    Event that runs when the application starts up.
    Can be used to check database connection, initialize integrations, etc.
    """
    logger.info(f"{settings.APP_NAME} is starting up...")


# Standard way to run the application (e.g., 'python main.py')
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)