# core/agentic_pipeline.py

import logging
from typing import Optional
from models.clinical_schema import ClinicalProcedureData
from models.billing_schema import InvoiceRecord
from integrations.clinical_system_adapter import ClinicalSystemAdapter
from integrations.billing_software_api import BillingSoftwareAPI
from core.billing_engine import BillingEngine
from database.crud import create_invoice_record
from database.db_session import get_session

logger = logging.getLogger(__name__)
# Initialize core components
clinical_adapter = ClinicalSystemAdapter()
billing_api = BillingSoftwareAPI()
billing_engine = BillingEngine()


class AgenticPipeline:
    """
    The main Agentic AI orchestration layer. 
    It manages the lifecycle from completed procedure to final invoice creation.
    """
    def process_completed_procedure(self, case_id: str) -> Optional[InvoiceRecord]:
        """
        1. Grabs data. 2. Calculates profit. 3. Creates external and internal invoice.
        """
        logger.info(f"Agentic Pipeline triggered for case ID: {case_id}")
        
        # 1. Grab necessary Procedure and Cost data (Agentic Data Handling)
        clinical_data: Optional[ClinicalProcedureData] = clinical_adapter.fetch_procedure_data(case_id)
        if not clinical_data:
            logger.error(f"Failed to fetch or validate clinical data for case {case_id}.")
            return None
        
        # 2. Calculate final charge and actual profit (Agentic Intelligence)
        invoice_data: Optional[InvoiceRecord] = billing_engine.calculate_and_generate_invoice(clinical_data)
        if not invoice_data:
            logger.error(f"Billing Engine failed to generate invoice for case {case_id}.")
            return None
        
        # 3. Push to external billing software (Agentic Automation)
        external_ref_id = billing_api.create_external_invoice(invoice_data)
        if not external_ref_id:
            logger.error(f"Failed to send invoice to external billing software for case {case_id}.")
            # Even if external push fails, we still track it internally
        
        # Update the invoice record with the external ID
        invoice_data.invoice_id = external_ref_id if external_ref_id else f"ERR-{case_id}"

        # 4. Save to internal tracking database
        session_generator = get_session()
        session = next(session_generator) # Get the session object
        
        internal_invoice = create_invoice_record(session, invoice_data)
        
        logger.info(f"Procedure {case_id} successfully processed. Internal ID: {internal_invoice.invoice_id}")
        return internal_invoice