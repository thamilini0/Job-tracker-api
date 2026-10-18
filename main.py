from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker API")


@app.get("/")
def home():
    return {"message": "Job Application Tracker API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/companies", response_model=schemas.CompanyOut)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = models.Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@app.get("/companies", response_model=list[schemas.CompanyOut])
def list_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()