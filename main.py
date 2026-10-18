from fastapi import FastAPI

app = FastAPI(title="Job Application Tracker API")


@app.get("/")
def home():
    return {"message": "Job Application Tracker API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}