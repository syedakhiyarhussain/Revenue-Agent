# integrations/ckb_database_gateway.py

import requests
import logging
from config import settings
from models.report_schema import MonthlyRevenueReport

logger = logging.getLogger(__name__)

class CKBDatabaseGateway:
    """
    Secure gateway to push clean, final revenue numbers to the Central Knowledge Base (CKB) 
    for reliable financial records and audits.
    """
    def __init__(self):
        self.base_url = settings.CKB_DATABASE_URL
        # Secure method for CKB (e.g., token or certs)
        self.headers = {"X-CKB-Token": "ckb_secure_token_xyz"} 

    def push_final_report(self, report: MonthlyRevenueReport) -> bool:
        """
        Pushes the finalized monthly revenue report to the CKB.
        """
        endpoint = f"{self.base_url}/financial-reports"
        
        try:
            response = requests.post(endpoint, json=report.model_dump(), headers=self.headers, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Successfully pushed monthly revenue for {report.month_year} to CKB.")
            return True

        except requests.RequestException as e:
            logger.error(f"Error pushing report to CKB: {e}")
            return False