# ============================================================
#  database.py — SQLite Database Setup
#  SQLAlchemy 2.0 style
# ============================================================

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime
import os

# ── Database file location ───────────────────────────────────
# Creates finguard.db in the Credit_Risk root folder
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH     = os.path.join(BASE_DIR, "finguard.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# ── Engine + Session ─────────────────────────────────────────
engine       = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ── Base class for all models ─────────────────────────────────
class Base(DeclarativeBase):
    pass

# ── Applications Table ────────────────────────────────────────
class Application(Base):
    __tablename__ = "applications"

    id                  = Column(Integer, primary_key=True, index=True)
    applicant_name      = Column(String,  default="Unknown")

    # Borrower info
    annual_income       = Column(Float)
    emp_length          = Column(Float)
    home_ownership      = Column(String)
    verification_status = Column(String)

    # Loan info
    loan_amount         = Column(Float)
    term                = Column(Integer)
    interest_rate       = Column(Float)
    installment         = Column(Float)

    # Credit info
    dti                 = Column(Float)
    fico_low            = Column(Float)
    fico_high           = Column(Float)
    open_acc            = Column(Float)
    revol_util          = Column(Float)
    pub_rec             = Column(Float)
    total_acc           = Column(Float)
    inq_last_6mths      = Column(Float)
    grade               = Column(Float)

    # Model output
    probability         = Column(Float)
    risk_tier           = Column(String)
    decision            = Column(String)

    # Timestamp
    created_at          = Column(DateTime, default=datetime.utcnow)


# ── Create tables ─────────────────────────────────────────────
def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"  Database initialized at: {DB_PATH}")


# ── Dependency for FastAPI routes ─────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
