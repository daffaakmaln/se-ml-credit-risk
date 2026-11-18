from database import SessionLocal
from models import *
from utils import generate_id

db = SessionLocal()

a = Applicant(applicant_id=generate_id(db, Applicant.applicant_id, "A"),
              age=30, marital_status="menikah", num_dependents=2, housing_status="milik sendiri")
a.employment = Employment(employment_id="E0001", job_type="karyawan", employment_duration="3 tahun")
a.financial = FinancialProfile(financial_id="F0001", checking_account_status="ada", num_existing_credits=1)

loan = LoanApplication(application_id="L0001", loan_amount=5000000, duration_months=12,
                       purpose="motor", installment_rate=20)
a.loans.append(loan)
loan.predictions.append(RiskPrediction(prediction_id="R0001", risk_label="good",
                                       risk_score=0.12, model_version="v1"))

db.add(a)
db.commit()

print(a.loans[0].predictions[0].risk_label)  # harus tercetak: good