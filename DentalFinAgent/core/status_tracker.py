# core/status_tracker.py

import logging
from typing import Optional
from database.crud import update_invoice_status
from database.db_session import get_session
from models.billing_schema import InvoiceUpdate, InvoiceRecord

logger = logging.getLogger(__name__)

class StatusTracker:
    """
    Manages the central online spot where staff track every invoice, 
    confirm payments, and update the Payment Status.
    """
    def update_payment_status(self, invoice_id: str, update_data: InvoiceUpdate) -> bool:
        """
        Updates the payment status in the internal database.
        Returns True if successful, False if the invoice is not found.
        """
        session = next(get_session())
        
        # Use CRUD function to handle the update
        updated_invoice: Optional[InvoiceRecord] = update_invoice_status(session, invoice_id, update_data)
        
        if updated_invoice:
            logger.info(f"Payment status for invoice {invoice_id} updated to {update_data.payment_status}.")
            return True
        else:
            logger.warning(f"Attempted to update status for non-existent invoice ID: {invoice_id}")
            return False
            
    # NOTE: You could add a method here to passively sync status from the external
    # billing software periodically (Agentic AI helping staff track).