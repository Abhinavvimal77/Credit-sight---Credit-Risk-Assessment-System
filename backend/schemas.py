# ============================================================
#  schemas.py — Input & Output Data Shapes (Pydantic v2)
#  Validates all data coming in and going out of the API
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Input: What the frontend sends ───────────────────────────
class LoanApplication(BaseModel):
    # Applicant name (optional — for history display)
    applicant_name:      Optional[str]   = "Unknown"

    # Borrower
    annual_income:       float = Field(..., gt=0,    description="Annual income in USD")
    emp_length:          float = Field(..., ge=0,    description="Employment length in years")
    home_ownership:      str   = Field(...,           description="RENT, OWN, MORTGAGE, OTHER")
    verification_status: str   = Field(...,           description="Verified, Source Verified, Not Verified")

    # Loan
    loan_amount:         float = Field(..., gt=0,    description="Loan amount in USD")
    term:                int   = Field(...,           description="36 or 60 months")
    interest_rate:       float = Field(..., gt=0,    description="Interest rate %")
    installment:         float = Field(..., gt=0,    description="Monthly installment USD")

    # Credit
    dti:                 float = Field(..., ge=0,    description="Debt to income ratio")
    fico_low:            float = Field(...,           description="FICO range low")
    fico_high:           float = Field(...,           description="FICO range high")
    open_acc:            float = Field(..., ge=0,    description="Number of open accounts")
    revol_util:          float = Field(..., ge=0,    description="Revolving utilization %")
    pub_rec:             float = Field(..., ge=0,    description="Public records")
    total_acc:           float = Field(..., ge=0,    description="Total accounts")
    inq_last_6mths:      float = Field(..., ge=0,    description="Inquiries last 6 months")
    grade:               float = Field(...,           description="Loan grade A=1 to G=7")

    model_config = {"json_schema_extra": {
        "example": {
            "applicant_name"     : "John Smith",
            "annual_income"      : 65000,
            "emp_length"         : 5,
            "home_ownership"     : "RENT",
            "verification_status": "Verified",
            "loan_amount"        : 15000,
            "term"               : 36,
            "interest_rate"      : 12.5,
            "installment"        : 500.5,
            "dti"                : 18.5,
            "fico_low"           : 690,
            "fico_high"          : 694,
            "open_acc"           : 8,
            "revol_util"         : 45.2,
            "pub_rec"            : 0,
            "total_acc"          : 20,
            "inq_last_6mths"     : 1,
            "grade"              : 3
        }
    }}


# ── Output: What the API returns ─────────────────────────────
class PredictionResult(BaseModel):
    application_id:      int
    applicant_name:      str
    probability:         float
    risk_tier:           str
    decision:            str
    # Key ratios for UI charts
    loan_to_income:      float
    installment_to_inc:  float
    fico_avg:            float
    dti:                 float
    revol_util:          float
    interest_rate:       float
    annual_income:       float
    loan_amount:         float
    created_at:          str


# ── Application record for history page ──────────────────────
class ApplicationRecord(BaseModel):
    id:                  int
    applicant_name:      str
    loan_amount:         float
    interest_rate:       float
    probability:         float
    risk_tier:           str
    decision:            str
    created_at:          str

    model_config = {"from_attributes": True}


# ── Summary stats for history page cards ─────────────────────
class HistorySummary(BaseModel):
    total_applications:  int
    approval_rate:       float
    high_risk_pct:       float
    avg_probability:     float
