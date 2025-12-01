# api/dependencies.py

from fastapi import Header, HTTPException, Depends
from config import settings
import logging

logger = logging.getLogger(__name__)

def get_current_user_id(
    x_api_key: str = Header(..., alias="X-API-Key")
) -> str:
    """
    Validates a custom API key (for doctor/staff access) and returns a user identifier.
    """
    if x_api_key == settings.DOCTOR_API_KEY:
        return "doctor_admin_101"
    elif x_api_key == settings.STAFF_API_KEY:
        return "billing_staff_201"
    else:
        logger.warning("Invalid API key attempted.")
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key or credentials provided."
        )

def require_doctor_role(user_id: str = Depends(get_current_user_id)):
    """Ensures only a user with the 'doctor' ID can access the route."""
    if not user_id.startswith("doctor"):
        raise HTTPException(
            status_code=403,
            detail="Operation forbidden: Requires Doctor privileges."
        )
    return user_id