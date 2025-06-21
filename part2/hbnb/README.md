# HBnB - Part 2: Business Logic and API Endpoints

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
├── app/
│   ├── api/                # Presentation Layer (API)
│   │   └── v1/             # Versioned API endpoints
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/             # Business Logic Layer
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/           # Facade Layer
│   │   ├── facade.py
│   │   └── __init__.py
│   └── persistence/        # In-Memory Repository
│       └── repository.py
├── config.py               # Application configuration
├── run.py                  # Flask application entrypoint
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🔌 How to Run

### 1. Clone the repository

```bash
git clone <repo-url>
cd part2/hbnb
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

### ✅ API Endpoints

Implemented using `flask-restx` and grouped by resource:

- **Users**
  - `POST /api/v1/users/`
  - `GET /api/v1/users/`
  - `GET /api/v1/users/<user_id>`
  - `PUT /api/v1/users/<user_id>`

- **Places**
  - `POST /api/v1/places/`
  - `GET /api/v1/places/`
  - `GET /api/v1/places/<place_id>`
  - `PUT /api/v1/places/<place_id>`

- **Amenities**
  - `POST /api/v1/amenities/`
  - `GET /api/v1/amenities/`
  - `GET /api/v1/amenities/<amenity_id>`
  - `PUT /api/v1/amenities/<amenity_id>`

- **Reviews**
  - `POST /api/v1/reviews/`
  - `GET /api/v1/reviews/`
  - `GET /api/v1/reviews/<review_id>`
  - `PUT /api/v1/reviews/<review_id>`
  - `DELETE /api/v1/reviews/<review_id>`
  - `GET /api/v1/places/<place_id>/reviews`

---

## ✅ Validation and Testing

- All fields validated at model level (e.g. price > 0, email format, lat/lon ranges).
- Status codes respected: `201 Created`, `200 OK`, `400 Bad Request`, `404 Not Found`.
- Tested using `curl`, Swagger UI, and `unittest`.

---

## 🧪 Example `curl` Commands

```bash
# Create a user
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}'

# Get all places
curl http://localhost:5000/api/v1/places/
```

---

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
