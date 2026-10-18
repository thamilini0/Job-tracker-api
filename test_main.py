import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def fresh_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def make_company():
    response = client.post("/companies", json={"name": "Test Company"})
    return response.json()["id"]


def test_create_company():
    response = client.post("/companies", json={"name": "Test Company"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Company"


def test_create_application():
    company_id = make_company()
    response = client.post(
        "/applications",
        json={"company_id": company_id, "role_title": "Python Intern"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "applied"


def test_application_with_unknown_company_fails():
    response = client.post(
        "/applications",
        json={"company_id": 999, "role_title": "Python Intern"},
    )
    assert response.status_code == 404


def test_update_status():
    company_id = make_company()
    created = client.post(
        "/applications",
        json={"company_id": company_id, "role_title": "Python Intern"},
    ).json()
    response = client.put(
        f"/applications/{created['id']}", json={"status": "interview"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "interview"


def test_invalid_status_rejected():
    company_id = make_company()
    response = client.post(
        "/applications",
        json={
            "company_id": company_id,
            "role_title": "Python Intern",
            "status": "banana",
        },
    )
    assert response.status_code == 422


def test_stats():
    company_id = make_company()
    client.post(
        "/applications",
        json={"company_id": company_id, "role_title": "Python Intern"},
    )
    response = client.get("/stats")
    assert response.json()["applied"] == 1
    assert response.json()["total"] == 1