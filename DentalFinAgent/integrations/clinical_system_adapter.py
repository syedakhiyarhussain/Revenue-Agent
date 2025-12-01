# integrations/clinical_system_adapter.py

import requests
import logging
from typing import Optional
from config import settings
from models.clinical_schema import ClinicalProcedureData

logger = logging.getLogger(__name__)

class ClinicalSystemAdapter:
    """
    Adapter to securely communicate with the external clinical system.
    This fetches the cost and procedure details.
    """
    def __init__(self):
        self.base_url = settings.CLINICAL_SYSTEM_URL
        # Assume an API key or token is needed for access
        self.headers = {"Authorization": "Bearer clinical_token_abc"} 

    def fetch_procedure_data(self, case_id: str) -> Optional[ClinicalProcedureData]:
        """
        Simulates grabbing necessary Procedure and Cost data as soon as a case is done.
        """
        endpoint = f"{self.base_url}/procedures/{case_id}"
        
        try:
            # In a real scenario, the response data would need careful validation
            response = requests.get(endpoint, headers=self.headers, timeout=5)
            response.raise_for_status() # Raise exception for bad status codes
            
            data = response.json()
            # Validate and convert the received data into our internal schema
            return ClinicalProcedureData(**data)
            
        except requests.RequestException as e:
            logger.error(f"Error fetching data from clinical system for case {case_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing clinical data: {e}")
            return None