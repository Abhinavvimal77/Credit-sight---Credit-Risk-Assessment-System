# ============================================================
#  routes/predict.py — /predict endpoint
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database import get_db, Application
from backend.schemas  import LoanApplication, PredictionResult
from backend.model    import predict

router = APIRouter()


@router.post("/predict", response_model=PredictionResult)
def run_prediction(app: LoanApplication, db: Session = Depends(get_db)):
    """
    Receives loan application data, runs XGBoost prediction,
    saves to database, returns result to frontend.
    """
    try:
        # ── Run model prediction ──────────────────────────────
        result = predict(app)

        # ── Save to database ──────────────────────────────────
        record = Application(
            applicant_name      = app.applicant_name,
            annual_income       = app.annual_income,
            emp_length          = app.emp_length,
            home_ownership      = app.home_ownership,
            verification_status = app.verification_status,
            loan_amount         = app.loan_amount,
            term                = app.term,
            interest_rate       = app.interest_rate,
            installment         = app.installment,
            dti                 = app.dti,
            fico_low            = app.fico_low,
            fico_high           = app.fico_high,
            open_acc            = app.open_acc,
            revol_util          = app.revol_util,
            pub_rec             = app.pub_rec,
            total_acc           = app.total_acc,
            inq_last_6mths      = app.inq_last_6mths,
            grade               = app.grade,
            probability         = result["probability"],
            risk_tier           = result["risk_tier"],
            decision            = result["decision"],
            created_at          = datetime.utcnow(),
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        # ── Return result ─────────────────────────────────────
        return PredictionResult(
            application_id      = record.id,
            applicant_name      = app.applicant_name,
            probability         = result["probability"],
            risk_tier           = result["risk_tier"],
            decision            = result["decision"],
            loan_to_income      = result["loan_to_income"],
            installment_to_inc  = result["installment_to_inc"],
            fico_avg            = result["fico_avg"],
            dti                 = result["dti"],
            revol_util          = result["revol_util"],
            interest_rate       = result["interest_rate"],
            annual_income       = result["annual_income"],
            loan_amount         = result["loan_amount"],
            created_at          = record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
