# 📊 High-Level Package Diagram
![High Level Package Diagram](https://raw.githubusercontent.com/guarickgit/holbertonschool-hbnb/main/part1/package_diagram.png)

# 🧭 Overview of the Workflow

When a client sends a request through the interface (e.g., a web browser), the request is passed to the API.
The API relies on a **Facade Pattern**, which acts as a single entry point to the business logic.
The facade then routes the request to the appropriate service (such as `UserService`, `PlaceService`, etc.).

### 🔍 Example: Creating a Place

1. The client sends a request to create a new place.
2. The API receives the request and forwards it to the **facade**.
3. The **facade** delegates the task to the `PlaceService`.
4. `PlaceService` processes the request and applies the business rules (e.g., field validation, positive price check, etc.).
5. Once validated, the service calls the **persistence layer** to save the place in the database.
6. After the place is created, a response is returned to the client, usually in **JSON** format.

---

# 🧱 The Three Layers of Architecture

## 💻 Presentation Layer

- The layer visible to the user.
- Includes the user interface (web or mobile).
- Allows the user to interact with the application.

## 🧠 Business Logic Layer

- Contains the **business logic**: rules and processes specific to the application.
- Examples: price must not be negative, username must be valid, etc.
- Manages the various **service components** (`UserService`, `PlaceService`, etc.).
- Centralizes data processing and validation.

## 💾 Persistence Layer

- Responsible for accessing the **database**.
- Handles **read and write operations** (CRUD).
- Completely isolated from business logic through simple operations (`save`, `delete`, `find_by_id`, etc.).

---

# 🎯 The **Facade Pattern**

The **Facade Pattern** is an object-oriented design pattern that provides a **unified and simplified interface** to a complex subsystem.

## In our architecture:

- It acts as a mediator between the **API** (presentation) and **business services** (logic).
- It **simplifies calls** from the API by hiding the complexity of service implementations.
- It helps **decouple** the layers, reducing direct dependencies between them.

✅ Result:
- The code is more modular and maintainable.
- Each layer can evolve independently as long as the facade interface remains stable.
