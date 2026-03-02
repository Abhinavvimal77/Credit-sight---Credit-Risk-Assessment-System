# ============================================================
#  routes/applications.py — /applications endpoints
#  Powers the Past Applications history page
# ============================================================

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from backend.database import get_db, Application
from backend.schemas  import ApplicationRecord, HistorySummary

router = APIRouter()


@router.get("/applications", response_model=List[ApplicationRecord])
def get_applications(
    db      : Session = Depends(get_db),
    limit   : int     = Query(default=50,  ge=1, le=200),
    offset  : int     = Query(default=0,   ge=0),
    risk_tier: Optional[str] = Query(default=None),
    decision : Optional[str] = Query(default=None),
):
    """
    Returns list of past applications.
    Supports filtering by risk_tier and decision.
    Powers the history table in the frontend.
    """
    query = db.query(Application).order_by(desc(Application.created_at))

    if risk_tier:
        query = query.filter(Application.risk_tier == risk_tier.upper())
    if decision:
        query = query.filter(Application.decision == decision)

    records = query.offset(offset).limit(limit).all()

    return [
        ApplicationRecord(
            id             = r.id,
            applicant_name = r.applicant_name or "Unknown",
            loan_amount    = r.loan_amount,
            interest_rate  = r.interest_rate,
            probability    = r.probability,
            risk_tier      = r.risk_tier,
            decision       = r.decision,
            created_at     = r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        )
        for r in records
    ]


@router.get("/applications/summary", response_model=HistorySummary)
def get_summary(db: Session = Depends(get_db)):
    """
    Returns summary stats for the history page cards:
    Total apps, approval rate, high risk %, avg PD
    """
    total = db.query(Application).count()

    if total == 0:
        return HistorySummary(
            total_applications = 0,
            approval_rate      = 0.0,
            high_risk_pct      = 0.0,
            avg_probability    = 0.0,
        )

    approved   = db.query(Application).filter(Application.decision == "Approve").count()
    high_risk  = db.query(Application).filter(Application.risk_tier == "HIGH").count()
    all_probs  = db.query(Application.probability).all()
    avg_prob   = sum(p[0] for p in all_probs) / total

    return HistorySummary(
        total_applications = total,
        approval_rate      = round(approved / total * 100, 1),
        high_risk_pct      = round(high_risk / total * 100, 1),
        avg_probability    = round(avg_prob * 100, 1),
    )


@router.delete("/applications/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific application by ID.
    """
    record = db.query(Application).filter(Application.id == app_id).first()
    if not record:
        return {"message": "Application not found"}
    db.delete(record)
    db.commit()
    return {"message": f"Application {app_id} deleted"}
