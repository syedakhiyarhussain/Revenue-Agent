# models/report_schema.py

from pydantic import BaseModel, Field # <-- ENSURE Field IS HERE
from typing import List

class MonthlyRevenueReport(BaseModel):
    """Summary of total revenue and profit for the current month."""
    month_year: str = Field(..., description="The month and year of the report (e.g., Nov 2025).")
    total_revenue: float = Field(..., description="Total gross billings for the month.")
    total_cost: float = Field(..., description="Total calculated internal costs for the month.")
    net_profit: float = Field(..., description="Total Revenue minus Total Cost.")
    
class AgedARDetail(BaseModel):
    """Detail for a single outstanding balance."""
    invoice_id: str
    patient_name: str
    outstanding_balance: float
    days_past_due: int

class AgedARReport(BaseModel):
    """Summary of outstanding patient balances grouped by aging period."""
    aging_bucket: str = Field(..., description="Aging period (e.g., 30-60 days).")
    total_amount: float = Field(..., description="Total dollar amount in this bucket.")
    details: List[AgedARDetail]