
# 📲 Sequence Diagrams for API Calls

---

## 🧍 Sequence Diagram: User Registration
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

### 🔹 Description:
The user submits a request to register an account. The system validates the input, checks for email uniqueness, and saves the user if all is valid.

### 🔸 Flow of Interactions:
- **API**: Checks data structure and required fields.
- **UserService**: Applies business rules (valid data, uniqueness).
- **UserRepository**: Checks existence and saves the user.
- **Database**: Persists the data.
- Returns `201 Created` on success, or `400`/`409` on error.

---

## 🏠 Sequence Diagram: Place Creation
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

### 🔹 Description:
An authenticated user creates a new listing. The system validates the data, assigns ownership, and stores it.

### 🔸 Flow of Interactions:
- **API**: Validates required fields.
- **PlaceService**: Applies business rules (e.g. positive price).
- **PlaceService** attaches the `owner_id` to the place.
- **PlaceRepository**: Saves the entity.
- **Database**: Confirms persistence.
- Returns `201 Created` or `400 Bad Request`.

---

## 📝 Sequence Diagram: Review Submission
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

### 🔹 Description:
The user submits a review for a place. The system ensures the data is valid and the place exists before saving the review.

### 🔸 Flow of Interactions:
- **API**: Checks required data (`rating`, `comment`, `place_id`, etc.).
- **ReviewService**: Applies business validation.
- **ReviewService** checks if the `Place` exists.
- **ReviewRepository**: Saves the review.
- **Database**: Confirms persistence.
- Returns `201 Created`, or `400`/`404` if invalid or not found.

---

## 🏡 Sequence Diagram: Fetching a List of Places
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

### 🔹 Description:
The user requests a filtered list of available places.

### 🔸 Flow of Interactions:
- **API**: Validates input parameters.
- **PlaceService**: Applies filtering logic (if any).
- **PlaceRepository**: Queries the database.
- **Database**: Returns matching places.
- Response sent to user as a `200 OK` with a JSON payload.

---
