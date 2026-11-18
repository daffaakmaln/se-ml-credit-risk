from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from deps import require_roles
from ml import predict_risk, decide_status, MODEL_VERSION
from models import (Applicant, Employment, FinancialProfile, LoanApplication,
                    RiskPrediction, LoanReview)
from utils import generate_id

router = APIRouter(prefix="/loans", tags=["Loans"])

PERSONAL = ["age", "marital_status", "num_dependents", "housing_status",
            "property_ownership", "has_registered_phone", "is_foreign_worker"]
JOB = ["job_type", "employment_duration"]
FIN = ["checking_account_status", "savings_amount", "credit_history",
       "num_existing_credits", "other_installment_plans"]

class LoanIn(BaseModel):
    age: int
    marital_status: str
    num_dependents: int = 0
    housing_status: str
    property_ownership: str
    has_registered_phone: bool = False
    is_foreign_worker: bool = False
    job_type: str
    employment_duration: str
    checking_account_status: str
    savings_amount: str
    credit_history: str
    num_existing_credits: int = 0
    other_installment_plans: str
    loan_amount: float
    duration_months: int
    purpose: str
    installment_rate: int
    guarantor: str

class DecisionIn(BaseModel):
    decision: Literal["approved", "rejected"]
    notes: str | None = None

def serialize(l: LoanApplication):
    a = l.applicant
    pred = l.predictions[0] if l.predictions else None
    return {
        "application_id": l.application_id,
        "status": l.status,
        "loan_amount": float(l.loan_amount),
        "duration_months": l.duration_months,
        "purpose": l.purpose,
        "installment_rate": l.installment_rate,
        "applicant": {
            "age": a.age,
            "marital_status": a.marital_status,
            "job_type": a.employment.job_type if a.employment else None,
            "credit_history": a.financial.credit_history if a.financial else None,
        },
        "risk_score": float(pred.risk_score) if pred else None,
        "risk_label": pred.risk_label if pred else None,
        "review": {"decision": l.review.decision, "notes": l.review.notes} if l.review else None,
    }

# ---------- USER: ajukan pinjaman ----------
@router.post("", status_code=201)
def submit_loan(data: LoanIn, db: Session = Depends(get_db),
                user=Depends(require_roles("user"))):
    d = data.model_dump()

    applicant = db.query(Applicant).filter(Applicant.user_id == user.user_id).first()
    if not applicant:
        applicant = Applicant(applicant_id=generate_id(db, Applicant.applicant_id, "A"),
                              user_id=user.user_id)
        db.add(applicant)
    for f in PERSONAL:
        setattr(applicant, f, d[f])
    db.flush()

    job = applicant.employment
    if not job:
        job = Employment(employment_id=generate_id(db, Employment.employment_id, "E"),
                         applicant_id=applicant.applicant_id)
        db.add(job)
    for f in JOB:
        setattr(job, f, d[f])

    fin = applicant.financial
    if not fin:
        fin = FinancialProfile(financial_id=generate_id(db, FinancialProfile.financial_id, "F"),
                               applicant_id=applicant.applicant_id)
        db.add(fin)
    for f in FIN:
        setattr(fin, f, d[f])
    db.flush()

    loan = LoanApplication(
        application_id=generate_id(db, LoanApplication.application_id, "L"),
        applicant_id=applicant.applicant_id,
        loan_amount=d["loan_amount"], duration_months=d["duration_months"],
        purpose=d["purpose"], installment_rate=d["installment_rate"],
        guarantor=d["guarantor"], status="submitted")
    db.add(loan)
    db.flush()

    score = predict_risk(d)
    loan.status = decide_status(score)
    db.add(RiskPrediction(
        prediction_id=generate_id(db, RiskPrediction.prediction_id, "R"),
        application_id=loan.application_id,
        risk_label="bad" if score >= 0.5 else "good",
        risk_score=score, model_version=MODEL_VERSION))
    db.commit()

    return {"application_id": loan.application_id, "status": loan.status,
            "risk_score": score}

# ---------- USER: lihat pengajuan sendiri ----------
@router.get("/my")
def my_loans(db: Session = Depends(get_db), user=Depends(require_roles("user"))):
    applicant = db.query(Applicant).filter(Applicant.user_id == user.user_id).first()
    if not applicant:
        return []
    return [serialize(l) for l in applicant.loans]

# ---------- CREDIT ANALYST + ADMIN: antrean kasus 50:50 ----------
@router.get("/review-queue")
def review_queue(db: Session = Depends(get_db),
                 user=Depends(require_roles("credit_analyst", "admin"))):
    loans = db.query(LoanApplication).filter(LoanApplication.status == "pending_review").all()
    return [serialize(l) for l in loans]

# ---------- ADMIN: semua pengajuan ----------
@router.get("")
def all_loans(status: str | None = None, db: Session = Depends(get_db),
              user=Depends(require_roles("admin"))):
    q = db.query(LoanApplication)
    if status:
        q = q.filter(LoanApplication.status == status)
    return [serialize(l) for l in q.all()]

# ---------- CREDIT ANALYST: putuskan kasus 50:50 ----------
@router.post("/{application_id}/decision")
def decide(application_id: str, data: DecisionIn, db: Session = Depends(get_db),
           analyst=Depends(require_roles("credit_analyst"))):
    loan = db.get(LoanApplication, application_id)
    if not loan:
        raise HTTPException(404, "Pengajuan tidak ditemukan")
    if loan.status != "pending_review":
        raise HTTPException(400, "Pengajuan ini tidak butuh review atau sudah diputuskan")

    db.add(LoanReview(
        review_id=generate_id(db, LoanReview.review_id, "D"),
        application_id=loan.application_id,
        analyst_id=analyst.user_id,
        decision=data.decision, notes=data.notes))
    loan.status = data.decision
    db.commit()
    return {"application_id": loan.application_id, "status": loan.status}