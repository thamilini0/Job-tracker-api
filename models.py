from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    website = Column(String, nullable=True)
    location = Column(String, nullable=True)

    applications = relationship("Application", back_populates="company")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role_title = Column(String, nullable=False)
    applied_date = Column(Date, nullable=True)
    status = Column(String, default="applied")
    job_link = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    company = relationship("Company", back_populates="applications")