# core/financial_reports.py

import logging
from typing import List
from datetime import datetime, timedelta
from database.crud import get_all_invoices
from database.db_session import get_session
from models.report_schema import MonthlyRevenueReport, AgedARReport, AgedARDetail
from models.billing_schema import InvoiceRecord, PaymentStatus

logger = logging.getLogger(__name__)

class FinancialReports:
    """
    Generates immediate, easy access to essential financial reports for doctors.
    """
    def __init__(self):
        # Dependencies are instantiated outside the loop (using get_session for DB access)
        pass

    def get_monthly_revenue(self) -> MonthlyRevenueReport:
        """Calculates Total Monthly Revenue and Net Profit (based on gross billings)."""
        session = next(get_session())
        all_invoices: List[InvoiceRecord] = get_all_invoices(session)

        # Filter for the current month (simplified)
        now = datetime.utcnow()
        current_month_invoices = [
            inv for inv in all_invoices 
            if inv.billing_date.month == now.month and inv.billing_date.year == now.year
        ]
        
        total_revenue = sum(inv.charge_amount for inv in current_month_invoices)
        total_cost = sum(inv.cost_amount for inv in current_month_invoices)
        net_profit = total_revenue - total_cost

        return MonthlyRevenueReport(
            month_year=now.strftime("%b %Y"),
            total_revenue=round(total_revenue, 2),
            total_cost=round(total_cost, 2),
            net_profit=round(net_profit, 2)
        )

    def get_aged_ar(self) -> List[AgedARReport]:
        """Calculates a clear picture of all Outstanding Patient Balances (Aged A/R)."""
        session = next(get_session())
        all_invoices: List[InvoiceRecord] = get_all_invoices(session)
        now = datetime.utcnow()
        
        outstanding_invoices = [
            inv for inv in all_invoices 
            if inv.payment_status != PaymentStatus.PAID
        ]
        
        aging_data = {
            "0-30 days": [],
            "30-60 days": [],
            "60-90 days": [],
            "90+ days": []
        }
        
        for inv in outstanding_invoices:
            days_past_due = (now - inv.billing_date).days
            detail = AgedARDetail(
                invoice_id=inv.invoice_id,
                patient_name=f"Patient_{inv.patient_id}", # Simplified name lookup
                outstanding_balance=inv.charge_amount,
                days_past_due=days_past_due
            )
            
            if days_past_due <= 30:
                aging_data["0-30 days"].append(detail)
            elif days_past_due <= 60:
                aging_data["30-60 days"].append(detail)
            elif days_past_due <= 90:
                aging_data["60-90 days"].append(detail)
            else:
                aging_data["90+ days"].append(detail)
                
        reports = []
        for bucket, details in aging_data.items():
            total = sum(d.outstanding_balance for d in details)
            reports.append(AgedARReport(
                aging_bucket=bucket,
                total_amount=round(total, 2),
                details=details
            ))
            
        return reports