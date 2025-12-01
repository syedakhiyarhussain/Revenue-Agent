# models/clinical_schema.py

from pydantic import BaseModel, Field
from datetime import datetime

class ClinicalProcedureData(BaseModel):
    """Data structure for a completed dental procedure captured from the clinical system."""
    patient_id: str = Field(..., description="Unique patient identifier.")
    procedure_code: str = Field(..., description="CDT or internal procedure code (e.g., D1110).")
    procedure_description: str = Field(..., description="Human-readable description of the service.")
    provider_id: str = Field(..., description="ID of the treating dentist/provider.")
    completion_date: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of when the procedure was completed.")
    internal_cost: float = Field(..., description="The calculated actual internal cost (materials, labor, overhead) of the procedure.")