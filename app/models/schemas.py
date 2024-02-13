from pydantic import BaseModel, EmailStr, UUID4, Field
from datetime import datetime
from typing import List, Optional


# User Schema
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class LeadCreate(BaseModel):
    name: str
    signal: List[int]
    number_of_samples: Optional[int] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.number_of_samples is None:
            self.number_of_samples = len(self.signal)


class ECGCreate(BaseModel):
    leads: List[LeadCreate]

    class Config:
        orm_mode = True


class LeadAnalysisSchema(BaseModel):
    num_zero_crosses: int

    class Config:
        orm_mode = True


class LeadOut(BaseModel):
    name: str
    number_of_samples: Optional[int] = None
    analysis: LeadAnalysisSchema

    class Config:
        orm_mode = True


class ECGOut(BaseModel):
    id: UUID4
    date: datetime
    processed: bool
    leads: List[LeadOut] = []

    class Config:
        orm_mode = True
