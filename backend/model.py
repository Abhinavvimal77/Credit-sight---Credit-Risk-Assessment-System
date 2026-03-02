# ============================================================
#  model.py — Load XGBoost Model & Run Predictions
# ============================================================

import joblib
import json
import numpy as np
import pandas as pd
import os

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH    = os.path.join(BASE_DIR, "finguard_xgb_model.pkl")
METADATA_PATH = os.path.join(BASE_DIR, "finguard_model_metadata.json")
FEATURES_PATH = os.path.join(BASE_DIR, "finguard_features.json")

# ── Load everything once at startup ───────────────────────────
print("  Loading FinGuard model artifacts...")

xgb_model     = joblib.load(MODEL_PATH)
print(f"  Model loaded     : {MODEL_PATH}")

with open(METADATA_PATH) as f:
    metadata  = json.load(f)
print(f"  Metadata loaded  : {METADATA_PATH}")

with open(FEATURES_PATH) as f:
    feature_names = json.load(f)
print(f"  Features loaded  : {len(feature_names)} features")

THRESHOLD = metadata["threshold"]
print(f"  Threshold        : {THRESHOLD}")
print()


# ── Grade mapping (same as training) ─────────────────────────
GRADE_MAP = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7}


# ── Build feature vector from application input ───────────────
def build_feature_vector(app) -> pd.DataFrame:
    """
    Takes a LoanApplication object and builds the exact
    feature array the model was trained on.
    One-hot encodes home_ownership and verification_status.
    """

    # ── Base numeric features ─────────────────────────────────
    row = {
        "loan_amnt"       : app.loan_amount,
        "term"            : app.term,
        "int_rate"        : app.interest_rate,
        "installment"     : app.installment,
        "grade"           : app.grade,
        "emp_length"      : app.emp_length,
        "annual_inc"      : app.annual_income,
        "dti"             : app.dti,
        "fico_range_low"  : app.fico_low,
        "fico_range_high" : app.fico_high,
        "open_acc"        : app.open_acc,
        "pub_rec"         : app.pub_rec,
        "revol_util"      : app.revol_util,
        "total_acc"       : app.total_acc,
        "inq_last_6mths"  : app.inq_last_6mths,
    }

    # ── One-hot: home_ownership ───────────────────────────────
    home_options = ["MORTGAGE", "OTHER", "OWN", "RENT"]
    for opt in home_options:
        row[f"home_{opt}"] = 1.0 if app.home_ownership.upper() == opt else 0.0

    # ── One-hot: verification_status ─────────────────────────
    verif_options = ["Not Verified", "Source Verified", "Verified"]
    for opt in verif_options:
        clean = opt.replace(" ", "_")
        row[f"verification_status_{clean}"] = (
            1.0 if app.verification_status == opt else 0.0
        )

    # ── Build DataFrame with correct column order ─────────────
    df = pd.DataFrame([row])

    # Make sure all expected columns exist (fill missing with 0)
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0.0

    # Return in exact training column order
    return df[feature_names]


# ── Run prediction ────────────────────────────────────────────
def predict(app) -> dict:
    """
    Takes a LoanApplication, returns probability + tier + decision.
    """
    # Build feature vector
    X = build_feature_vector(app)

    # Get probability of default
    probability = float(xgb_model.predict_proba(X)[0][1])

    # Apply threshold → risk tier → decision
    if probability < 0.30:
        risk_tier = "LOW"
        decision  = "Approve"
    elif probability < THRESHOLD:
        risk_tier = "MEDIUM"
        decision  = "Review"
    else:
        risk_tier = "HIGH"
        decision  = "Reject"

    # Compute key ratios for UI charts
    loan_to_income     = app.loan_amount / (app.annual_income + 1)
    installment_to_inc = app.installment / (app.annual_income / 12 + 1)
    fico_avg           = (app.fico_low + app.fico_high) / 2

    return {
        "probability"       : round(probability, 4),
        "risk_tier"         : risk_tier,
        "decision"          : decision,
        "loan_to_income"    : round(loan_to_income, 4),
        "installment_to_inc": round(installment_to_inc, 4),
        "fico_avg"          : round(fico_avg, 1),
        "dti"               : app.dti,
        "revol_util"        : app.revol_util,
        "interest_rate"     : app.interest_rate,
        "annual_income"     : app.annual_income,
        "loan_amount"       : app.loan_amount,
    }
