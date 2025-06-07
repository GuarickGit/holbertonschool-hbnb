
# 🏗️ HBnB – Documentation Technique de l’Architecture

---

## 📘 Introduction

Le projet **HBnB** est une ré-implémentation simplifiée de la plateforme AirBnB. Il comprend la gestion des comptes utilisateurs, la création d’annonces, la soumission d’avis, et la recherche avec filtres. Ce document présente la base technique de l’application, servant de référence tout au long du développement.

Il regroupe :
- Une vue d’architecture haut-niveau du système
- Un diagramme de classes pour la couche métier
- Quatre diagrammes de séquence pour illustrer les principales interactions API

---

## 🧱 Architecture Haut-Niveau

### 🔹 Vue d’ensemble

Le système HBnB est conçu en **architecture trois couches** :
- **Présentation (API)** : Gère les requêtes entrantes
- **Logique métier (Services)** : Applique les règles de l’application
- **Persistance (Repository)** : Gère les interactions avec la base de données

L’architecture applique le **modèle facade**, pour simplifier les appels entre API et logique métier.

### 🔸 Diagramme

![High Level Package Diagram](https://raw.githubusercontent.com/guarickgit/holbertonschool-hbnb/main/part1/package_diagram.png)

- Les services `UserService`, `PlaceService`, `ReviewService` font office de facade.
- Les repositories isolent l’accès aux données.

### 🔸 Remarques

- Chaque couche est découplée, facilitant la maintenance.
- L’API ne communique **qu’avec les services**, jamais directement avec la base.

---

## 📐 Couche Logique Métier – Diagramme de Classes

### 🔹 Diagramme

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

### 🔸 Vue d’ensemble

Ce diagramme modélise les entités principales :
- `User` : méthode `register()`, propriétaire de `Place` et `Review`
- `Place` : possède une méthode `listed()`, est lié à `User` et `Amenity`
- `Review` : lié à un `User` et un `Place`, contient `rating`, `comment`
- `Amenity` : équipement associé à un `Place`
- `Base` : classe abstraite avec `create()`, `update()`, etc.

### 🔸 Relations

- `User 1 → * Place`
- `Place 1 → * Review`
- `Place * ↔ * Amenity`
- `Review * → 1 Place`
- `Review * → 1 User`

---

## 🔁 Diagrammes de Séquence – API

### 🧍 Enregistrement d’un utilisateur

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

- L'utilisateur s’enregistre via `API → UserService → UserRepository`
- Validation : format, règles métier, unicité de l'email
- Erreurs possibles : `400`, `409`
- Succès : `201 Created`

---

### 🏠 Création d’un lieu

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

- L'utilisateur crée un lieu avec `user_id` et `place_data`
- Le service applique les règles métier (ex : prix positif)
- Le lieu est enregistré via `PlaceRepository`
- Réponse : `201 Created` ou `400 Bad Request`

---

### 📝 Soumission d’un avis

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

- L'utilisateur envoie un avis sur un lieu existant
- Règles métier : commentaire, note valide, lieu existant
- Réponse : `201 Created`, ou erreur `400`, `404`

---

### 🏡 Récupération d’une liste de lieux

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

- L’utilisateur envoie une requête avec des filtres (ville, capacité…)
- Le service applique des filtres métier si besoin
- Le repository renvoie les lieux correspondants
- Réponse : `200 OK` avec la liste JSON

---

## ✅ Résumé

Ce document regroupe toute la base technique de HBnB : architecture, classes métiers, et interactions clés de l’API.
Il sert de référence claire, modulaire et maintenable pour guider le développement de l’application.

