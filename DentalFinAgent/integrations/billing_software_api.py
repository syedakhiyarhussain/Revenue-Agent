# integrations/billing_software_api.py

import requests
import logging
from typing import Dict, Any
from config import settings
from models.billing_schema import InvoiceRecord

logger = logging.getLogger(__name__)

class BillingSoftwareAPI:
    """
    API client to push generated invoice data and sync payment status with the main billing software.
    """
    def __init__(self):
        self.base_url = settings.BILLING_SOFTWARE_URL
        self.headers = {"Content-Type": "application/json"} 

    def create_external_invoice(self, invoice: InvoiceRecord) -> Optional[str]:
        """
        Pushes a final, validated invoice to the external billing system,
        instantly starting the invoice process.
        Returns the external system's invoice reference ID on success.
        """
        endpoint = f"{self.base_url}/invoices"
        
        # Prepare data for external system (can be different from internal schema)
        payload = invoice.model_dump_json(exclude_none=True) 

        try:
            response = requests.post(endpoint, data=payload, headers=self.headers, timeout=5)
            response.raise_for_status() 

            # Assume the external system returns a reference ID
            external_ref_id = response.json().get("reference_id")
            logger.info(f"Successfully created external invoice. Ref ID: {external_ref_id}")
            return external_ref_id

        except requests.RequestException as e:
            logger.error(f"Error creating external invoice: {e}")
            return None