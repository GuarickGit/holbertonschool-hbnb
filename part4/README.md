# HBnB - Part 4: Simple Web Client

![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=yellow)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?logo=jsonwebtokens&logoColor=white)
![Fetch API](https://img.shields.io/badge/Fetch--API-333333?logo=javascript)


This repository contains **Part 4** of the HBnB project. This phase focuses on building a dynamic web front-end that interfaces with the secure API created in previous phases. It includes user authentication, place listing, place detail view, and the ability for logged-in users to post reviews.

---

## 📚 Project Scope

This part of the project implements the front-end interface and JavaScript functionality to:

- 🔐 Log in using JWT and store token in cookies
- 🏡 Display a list of places dynamically (with client-side filtering)
- 🧾 View detailed information about a place
- 🗣️ Add a review for a place (only when authenticated)

---

## 🏗️ Project Structure

```
Part4/
├── add_review.html         # Page to submit a review (auth only)
├── index.html              # Lists all available places (main page)
├── login.html              # User login page
├── place.html              # Page showing a specific place's info
├── styles.css              # Provided and custom styling
├── README.md               # You are here !
├── images/                 # App logo and app icon
└── scripts/
    ├── common.js           # Handles logout, cookie parsing, auth checks
    ├── index.js            # Login logic, fetch & display places, filters
    ├── place.js            # Fetch place info & reviews
    └── reviews.js          # Auth check & review submission form
```

---

## 🚀 How to Run

1. Clone this repository

```bash
git clone https://github.com/GuarickGit/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

2. Launch your Flask backend on port 5000:

```bash
python3 run.py
```

3. Launch your frontend using Python HTTP server on port 8000:

```bash
python3 -m http.server 8000
```

> ⚠️ Ensure the API is available at `http://localhost:5000` — adjust URLs in JS if needed.

---

## 🔧 Features Implemented

### ✅ Authentication

- JWT-based login via API (`/api/v1/auth/login`)
- Token stored in cookies and reused on requests
- Logout button clears cookie and redirects

### 🏘️ List of Places (`index.html`)

- Dynamic card layout populated via JS
- Filters places by max price (dropdown: 10, 50, 100, All)
- Redirects to login if not authenticated

### 🏠 Place Details (`place.html`)

- Title, host name, description, price
- Amenities and reviews displayed dynamically
- Shows 'Add Review' button only if logged in

### 📝 Add Review (`add_review.html`)

- Redirects unauthenticated users to index
- Authenticated users can submit a rating (1–5) and text
- Submits review via POST to `/api/v1/reviews/`
- Displays alert and redirects back to the place page

---

## 🌐 API Usage

All requests sent using Fetch API. Authentication uses:

```http
Authorization: Bearer <token>
```

Endpoints:

- `POST /api/v1/auth/login` → returns JWT token
- `GET /api/v1/places/` → list of all places
- `GET /api/v1/places/<place_id>` → detailed place info
- `POST /api/v1/reviews/` → create new review (auth only)

---

## 🔐 Authentication Logic (JS)

- `getCookie(name)` → parses cookies to extract JWT
- `checkAuthentication()` → toggles UI and routes based on auth
- `logoutButton` clears token and redirects to login

---

## 🧠 Key Learnings

- Front-end & back-end integration via Fetch
- Using JWT securely in client-side apps
- Dynamic DOM updates with JS templates
- Protecting routes on the client using cookies
- CORS handling with `flask_cors`

---

## 👥 Author

Fresne Kévin – [@GuarickGit](https://github.com/GuarickGit)
