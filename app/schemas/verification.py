from pydantic import BaseModel, Field

class VerificationRequest(BaseModel):
    registration_number: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    state_council: str = Field(..., min_length=1)
    qualification_year: int = Field(..., ge=1950, le=2030)

class VerificationResponse(BaseModel):
    verified: bool
    score: int