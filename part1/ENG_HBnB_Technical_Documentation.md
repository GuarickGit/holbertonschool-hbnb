
# 🏗️ HBnB – Technical Architecture Documentation

---

## 📘 Introduction

The **HBnB** project is a simplified re-implementation of the AirBnB platform. It involves user account management, place listing creation, review submission, and search/filter functionalities. This document presents the technical design blueprint of the application and is intended as a reference throughout the development process.

It compiles:
- A high-level architectural overview of the system
- A detailed class diagram for the business logic layer
- Four sequence diagrams representing key API interactions

---

## 🧱 High-Level Architecture

### 🔹 Overview

The HBnB system is built using a **3-layer architecture**:
- **Presentation Layer (API)**: Handles incoming client requests
- **Business Logic Layer (Service)**: Processes application logic and enforces rules
- **Persistence Layer (Repository)**: Manages interaction with the database

The architecture uses the **Facade Pattern** to simplify the connection between the API and business logic.

### 🔸 Diagram

![High Level Package Diagram](https://raw.githubusercontent.com/guarickgit/holbertonschool-hbnb/main/part1/package_diagram.png)
- Services like `UserService`, `PlaceService`, and `ReviewService` act as facades to the business logic.
- Repositories isolate data access from the business layer.

### 🔸 Notes

- Each layer is decoupled, allowing for isolated testing and maintenance.
- API communicates only with Services, never directly with Repositories.

---

## 📐 Business Logic Layer – Class Diagram

### 🔹 Diagram

```mermaid
classDiagram
class ClassUser {
    + firstname : string
    + lastname : string
    + email : string
    # password : string
    # admin : boolean
    + register() void
    + is_admin() boolean
}
class ClassReview {
    + rating : integer
    + comment : string
    + place : ClassPlace
    + user : ClassUser
    + listed_by_place(place_id: UUID) List~ClassReview~
}
class ClassBase{
    + id : UUID
    + created_at : datetime
    + updated_at : datetime
    + create() void
    + update() void
    + delete() void
}
class ClassPlace {
    + title : string
    + description : string
    + price : float
    + latitude : float
    + longitude : float
    + owner : ClassUser
    + amenities : List~ClassAmenity~
    + listed() List~ClassPlace~
}
class ClassAmenity {
    + name : string
    + description : string
    + listed() List~ClassAmenity~
}
ClassBase <|-- ClassUser : inheritance
ClassBase <|-- ClassPlace : inheritance
ClassBase <|-- ClassReview : inheritance
ClassBase <|-- ClassAmenity : inheritance
ClassUser "1" --> "*" ClassPlace : owns
ClassUser "1" --> "*" ClassReview :writes
ClassPlace "1" --> "*" ClassReview : has
ClassPlace "*" --> "*" ClassAmenity : includes
ClassReview "*" --> "1" ClassPlace : about
ClassReview "*" --> "1" ClassUser : written_by
```

### 🔸 Overview

The class diagram defines the core entities:
- `User`: has a `register()` method and owns Places and Reviews
- `Place`: linked to a `User` (owner), has a `listed()` method, includes Amenities
- `Review`: linked to both a `User` and `Place`, includes `rating`, `comment`
- `Amenity`: features associated with a Place
- `Base`: abstract class with shared attributes/methods like `create()`, `update()`

### 🔸 Relationships

- `User 1 → * Place`
- `Place 1 → * Review`
- `Place * ↔ * Amenity`
- `Review * → 1 Place`
- `Review * → 1 User`

---

## 🔁 API Interaction Flow – Sequence Diagrams

### 🧍 User Registration

```mermaid
sequenceDiagram
participant User
participant API
participant UserService
participant UserRepository
participant Database

User->>API: register()
API->>API: Check format / required fields

alt Invalid format
    API-->>User: 400 Bad Request
else Valid format
    API->>UserService: register(user_data)
    UserService->>UserService: Validate user rules
    alt Invalid user data
        UserService-->>API: 400 Bad Request: invalid user
        API-->>User: 400 Bad Request
    else Valid user data
        UserService->>UserRepository: Check if user exists
        alt User already exists
            UserService-->>API: 400 Conflict: user already exists
            API-->>User: 400 Conflict
        else New user
            UserRepository->>Database: Insert into users
            Database-->>UserRepository: Confirm Save
            UserRepository-->>UserService: Success
            UserService-->>API: User created
            API-->>User: return 201 Created
        end
    end
end
```

- The user registers through `API → UserService → UserRepository`
- Validations include format checks, rule enforcement, and email uniqueness
- Errors: `400 Bad Request`, `409 Conflict`
- Success: `201 Created`

### 🏠 Place Creation

```mermaid
sequenceDiagram
participant User
participant API
participant PlaceService
participant PlaceRepo
participant Database

User->>API: Create()
API->>API: Check format / required fields
alt Invalid Data
    API-->>User: Error 400 Bad Request
else Valid Data
    API->>PlaceService: Create(user_id, place_data)
    PlaceService->>PlaceService: Validate business rules
    alt Invalid Business rules
        PlaceService-->>API: 400 Bad Request : Invalid data
        API-->>User: 400 Bad Request
    else Valid Business rules
        PlaceService->>PlaceService: attach owner_id to place
        PlaceService->>PlaceRepo: create()
        PlaceRepo->>Database: Insert into Place
        Database-->>PlaceRepo: Confirm save
        PlaceRepo-->>PlaceService: Success
        PlaceService-->>API: Place Created
        API-->>User: Return 201 Created
    end
end
```

- The user creates a listing with `user_id` and `place_data`
- Business rules are applied (e.g., price must be positive)
- `PlaceRepository` handles persistence
- Success: `201 Created`, Error: `400`

### 📝 Review Submission

```mermaid
sequenceDiagram
participant User
participant API
participant ReviewService
participant ReviewRepository
participant Database

User->>API: create()
API->>API: Check format / required fields

alt Invalid format
    API-->>User: 400 Bad Request
else Valid format
    API->>ReviewService: create(user_id, review_data)
    ReviewService->>ReviewService: Validate business rules
    alt Invalid review data
        ReviewService-->>API: 400 Bad Request: invalid review
        API-->>User: 400 Bad Request
    else Valid review data
        ReviewService->>Database: Check if place exists
        alt Place does not exist
            ReviewService-->>API: 404 Not Found: place not found
            API-->>User: 404 Not Found
        else Place exists
            ReviewService->>ReviewRepository: create()
            ReviewRepository->>Database: Insert into reviews
            Database-->>ReviewRepository: Confirm save
            ReviewRepository-->>ReviewService: Success
            ReviewService-->>API: Review created
            API-->>User: 201 Created
        end
    end
end
```

- The user submits a review for an existing `Place`
- Validation includes rating bounds, place existence
- May return: `400`, `404`, or `201 Created`

### 🏡 Fetching a List of Places

```mermaid
sequenceDiagram
participant User
participant API
participant PlaceService
participant PlaceRepository
participant Database

User->>API: listed(filters)
API->>API: Validate query parameters

alt Invalid parameters
    API-->>User: 400 Bad Request
else Valid parameters
    API->>PlaceService: listed(filters)
    PlaceService->>PlaceService: Apply business filters
    PlaceService->>PlaceRepository: listed(filters)
    PlaceRepository->>Database: Fetch matching places
    Database-->>PlaceRepository: Return place list
    PlaceRepository-->>PlaceService: Return place list
    PlaceService-->>API: Return place list
    API-->>User: 200 OK + JSON list
end
```

- The user queries places using filters
- Service applies optional business filters
- Repository returns matching results
- Response: `200 OK + JSON`

---

## ✅ Summary

This document compiles the complete technical foundation for HBnB, structured across architecture, class modeling, and runtime interactions. It ensures a clean, modular, and testable base for implementing the full functionality.
