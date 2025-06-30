# HBnB - Part 2: Business Logic and API Endpoints

![Python](https://img.shields.io/badge/Python-3.12.3-blue)
![Flask](https://img.shields.io/badge/Flask-RESTx-success)
![Pattern](https://img.shields.io/badge/Pattern-Facade-orange)
![Architecture](https://img.shields.io/badge/Architecture-Layered%20MVC-blueviolet)
[![Swagger UI](https://img.shields.io/badge/Swagger-UI-yellowgreen)](http://127.0.0.1:5000/)

This repository contains Part 2 of the HBnB project, focused on implementing the Business Logic and RESTful API endpoints using Python and Flask.

## 📚 Project Scope

This phase of the HBnB project brings to life the application's internal functionality by implementing:

- A **Business Logic Layer**: Models and relationships for `User`, `Place`, `Review`, and `Amenity`.
- A **Presentation Layer**: RESTful API endpoints using Flask and `flask-restx`.
- An **In-memory Repository**: For data persistence using dictionaries before migrating to a database in Part 3.
- The **Facade Pattern**: A single interface that connects the API to the business logic and persistence.

---

## 🏗️ Project Structure

```
hbnb/
├── app/                         # Core application logic
│   ├── __init__.py              # Initializes the app package
│   ├── validators.py            # Input validation logic
│
│   ├── api/                     # 🌐 Presentation Layer (Flask-RESTx APIs)
│   │   └── v1/                  # Version 1 of the API
│   │       ├── users.py         # CRUD for users
│   │       ├── places.py        # CRUD for places
│   │       ├── reviews.py       # CRUD for reviews
│   │       ├── amenities.py     # CRUD for amenities
│
│   ├── models/                  # 🧠 Business Logic Layer
│   │   ├── base_model.py        # Shared base class (id, created_at, updated_at, save, update)
│   │   ├── user.py              # User entity
│   │   ├── place.py             # Place entity (linked to User, Amenity, Review)
│   │   ├── review.py            # Review entity (linked to User and Place)
│   │   ├── amenity.py           # Amenity entity (linked to Place)
│
│   ├── persistence/             # 💾 In-Memory Persistence Layer
│   │   ├── repository.py        # Abstract and in-memory repository implementations
│
│   ├── services/                # 🪄 Facade Layer
│   │   ├── facade.py            # HBnBFacade: interface to all business operations
│
├── tests/                       # ✅ Unit tests for models and APIs
│   ├── test_user.py             # Tests for User logic and endpoints
│   ├── test_place.py            # Tests for Place logic and endpoints
│   ├── test_review.py           # Tests for Review logic and endpoints
│   ├── test_amenity.py          # Tests for Amenity logic and endpoints
│   └── TEST_REPORT.md           # Manual test results or coverage report
│
├── config.py                    # Application settings and configuration
├── run.py                       # Entrypoint for running the Flask app
├── requirements.txt             # Python dependencies (Flask, flask-restx, etc.)
└── README.md                    # Project documentation (you're here!)

```

---

## 🔌 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/GuarickGit/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python run.py
```

Access Swagger documentation at:

```
http://127.0.0.1:5000/
```

---

## 🔧 Features Implemented

### ✅ Business Logic Classes

- `User`: Handles registration, email uniqueness, and admin status.
- `Place`: Includes price, coordinates validation, owner reference, amenities, and reviews.
- `Amenity`: Independent entity linked to places.
- `Review`: Linked to both users and places, includes rating validation (1-5).

## ✅ API Endpoints

Implemented using `flask-restx` and grouped by resource:

### 🔹 Users
| Method | Endpoint                         | Description                              |
|--------|----------------------------------|------------------------------------------|
| `POST` | `/api/v1/users/`                 | Create a new user                        |
| `GET`  | `/api/v1/users/`                 | Retrieve all users                       |
| `GET`  | `/api/v1/users/<user_id>`        | Retrieve a specific user by ID           |
| `PUT`  | `/api/v1/users/<user_id>`        | Update a user’s information              |

---

### 🔹 Places
| Method | Endpoint                         | Description                              |
|--------|----------------------------------|------------------------------------------|
| `POST` | `/api/v1/places/`                | Create a new place                       |
| `GET`  | `/api/v1/places/`                | Retrieve all places                      |
| `GET`  | `/api/v1/places/<place_id>`      | Retrieve a specific place by ID          |
| `PUT`  | `/api/v1/places/<place_id>`      | Update a place’s details                 |

---

### 🔹 Amenities
| Method | Endpoint                             | Description                          |
|--------|--------------------------------------|--------------------------------------|
| `POST` | `/api/v1/amenities/`                 | Create a new amenity                 |
| `GET`  | `/api/v1/amenities/`                 | Retrieve all amenities               |
| `GET`  | `/api/v1/amenities/<amenity_id>`     | Retrieve a specific amenity by ID    |
| `PUT`  | `/api/v1/amenities/<amenity_id>`     | Update an amenity’s information      |

---

### 🔹 Reviews
| Method  | Endpoint                              | Description                                 |
|---------|---------------------------------------|---------------------------------------------|
| `POST`  | `/api/v1/reviews/`                    | Create a new review                         |
| `GET`   | `/api/v1/reviews/`                    | Retrieve all reviews                        |
| `GET`   | `/api/v1/reviews/<review_id>`         | Retrieve a specific review by ID            |
| `PUT`   | `/api/v1/reviews/<review_id>`         | Update a review’s content                   |
| `DELETE`| `/api/v1/reviews/<review_id>`         | Delete a review                             |
| `GET`   | `/api/v1/places/<place_id>/reviews`   | Retrieve all reviews for a specific place   |
---

## ✅ Validation and Testing

- All fields validated at model level (e.g. price > 0, email format, lat/lon ranges).
- Status codes respected: `201 Created`, `200 OK`, `400 Bad Request`, `404 Not Found`.
- Tested using `curl`, Swagger UI, and `unittest`.

---

## 🧪 Example Unit Test

Here is a basic example of a unit test for the `User` model:

### 🔹 File: `tests/test_user.py`

```python
import unittest
from app.models.user import User

class TestUserModel(unittest.TestCase):
    def test_valid_user_creation(self):
        user = User(first_name="Axel", last_name="Goré", email="axel.goré@gmail.com")
        self.assertEqual(user.first_name, "Axel")
        self.assertEqual(user.last_name, "Goré")
        self.assertEqual(user.email, "axel.goré@gmail.com")
```

### ▶️ Command to run this test
```bash
python3 -m unittest tests/test_user.py
```

### ✅ Expected output
```bash
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```
---

## 🧪 Example `curl` Commands

```bash
# Create a user
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Axel", "last_name": "Goré", "email": "axel.goré@gmail.com"}'

# Get all places
curl http://localhost:5000/api/v1/places/
```

---

## 🧪 Example Swagger UI Test

You can test endpoints directly from the **Swagger UI** (interactive docs) available at:

http://localhost:5000/

### 🔹 Example: `POST /api/v1/users/`

#### 📤 Request Body (via Swagger "Try it out")

```json
{
  "first_name": "Axel",
  "last_name": "Goré",
  "email": "axel.goré@gmail.com"
}
```

#### 📥 Example Response (201 Created)
```json
{
  "id": "8f1c6a97-b6c0-47c0-8bc3-507e5e2e55e3",
  "first_name": "Axel",
  "last_name": "Goré",
  "email": "axel.goré@gmail.com",
}
```

#### 🧾 Response Headers
```
connection: close
content-length: 150
content-type: application/json
date: Sun, 22 Jun 2025 17:47:27 GMT
server: Werkzeug/3.1.3 Python/3.12.3
```
#### ✅ Possible Status Codes
```json
201 - User successfully created
400 - Bad request: Email already registered, missing field, or invalid format
```

## 📘 Swagger API Documentation

Visit:

```
http://localhost:5000/
```

This interactive documentation is automatically generated from the codebase using `flask-restx`.

---

## 🧠 Key Learnings

- Structuring a modular Flask application.
- Applying the Facade Pattern to decouple logic layers.
- Building and validating REST APIs with Flask-RESTx.
- In-memory persistence and preparation for database integration.
- Handling object relationships and nested serialization.

---

## 🧰 Technologies Used

| Category         | Tools / Frameworks                              |
|------------------|--------------------------------------------------|
| Language         | Python 3.12.3                                    |
| Web Framework    | Flask + Flask-RESTx (for RESTful APIs)           |
| API Docs         | Swagger UI (auto-generated via `flask-restx`)    |
| Architecture     | Layered MVC + Facade Pattern                     |
| Validation       | Custom validation logic (`validators.py`)        |
| Persistence      | In-memory Repository (dictionary-based)          |
| Testing          | `unittest`, `curl`, manual reports (`TEST_REPORT.md`) |
| Documentation    | Markdown (`README.md`), Swagger, curl examples   |

---

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-RESTx Docs](https://flask-restx.readthedocs.io/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [Unittest — Python docs](https://docs.python.org/3/library/unittest.html)
- [REST API Design Guide](https://restfulapi.net/)
- [PEP8 Style Guide](https://peps.python.org/pep-0008/)

## 👥 Authors

- **Fresne Kévin** – [@GuarickGit](https://github.com/GuarickGit)
- **Roche Samira** – [@StrawberSam](https://github.com/StrawberSam)
