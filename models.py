from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True)
    sl_no = Column(Integer)
    registration_number = Column(String(50))
    name = Column(Text)
    father_name = Column(Text)
    state_council = Column(Text)
    year_of_info = Column(Integer)
    fetched_at = Column(TIMESTAMP, server_default=func.now())

class VerificationAttempt(Base):
    __tablename__ = "verification_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))
    registration_number = Column(String(50))
    name = Column(Text)
    state_council = Column(Text)
    qualification_year = Column(Integer)
    score = Column(Integer)
    verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
