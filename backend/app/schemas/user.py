import uuid
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    timezone: str = "Asia/Kolkata"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    timezone: str
    prefs: dict | None = None

    model_config = {"from_attributes": True}


class FCMTokenUpdate(BaseModel):
    fcm_token: str
