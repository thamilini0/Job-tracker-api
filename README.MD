# Job Application Tracker API

A REST API to track job applications, built with FastAPI and SQLite.
I built it to practise backend development and to keep track of my own job search.

## Features
- Add and list companies
- Add, view, update and delete job applications
- Filter applications by status (applied, interview, offer, rejected)
- `/stats` endpoint with a count of applications per status
- Input validation and clear error messages (for example, 404 for an unknown company)
- Automated tests with pytest

## Tech used
Python, FastAPI, SQLAlchemy, SQLite, pytest, Git and GitHub

## API endpoints
| Method | Path | Description |
|---|---|---|
| POST | /companies | Add a company |
| GET | /companies | List companies |
| POST | /applications | Add an application |
| GET | /applications | List applications (optional `?status=interview`) |
| GET | /applications/{id} | Get one application |
| PUT | /applications/{id} | Update an application |
| DELETE | /applications/{id} | Delete an application |
| GET | /stats | Count of applications per status |

## How to run
```bash
git clone https://github.com/thamilini0/job-tracker-api.git
cd job-tracker-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000/docs to try the API.

## How to run the tests
```bash
pytest
```

## Screenshots
![API docs](screenshots/docs.png)

## What I learned
- Building a REST API with FastAPI
- Working with a database using SQLAlchemy
- Validating input with Pydantic
- Writing automated tests with pytest
- Using Git and GitHub for version control