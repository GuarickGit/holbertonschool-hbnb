## 🧍 Sequence Diagram for User Registration
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

## 🏠 Sequence Diagram for Place Creation
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
## 📝 Sequence Diagram for Review Submission
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
## 🏡 Sequence Diagram for Fetching a List of Places
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
