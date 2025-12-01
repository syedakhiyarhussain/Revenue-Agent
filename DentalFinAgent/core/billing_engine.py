# core/billing_engine.py

import logging
from typing import Optional
from models.clinical_schema import ClinicalProcedureData
from models.billing_schema import InvoiceRecord

logger = logging.getLogger(__name__)

# --- Mock Data for Demonstration ---
# In a real app, this would come from a fee schedule database lookup
FEE_SCHEDULE = {
    "D1110": 120.00,  # Prophylaxis
    "D2740": 950.00,  # Crown - PFM
    "D0120": 65.00    # Periodic oral evaluation
}

class BillingEngine:
    """
    Calculates the billed charge, cost, and immediate profit for a procedure.
    """
    def get_procedure_charge(self, procedure_code: str) -> float:
        """Looks up the standard billed charge based on the procedure code."""
        # Simple lookup; real-world logic includes insurer/plan specifics
        return FEE_SCHEDULE.get(procedure_code, 0.0)

    def calculate_and_generate_invoice(self, clinical_data: ClinicalProcedureData) -> Optional[InvoiceRecord]:
        """
        Calculates the final billed amount and creates the internal invoice record.
        """
        billed_charge = self.get_procedure_charge(clinical_data.procedure_code)
        
        if billed_charge == 0.0:
            logger.error(f"Cannot bill procedure {clinical_data.procedure_code}: charge is zero.")
            return None
            
        # The key feature: Instantly calculate profit (Revenue - Cost)
        # Note: Actual profit realization depends on payment, but this is the 'quick profit' view.
        profit_estimate = billed_charge - clinical_data.internal_cost
        
        logger.info(f"Calculated Charge: {billed_charge}, Cost: {clinical_data.internal_cost}, Profit: {profit_estimate:.2f}")

        # Create the internal invoice record (InvoiceRecord is a SQLModel table)
        invoice = InvoiceRecord(
            patient_id=clinical_data.patient_id,
            procedure_code=clinical_data.procedure_code,
            charge_amount=billed_charge,
            cost_amount=clinical_data.internal_cost,
        )
        return invoice