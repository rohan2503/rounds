from pydantic import BaseModel, Field, field_validator
import re

class SendOTPRequest(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15)
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v):
        # Remove spaces, dashes, plus signs
        cleaned = re.sub(r'[\s\-\+]', '', v)
        if not cleaned.isdigit():
            raise ValueError('Phone number must contain only digits')
        if len(cleaned) < 10:
            raise ValueError('Phone number must be at least 10 digits')
        return cleaned

class SendOTPResponse(BaseModel):
    success: bool
    message: str
    expires_in: int  # seconds

class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp_code: str = Field(..., min_length=6, max_length=6)

class SignUpRequest(BaseModel):
    phone_number: str
    otp_code: str = Field(..., min_length=6, max_length=6)
    full_name: str = Field(..., min_length=2, max_length=200)
    registration_number: str
    state_council: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserResponse(BaseModel):
    id: int
    phone_number: str
    full_name: str
    is_verified: bool
    registration_number: str | None
    state_council: str | None
    created_at: str