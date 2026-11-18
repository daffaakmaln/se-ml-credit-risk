CREATE TABLE IF NOT EXISTS roles (
  role_id CHAR(5) PRIMARY KEY,
  role_name VARCHAR(30) UNIQUE NOT NULL
);

-- ROL03 yang tadinya 'manager' otomatis jadi 'user'
INSERT INTO roles VALUES
  ('ROL01', 'admin'),
  ('ROL02', 'credit_analyst'),
  ('ROL03', 'user')
ON CONFLICT (role_id) DO UPDATE SET role_name = EXCLUDED.role_name;

CREATE TABLE IF NOT EXISTS users (
  user_id CHAR(5) PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role_id CHAR(5) NOT NULL REFERENCES roles(role_id),
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT chk_user_id CHECK (user_id ~ '^U[0-9]{4}$')
);

CREATE TABLE IF NOT EXISTS revoked_tokens (
  jti VARCHAR(64) PRIMARY KEY,
  expires_at TIMESTAMP NOT NULL
);

-- Hubungkan pemohon ke akun user
ALTER TABLE applicants
  ADD COLUMN IF NOT EXISTS user_id CHAR(5) UNIQUE REFERENCES users(user_id);

-- Status pengajuan
ALTER TABLE loan_applications
  ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'submitted';
ALTER TABLE loan_applications
  ADD CONSTRAINT chk_loan_status CHECK (status IN
  ('submitted','auto_approved','auto_rejected','pending_review','approved','rejected'));

-- Keputusan credit analyst
CREATE TABLE IF NOT EXISTS loan_reviews (
  review_id CHAR(5) PRIMARY KEY,
  application_id CHAR(5) NOT NULL UNIQUE REFERENCES loan_applications(application_id) ON DELETE CASCADE,
  analyst_id CHAR(5) NOT NULL REFERENCES users(user_id),
  decision VARCHAR(10) NOT NULL CHECK (decision IN ('approved','rejected')),
  notes TEXT,
  decided_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT chk_review_id CHECK (review_id ~ '^D[0-9]{4}$')
);

ALTER TABLE roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE revoked_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE loan_reviews ENABLE ROW LEVEL SECURITY;