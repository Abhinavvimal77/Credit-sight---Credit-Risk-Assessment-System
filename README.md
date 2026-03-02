# credit sight — AI Credit Risk Assessment System

> An end-to-end machine learning system that predicts loan default probability, classifies applicants into risk tiers, and recommends credit decisions through a professional dark-themed web dashboard.

---

## 🚀 Live Demo

| Layer | URL |
|---|---|
| Frontend | Coming soon — Netlify |
| Backend API | Coming soon — Render |
| API Docs | Coming soon — /docs |

---

## 📸 Preview

> Dark enterprise UI with real-time XGBoost predictions, radar charts, FICO gauge, and full application history.

---

## 🧠 What It Does

- Takes a loan application as input — income, FICO score, DTI, loan amount, employment, etc.
- Runs it through a trained **XGBoost model** to predict probability of default
- Classifies the applicant into **LOW / MEDIUM / HIGH** risk tier
- Recommends **Approve / Review / Reject**
- Saves every assessment to a **SQLite database**
- Displays results with animated charts and gauges in a web dashboard
- Shows full application history with search and filter

---

## 🏗️ System Architecture

```
User fills form (Frontend HTML)
        ↓
POST /predict  (FastAPI Backend)
        ↓
Pydantic validates input
        ↓
Build 21-feature vector (model.py)
        ↓
XGBoost predict_proba() → 0.0 to 1.0
        ↓
Apply threshold (0.55) → Risk tier
        ↓
Save to SQLite (SQLAlchemy)
        ↓
Return JSON → { probability, risk_tier, decision }
        ↓
Frontend updates charts, gauges, badges
```

---

## 🔧 Tech Stack

| Layer | Technology | Version |
|---|---|---|
| ML Model | XGBoost | 3.2.0 |
| Data Processing | Pandas / NumPy | 2.3 / 2.2 |
| Backend API | FastAPI | 0.134.0 |
| API Server | Uvicorn | 0.41.0 |
| Database ORM | SQLAlchemy | 2.0.47 |
| Database | SQLite | Built-in |
| Data Validation | Pydantic | 2.12.5 |
| Model Persistence | Joblib | 1.5.1 |
| Frontend | HTML / CSS / JS | Vanilla |
| Language | Python | 3.13.3 |

---

## 📁 Project Structure

```
finguard-credit-risk/
│
├── main.py                          # FastAPI app entry point
├── requirements.txt                 # Python dependencies
│
├── backend/
│   ├── model.py                     # Load model, run predictions
│   ├── database.py                  # SQLite setup via SQLAlchemy
│   ├── schemas.py                   # Pydantic input/output models
│   └── routes/
│       ├── predict.py               # POST /predict endpoint
│       └── applications.py          # GET /applications endpoints
│
├── creditsight-v3.html              # Full frontend UI
│
├── finguard_xgb_model.pkl           # Trained XGBoost model
├── finguard_scaler.pkl              # Fitted StandardScaler
├── finguard_lr_model.pkl            # Logistic Regression backup
├── finguard_features.json           # Feature names and order
├── finguard_model_metadata.json     # Threshold, tiers, metrics
│
├── ml/
│   ├── Cleaning_&_EDA.ipynb         # Phase 1 — data cleaning
│   ├── Training_&_Evaluation.ipynb  # Phase 2 — model training
│   └── credit_risk_clean.csv        # Cleaned dataset
│
└── FinGuard_Project_Documentation.docx  # Full project documentation
```

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| Algorithm | XGBoost Classifier |
| AUC Score | **0.742** |
| Accuracy | 71.9% |
| Recall (Default) | 59.4% |
| Precision (Default) | 38.5% |
| F1 Score (Default) | 0.467 |
| Cross-Val AUC | 0.742 ± 0.005 |
| Prediction Threshold | 0.55 |
| Training Records | 297,708 |
| Test Records | 74,428 |

---

## 🚦 Risk Tier Logic

| Probability of Default | Risk Tier | Decision |
|---|---|---|
| 0% — 29.99% | 🟢 LOW | Approve |
| 30% — 54.99% | 🟡 MEDIUM | Manual Review |
| 55% and above | 🔴 HIGH | Reject |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/predict` | Run XGBoost prediction + save to DB |
| GET | `/applications` | Fetch all past applications |
| GET | `/applications/summary` | Summary stats for history page |
| DELETE | `/applications/{id}` | Delete an application |
| GET | `/health` | Health check |
| GET | `/docs` | Auto-generated API documentation |

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/finguard-credit-risk.git
cd finguard-credit-risk
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the backend server

```bash
python -m uvicorn main:app --reload
```

### 4. Open the frontend

Open `creditsight-v3.html` directly in your browser.

### 5. Verify everything works

- Visit `http://localhost:8000/health` — should return `{"status":"running"}`
- Visit `http://localhost:8000/docs` — see all API endpoints
- Fill the form and click **Run Assessment**

---

## 🧪 Sample Test Data — Low Risk (Approve)

```json
{
  "applicant_name": "John Smith",
  "annual_income": 150000,
  "emp_length": 10,
  "home_ownership": "OWN",
  "verification_status": "Verified",
  "loan_amount": 10000,
  "term": 36,
  "interest_rate": 7.5,
  "installment": 310,
  "dti": 8,
  "fico_low": 780,
  "fico_high": 784,
  "open_acc": 6,
  "revol_util": 10,
  "pub_rec": 0,
  "total_acc": 25,
  "inq_last_6mths": 0,
  "grade": 1
}
```

---

## 🗄️ Database

SQLite database (`finguard.db`) is created automatically on first server startup. Every prediction is saved permanently with full application details, model output, risk tier, decision, and timestamp.

**Applications table stores:**
- All 17 input features
- Probability of default
- Risk tier and decision
- Timestamp

---

## 🤖 Model Development Journey

| Cell | Approach | AUC | Result |
|---|---|---|---|
| Cell 1 | Logistic Regression + threshold tuning | 0.735 | Baseline |
| Cell 2 | Random Forest + comparison | 0.729 | Worse than LR |
| Cell 3 | XGBoost — first run | **0.742** | Best model ✅ |
| Cell 4 | XGBoost + SMOTE oversampling | 0.740 | No improvement |
| Cell 5 | XGBoost + 11 engineered features | 0.742 | Confirmed ceiling |
| Cell 6 | 5-fold cross-validation + model saving | 0.742 ± 0.005 | Finalized ✅ |

---

## 🔑 Top Feature Importances

| Rank | Feature | Importance | Description |
|---|---|---|---|
| 1 | grade | 44.1% | LendingClub risk grade (A–G) |
| 2 | term | 22.7% | 36 vs 60 month loan term |
| 3 | int_rate | 14.3% | Interest rate assigned |
| 4 | home_RENT | 3.4% | Home ownership — RENT |
| 5 | fico_range_high | 1.6% | FICO score upper bound |

---

## 🌍 Deployment Plan (Free)

| Layer | Service | Cost |
|---|---|---|
| Frontend | Netlify | Free forever |
| Backend | Render | Free tier |
| Database | Supabase (PostgreSQL) | Free 500MB |
| Keep-alive | UptimeRobot | Free |

> UptimeRobot pings the Render server every 10 minutes to prevent sleep.

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 👤 Author

**Abhinav M**
- Built as an end-to-end ML + backend + frontend project
- Dataset: LendingClub Loan Data (~372,000 records)
- Model: XGBoost with AUC 0.742

---

*Credit sight v1.0 — ML Model + FastAPI Backend + SQLite Database + Vanilla JS Frontend*
