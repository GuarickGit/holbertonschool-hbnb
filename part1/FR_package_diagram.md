# 📊 High-Level Package Diagram
![High Level Package Diagram](https://raw.githubusercontent.com/guarickgit/holbertonschool-hbnb/main/part1/package_diagram.png)

# 🧭 Vue d’ensemble du fonctionnement

Lorsqu’un client envoie une requête via l’interface (par exemple un navigateur), cette requête est transmise à l’API.
L’API s’appuie sur un **Facade Pattern**, qui agit comme un point d’entrée unique vers la logique métier.
Ce facade se charge ensuite d’orienter la requête vers le service concerné (par exemple `UserService`, `PlaceService`, etc.).

### 🔍 Exemple : Création d’un logement (*place*)

1. Le client envoie une requête pour créer une nouvelle place.
2. L’API reçoit la requête et la transmet au **facade**.
3. Le **facade** délègue le traitement au `PlaceService`.
4. Le `PlaceService` applique les règles métiers (ex : validité des champs, prix non négatif, etc.).
5. Une fois validée, la demande est transmise à la couche de **persistence** pour l’enregistrement en base de données.
6. Une fois la place créée, une réponse est renvoyée au client, généralement au format **JSON**.

---

# 🧱 Les Trois Couches de l’Architecture

## 💻 Presentation Layer

- Couche visible par l’utilisateur.
- Comprend l’interface utilisateur (web ou mobile).
- Permet à l’utilisateur d’interagir avec l’application.

## 🧠 Business Logic Layer

- Contient la **logique métier** : les règles et traitements propres à l’application.
- Exemples : un prix ne peut pas être négatif, un nom d’utilisateur doit être valide, etc.
- Gère les différents **services métiers** (`UserService`, `PlaceService`, etc.).
- Centralise les validations et le traitement des données.

## 💾 Persistence Layer

- Responsable de l’accès à la **base de données**.
- Assure les opérations de **lecture et d’écriture** (CRUD).
- Totalement isolée de la logique métier via des interfaces simples (`save`, `delete`, `find_by_id`, etc.).

---

# 🎯 Le **Facade Pattern**

Le **Facade Pattern** est un patron de conception orienté objet qui fournit une **interface unifiée et simplifiée** vers un ensemble complexe de sous-systèmes.

## Dans notre architecture :

- Il sert d’intermédiaire entre l’**API** (présentation) et les **services métiers** (logique métier).
- Il **simplifie les appels** faits depuis l’API, en masquant les détails d’implémentation des services.
- Il permet de **découpler** les couches, réduisant ainsi les dépendances directes entre elles.

✅ Résultat :
- Le code est plus modulaire, plus maintenable.
- Chaque couche peut évoluer indépendamment tant que l’interface du facade reste stable.
