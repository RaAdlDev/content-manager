from pydantic import BaseModel, ConfigDict, field_validator, EmailStr
import re
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        if not re.search(r'[A-Z]', v):
            raise ValueError("password must have a capital letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("password must have a lowercase letter")
        if not re.search(r'[0-9]', v):
            raise ValueError("password must have a number")
        if not re.search(r'[@$!%*?&._-]', v):
            raise ValueError("password must have a special character")
        return v
            


class UserResponse(BaseModel):
    email: str
    is_premium: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str
    password: str