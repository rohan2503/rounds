CREATE TABLE IF NOT EXISTS verification_attempts (
  id SERIAL PRIMARY KEY,
  user_id TEXT NOT NULL,
  registration_number TEXT NOT NULL,
  name TEXT,
  state_council TEXT,
  qualification_year INT,
  score INT,
  verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);