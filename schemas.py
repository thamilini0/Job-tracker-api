from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict

Status = Literal["applied", "interview", "offer", "rejected"]


class CompanyCreate(BaseModel):
    name: str
    website: Optional[str] = None
    location: Optional[str] = None


class CompanyOut(CompanyCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ApplicationCreate(BaseModel):
    company_id: int
    role_title: str
    applied_date: Optional[date] = None
    status: Status = "applied"
    job_link: Optional[str] = None
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    role_title: Optional[str] = None
    applied_date: Optional[date] = None
    status: Optional[Status] = None
    job_link: Optional[str] = None
    notes: Optional[str] = None


class ApplicationOut(ApplicationCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)