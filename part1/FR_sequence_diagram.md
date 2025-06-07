# 📲 Diagrammes de séquence pour les appels d'API
## 🧍 Diagramme de séquence pour l'enregistrement des utilisateurs
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
---

## 🧍 Inscription de l'utilisateur

### 🔹 Description :
L’utilisateur envoie une requête pour créer un compte sur la plateforme. Le système doit valider les données, vérifier l’unicité de l’adresse email, puis enregistrer l’utilisateur dans la base de données.

### 🔸 Flow des interactions :
- **API** : Vérifie la structure et les champs obligatoires (ex: email, mot de passe).
- **UserService** : Applique les règles métier (validité des données, unicité).
- **UserRepository** : Vérifie si l’utilisateur existe déjà, puis enregistre le nouvel utilisateur.
- **Database** : Enregistre les données persistantes.
- En cas de succès, l’API renvoie un `201 Created`. Sinon, des erreurs `400` ou `409` sont retournées selon le cas.

---
## 🏠 Diagramme de séquence pour la création de lieux
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
---

## 🏠 Création de lieux

### 🔹 Description :
Un utilisateur authentifié crée une nouvelle annonce de logement. Le système valide les données du logement, les complète avec l’`owner_id`, puis les enregistre en base.

### 🔸 Flow des interactions :
- **API** : Vérifie le format et les champs requis dans la requête.
- **PlaceService** : Applique les règles métier (ex: prix positif, description présente).
- **PlaceService** ajoute l'identifiant de l’utilisateur comme propriétaire du `Place`.
- **PlaceRepository** : Enregistre l’objet dans la base.
- **Database** : Confirme l’enregistrement.
- Le système retourne un `201 Created` ou une erreur `400` en cas de problème.

---
## 📝 Diagramme de séquence pour la soumission dun avis
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
---

## 📝 Soumission d'un avis

### 🔹 Description :
Un utilisateur souhaite publier un avis (note/commentaire) sur un logement. Le système valide l’avis, s’assure que le logement existe, puis le sauvegarde.

### 🔸 Flow des interactions :
- **API** : Vérifie la structure des données (`rating`, `comment`, `place_id`…).
- **ReviewService** : Applique les règles métier (note dans les bornes, commentaire non vide).
- Le service vérifie ensuite que le `Place` ciblé existe dans la base.
- **ReviewRepository** : Insère la `Review`.
- **Database** : Confirme l’enregistrement.
- Réponse : `201 Created` si succès, sinon `400` ou `404` selon l’erreur.

---
## 🏡 Diagramme de séquence pour récupérer une liste de lieux
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
---

## 🏡 Récupération d'une liste de lieux

### 🔹 Description :
L’utilisateur envoie une requête pour consulter une liste de logements disponibles, en filtrant éventuellement par ville, capacité, etc.

### 🔸 Flow des interactions :
- **API** : Valide les paramètres de requête (types, valeurs).
- **PlaceService** : Applique des règles supplémentaires (filtres métier ou valeurs par défaut).
- **PlaceRepository** : Exécute la requête filtrée vers la base.
- **Database** : Retourne la liste des `Place` correspondants.
- La liste est remontée jusqu’à l’utilisateur avec un `200 OK` + `fichier json`.

---
