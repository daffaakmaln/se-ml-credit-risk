from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, CHAR, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Applicant(Base):
    __tablename__ = "applicants"
    applicant_id = Column(CHAR(5), primary_key=True)
    age = Column(Integer, nullable=False)
    marital_status = Column(String(30))
    num_dependents = Column(Integer, default=0)
    housing_status = Column(String(20))
    property_ownership = Column(String(50))
    has_registered_phone = Column(Boolean, default=False)
    is_foreign_worker = Column(Boolean, default=False)

    employment = relationship("Employment", uselist=False, back_populates="applicant")
    financial = relationship("FinancialProfile", uselist=False, back_populates="applicant")
    loans = relationship("LoanApplication", back_populates="applicant")

class Employment(Base):
    __tablename__ = "employments"
    employment_id = Column(CHAR(5), primary_key=True)
    applicant_id = Column(CHAR(5), ForeignKey("applicants.applicant_id"), unique=True, nullable=False)
    job_type = Column(String(50))
    employment_duration = Column(String(30))

    applicant = relationship("Applicant", back_populates="employment")

class FinancialProfile(Base):
    __tablename__ = "financial_profiles"
    financial_id = Column(CHAR(5), primary_key=True)
    applicant_id = Column(CHAR(5), ForeignKey("applicants.applicant_id"), unique=True, nullable=False)
    checking_account_status = Column(String(30))
    savings_amount = Column(String(30))
    credit_history = Column(String(50))
    num_existing_credits = Column(Integer, default=0)
    other_installment_plans = Column(String(30))

    applicant = relationship("Applicant", back_populates="financial")

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    application_id = Column(CHAR(5), primary_key=True)
    applicant_id = Column(CHAR(5), ForeignKey("applicants.applicant_id"), nullable=False)
    loan_amount = Column(DECIMAL(15, 2), nullable=False)
    duration_months = Column(Integer, nullable=False)
    purpose = Column(String(50))
    installment_rate = Column(Integer)
    guarantor = Column(String(30))
    created_at = Column(DateTime, server_default=func.now())

    applicant = relationship("Applicant", back_populates="loans")
    predictions = relationship("RiskPrediction", back_populates="application")

class RiskPrediction(Base):
    __tablename__ = "risk_predictions"
    prediction_id = Column(CHAR(5), primary_key=True)
    application_id = Column(CHAR(5), ForeignKey("loan_applications.application_id"), nullable=False)
    risk_label = Column(String(10))
    risk_score = Column(DECIMAL(5, 4))
    model_version = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())

    application = relationship("LoanApplication", back_populates="predictions")