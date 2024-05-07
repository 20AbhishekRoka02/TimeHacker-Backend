
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from datetime import datetime

class UserBase(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    user_name: str
    email: str
    password: str
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    # user_id: UUID = Field(default_factory=uuid4)
    user_name: str
    email: str
    password: str
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class VerifyOTP(BaseModel):
    email: str
    otp: str

class resendOTP(BaseModel):
    email: str
        
class OTPBase(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    email: str
    otp: str
    creation_time: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str

class TimeTableCreate(BaseModel):
    task_list: list
    allocated_time: list