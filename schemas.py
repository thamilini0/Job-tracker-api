from typing import Optional
from pydantic import BaseModel, ConfigDict


class CompanyCreate(BaseModel):
    name: str
    website: Optional[str] = None
    location: Optional[str] = None


class CompanyOut(CompanyCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)