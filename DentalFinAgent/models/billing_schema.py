# models/billing_schema.py

from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel # <-- ADD THIS LINE
from typing import Optional
from datetime import datetime
from enum import Enum

class PaymentStatus(str, Enum):
    """Possible states for an invoice payment."""
    PENDING = "Pending"
    PAID = "Paid"
    AGING_30 = "Aging_30"
    AGING_60 = "Aging_60"
    AGING_90_PLUS = "Aging_90+"

class InvoiceBase(SQLModel):
    """Base schema for invoice data."""
    invoice_id: Optional[str] = Field(default=None, primary_key=True)
    patient_id: str
    procedure_code: str
    charge_amount: float = Field(..., description="The amount billed to the patient/insurer.")
    cost_amount: float = Field(..., description="The internal cost of the procedure (from clinical data).")
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    billing_date: datetime = Field(default_factory=datetime.utcnow)
    
class InvoiceRecord(InvoiceBase, table=True):
    """Database model for an internally tracked invoice."""
    pass

# BaseModel is now defined and the error is fixed!
class InvoiceUpdate(BaseModel):
    """Schema for staff/API updating the payment status."""
    payment_status: PaymentStatus = Field(..., description="The new status of the payment.")
    payment_date: Optional[datetime] = None