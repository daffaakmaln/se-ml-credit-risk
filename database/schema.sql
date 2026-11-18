CREATE TABLE IF NOT EXISTS applicants (
  applicant_id CHAR(5) PRIMARY KEY,
  age INT NOT NULL,
  marital_status VARCHAR(30),
  num_dependents INT DEFAULT 0,
  housing_status VARCHAR(20),
  property_ownership VARCHAR(50),
  has_registered_phone BOOLEAN DEFAULT FALSE,
  is_foreign_worker BOOLEAN DEFAULT FALSE,
  CONSTRAINT chk_applicant_id CHECK (applicant_id ~ '^A[0-9]{4}$')
);

CREATE TABLE IF NOT EXISTS employments (
  employment_id CHAR(5) PRIMARY KEY,
  applicant_id CHAR(5) UNIQUE NOT NULL REFERENCES applicants(applicant_id) ON DELETE CASCADE,
  job_type VARCHAR(50),
  employment_duration VARCHAR(30),
  CONSTRAINT chk_employment_id CHECK (employment_id ~ '^E[0-9]{4}$')
);

CREATE TABLE IF NOT EXISTS financial_profiles (
  financial_id CHAR(5) PRIMARY KEY,
  applicant_id CHAR(5) UNIQUE NOT NULL REFERENCES applicants(applicant_id) ON DELETE CASCADE,
  checking_account_status VARCHAR(30),
  savings_amount VARCHAR(30),
  credit_history VARCHAR(50),
  num_existing_credits INT DEFAULT 0,
  other_installment_plans VARCHAR(30),
  CONSTRAINT chk_financial_id CHECK (financial_id ~ '^F[0-9]{4}$')
);

CREATE TABLE IF NOT EXISTS loan_applications (
  application_id CHAR(5) PRIMARY KEY,
  applicant_id CHAR(5) NOT NULL REFERENCES applicants(applicant_id) ON DELETE CASCADE,
  loan_amount DECIMAL(15,2) NOT NULL,
  duration_months INT NOT NULL,
  purpose VARCHAR(50),
  installment_rate INT,
  guarantor VARCHAR(30),
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT chk_application_id CHECK (application_id ~ '^L[0-9]{4}$')
);

CREATE TABLE IF NOT EXISTS risk_predictions (
  prediction_id CHAR(5) PRIMARY KEY,
  application_id CHAR(5) NOT NULL REFERENCES loan_applications(application_id) ON DELETE CASCADE,
  risk_label VARCHAR(10),
  risk_score DECIMAL(5,4),
  model_version VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT chk_prediction_id CHECK (prediction_id ~ '^R[0-9]{4}$')
);

-- Untuk Supabase: tutup akses lewat API publik
ALTER TABLE applicants ENABLE ROW LEVEL SECURITY;
ALTER TABLE employments ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE loan_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE risk_predictions ENABLE ROW LEVEL SECURITY;