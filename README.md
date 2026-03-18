MediCare API
--
MediCare API is a FastAPI-based backend for managing doctors, scheduling medical appointments, and tracking consultations. The API is backed by PostgreSQL and deployed via Docker for production-ready use.
--

Features:

- Manage doctors: create, update, delete, and view doctor records.

- Schedule appointments: in-person, video, or emergency types.

- Track appointments: scheduled, confirmed, cancelled, completed.

- Pydantic-based input validation.

- Filter, search, sort, and paginate doctors and appointments.

- Multi-step workflows for appointments.

- Database-backed (PostgreSQL) for persistence.

- Fully containerized with Docker for easy deployment.

---

Tech Stack:

Backend: FastAPI

Database: PostgreSQL

ORM: SQLAlchemy

Data Validation: Pydantic

Containerization: Docker & Docker Compose

Python Version: 3.11

--- 
Setup & Installation:

Clone the repository:
```bash
git clone https://github.com/heubert-69/MediCare-API.git
cd MediCare-API
```

Create a virtual environment and activate it (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Configure environment variables:

Create a .env file:
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=medicare
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
---

Docker Deployment:

Build and start the services:

```bash
docker-compose up -d --build
```

Verify running containers:
```bash
docker ps
```

View logs:
```bash
docker-compose logs -f
```

Stop services:
```bash
docker-compose down
```
---
Database:

- PostgreSQL is used as the primary datastore.

- SQLAlchemy models handle persistence.

- Initial setup creates tables automatically on first run.

- docker-compose mounts a persistent volume (postgres_data) for database storage.
---
API Endpoints:
---
Doctors:
Method	Endpoint	Description
GET	/doctors	List all doctors
GET	/doctors/{doctor_id}	Retrieve a doctor by ID
POST	/doctors	Add a new doctor
PUT	/doctors/{doctor_id}	Update a doctor
DELETE	/doctors/{doctor_id}	Delete a doctor (if no active appointments)
GET	/doctors/summary	Summary statistics for doctors
GET	/doctors/filter	Filter doctors by specialization, fee, experience, availability
GET	/doctors/search	Search doctors by name or specialization
GET	/doctors/sort	Sort doctors by fee, experience, or name
GET	/doctors/page	Paginate doctors list
GET	/doctors/browse	Combined search + sort + pagination
--
Appointments:
Method	Endpoint	Description
GET	/appointments	List all appointments
POST	/appointments	Create a new appointment
POST	/appointments/{appointment_id}/confirm	Confirm an appointment
POST	/appointments/{appointment_id}/cancel	Cancel an appointment
POST	/appointments/{appointment_id}/complete	Complete an appointment
GET	/appointments/active	List only scheduled/confirmed appointments
GET	/appointments/by-doctor/{doctor_id}	List appointments for a specific doctor
GET	/appointments/search	Search appointments by patient name
GET	/appointments/sort	Sort appointments by fee or date
GET	/appointments/page	Paginate appointments list

Testing:

- Use Swagger UI at /docs for interactive testing.

- Example requests are pre-populated.

- All input validations are enforced via Pydantic models.

Project Structure:
```bash
MediCare-API/
├─ app/
│  ├─ main.py          # FastAPI app
│  ├─ models.py        # SQLAlchemy models
│  ├─ schemas.py       # Pydantic models
│  ├─ crud.py          # Database operations
│  ├─ helpers.py       # Helper functions (fee calculation, filtering)
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ .env
├─ README.md
```
---
Contributing:

- Fork the repo

- Create a feature branch

- Commit changes with clear messages

- Push branch and open a pull request
---
License

This project is licensed under MIT License.
