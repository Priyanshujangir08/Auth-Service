from pydantic import BaseModel, EmailStr
from typing import Optional

class SignIn(BaseModel):
    email: EmailStr
    password: str

class SignUp(BaseModel):
    email: EmailStr
    password: str
    organization_name: str
    organization_settings: Optional[dict] = None
    personal: Optional[bool] = False
    profile: Optional[dict] = None
    user_settings: Optional[dict] = None


class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str

class InviteMail(BaseModel): 
    org_id: int 
    user_email: EmailStr
    role_id: int