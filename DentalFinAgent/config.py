# config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables (.env file).
    """
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    # --- API & Core Settings ---
    APP_NAME: str = "DentalFinAgent"
    API_VERSION: str = "v1"
    
    # --- Database Settings (Internal Invoice Tracking) ---
    # NOTE: The format MUST be correct for SQLAlchemy to parse it. 
    DATABASE_URL: str = "sqlite:///./dentalfin_data.db" # Confirmed correct SQLite URL
    
    # --- External System Keys (Used by dependencies.py) ---
    DOCTOR_API_KEY: str = "SECURE_DENTAL_KEY_DOCTOR"  # Placeholder key for Doctor access
    STAFF_API_KEY: str = "SECURE_DENTAL_KEY_STAFF"    # Placeholder key for Staff access

    # --- Agentic AI / External Integration Keys ---
    GOOGLE_API_KEY: str = "" # Read from .env
    
    # --- Integration Endpoints ---
    CLINICAL_SYSTEM_URL: str = "http://clinical.api/v1"
    BILLING_SOFTWARE_URL: str = "http://billing.api/v1"
    CKB_DATABASE_URL: str = "http://ckb.api/v1"

# Initialize settings object
settings = Settings()