# database/crud.py

from sqlmodel import Session, select
from models.billing_schema import InvoiceRecord, InvoiceUpdate, PaymentStatus
from typing import List, Optional

def get_invoice_by_id(session: Session, invoice_id: str) -> Optional[InvoiceRecord]:
    """Reads a single invoice record by ID."""
    statement = select(InvoiceRecord).where(InvoiceRecord.invoice_id == invoice_id)
    return session.exec(statement).first()

def create_invoice_record(session: Session, invoice: InvoiceRecord) -> InvoiceRecord:
    """Creates a new invoice record in the internal database."""
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice

def update_invoice_status(session: Session, invoice_id: str, update_data: InvoiceUpdate) -> Optional[InvoiceRecord]:
    """Updates the payment status and date of an existing invoice."""
    db_invoice = get_invoice_by_id(session, invoice_id)
    if db_invoice is None:
        return None
        
    db_invoice.payment_status = update_data.payment_status
    if update_data.payment_date:
        db_invoice.payment_date = update_data.payment_date

    session.add(db_invoice)
    session.commit()
    session.refresh(db_invoice)
    return db_invoice

def get_all_invoices(session: Session) -> List[InvoiceRecord]:
    """Retrieves all invoice records for reporting purposes."""
    statement = select(InvoiceRecord).order_by(InvoiceRecord.billing_date)
    return session.exec(statement).all()