from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    currency: str = Field("EUR", min_length=3, max_length=3)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    currency: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)


class UserAdminUpdate(UserUpdate):
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserRead(UserBase):
    id: UUID
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    type: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
