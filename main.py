from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
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


# ---------- Companies ----------

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


# ---------- Applications ----------

@app.post("/applications", response_model=schemas.ApplicationOut)
def create_application(
    application: schemas.ApplicationCreate, db: Session = Depends(get_db)
):
    company = db.get(models.Company, application.company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    db_application = models.Application(**application.model_dump())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


@app.get("/applications", response_model=list[schemas.ApplicationOut])
def list_applications(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Application)
    if status:
        query = query.filter(models.Application.status == status)
    return query.all()


@app.get("/applications/{application_id}", response_model=schemas.ApplicationOut)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.get(models.Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@app.put("/applications/{application_id}", response_model=schemas.ApplicationOut)
def update_application(
    application_id: int,
    updates: schemas.ApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = db.get(models.Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application


@app.delete("/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = db.get(models.Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()
    return {"message": "Application deleted"}