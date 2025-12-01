# api/endpoints.py

from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
import logging

# Import core logic and data models
from core.financial_reports import FinancialReports
from core.status_tracker import StatusTracker
from models.report_schema import MonthlyRevenueReport, AgedARReport
from models.billing_schema import InvoiceUpdate
from api.dependencies import require_doctor_role, get_current_user_id

router = APIRouter()
logger = logging.getLogger(__name__)

# Instantiate core services
reports_service = FinancialReports()
status_service = StatusTracker()


# --- Health Check ---
@router.get("/health", status_code=status.HTTP_200_OK, tags=["System"])
def health_check():
    """Confirms the API is running."""
    return {"status": "ok", "agent": "DentalFinAgent"}


# --- Financial Reporting Endpoints (Doctor Access) ---
@router.get(
    "/reports/monthly-revenue",
    response_model=MonthlyRevenueReport,
    tags=["Reports"],
    dependencies=[Depends(require_doctor_role)]
)
def get_monthly_revenue_report(user_id: str = Depends(get_current_user_id)):
    """Provides the Doctor a live view of Total Monthly Revenue."""
    report_data = reports_service.get_monthly_revenue()
    return report_data

@router.get(
    "/reports/aged-ar",
    response_model=List[AgedARReport],
    tags=["Reports"],
    dependencies=[Depends(require_doctor_role)]
)
def get_aged_ar_report(user_id: str = Depends(get_current_user_id)):
    """Provides a clear picture of all Outstanding Patient Balances (Aged A/R)."""
    report_data = reports_service.get_aged_ar()
    return report_data


# --- Invoice and Status Tracking Endpoints (Staff Access) ---
@router.put(
    "/invoices/{invoice_id}/status",
    status_code=status.HTTP_200_OK,
    tags=["Invoicing"]
)
def update_invoice_payment_status(
    invoice_id: str,
    update_data: InvoiceUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Staff manually update the Payment Status (Paid/Pending) for an invoice."""
    
    success = status_service.update_payment_status(invoice_id, update_data)
    
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    return {"message": f"Invoice {invoice_id} status updated successfully."}