# HBnB - Part 4: Simple Web Client

![HTML5](https://img.shields.io/badge/HTML5-✔️-orange)
![CSS3](https://img.shields.io/badge/CSS3-✔️-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow)
![FetchAPI](https://img.shields.io/badge/AJAX-Fetch%20API-lightgrey)
![Authentication](https://img.shields.io/badge/Auth-JWT%20&%20Cookies-green)

This repository contains **Part 4** of the **HBnB project**, which focuses on building a responsive, interactive **front-end web client** using HTML, CSS, and JavaScript ES6 that communicates with the backend API from previous phases.

---

## 🎯 Project Scope

This client provides:

- 🔐 **Login interface** to authenticate users and store JWT tokens via cookies.
- 🏠 **Dynamic place listings** fetched from the API, filtered client-side.
- 📄 **Detailed place pages** with reviews and amenities.
- ✍️ **Review submission form**, only accessible when logged in.
- 🌐 **AJAX-based interactivity** (no full page reloads).
- 📱 **Responsive UI** using semantic HTML5 and custom CSS.

---

## 🗂️ Project Structure

```bash
hbnb/
├── app/
│   ├── api/
│   ├── models/
│   ├── persistence/
│   └── services/
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── images/
│   │   ├── logo.png
│   │   ├── default.jpg
│   │   ├── Charmante-maison-à-Evron.jpg
│   ├── js/
│   │   └── scripts.js
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── place.html
│   ├── header.html
│   └── footer.html
├── tests/
├── sql/
├── run.py
└── requirements.txt
```

---

## 📋 Features Implemented

### ✅ 1. Login Functionality

- Uses **AJAX (Fetch API)** to submit user credentials.
- On success, **JWT token stored in cookie** for session management.
- Failed logins display error messages.
- Authenticated users are redirected to the homepage.

### ✅ 2. Places List (index.html)

- Dynamically fetched from API on page load.
- Supports **price filtering** client-side (10 / 50 / 100 / All).
- Redirects to login if user not authenticated.
- Places displayed as cards using `.place-card` class.

### ✅ 3. Place Details (place.html)

- Displays place info: name, host, price, description, amenities, and reviews.
- Uses place ID from URL query string.
- Shows "Add Review" button only if logged in.
- Reviews shown in `.review-card` elements.

### ✅ 4. Add Review (add_review.html)

- Authenticated users can post reviews using AJAX POST.
- Unauthenticated users are redirected to `index.html`.
- Form validated and cleared after success.
- API errors are handled and shown to the user.

---

## 🎨 UI Design Specs

| Element        | Class/ID            | Notes                                |
|----------------|---------------------|--------------------------------------|
| Logo           | `.logo`             | Found in header, use logo.png        |
| Login Button   | `.login-button`     | Top right, hidden when logged in     |
| Places         | `.place-card`       | Cards on homepage                    |
| Place Details  | `.place-details`, `.place-info` | Detailed info section           |
| Reviews        | `.review-card`      | User comments with rating & name     |
| Add Review     | `.add-review`       | Form visible only when logged in     |

**CSS parameters (fixed)**:
- `margin`: 20px
- `padding`: 10px
- `border`: `1px solid #ddd`
- `border-radius`: 10px

**Flexible parameters**: colors, fonts, images.

---

## 🔐 Authentication Flow

| Step | Behavior |
|------|----------|
| Login | Calls `POST /login`, stores token in cookie |
| Token Usage | Included in `Authorization` header for GET/POST |
| Auth Checks | JS checks cookie on page load |
| Redirection | Users redirected to login/index if not authenticated |

---

## 🧪 Testing Instructions

- ✅ Login with valid & invalid credentials
- ✅ Check JWT stored via `document.cookie`
- ✅ Visit homepage → see list of places if logged in
- ✅ Click "View Details" → navigate to `place.html?place_id=...`
- ✅ Review section appears only if logged in
- ✅ Submit review → see success message & updated review list

---

## 🔧 How to Run

1. **Clone repository**:
```bash
git clone https://github.com/StrawberSam/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4
```

2. **Install dependencies** (back-end):
```bash
pip install -r requirements.txt
```

3. **Start the back-end and front-end**:
```bash
python3 run.py
```
---

## 📚 Resources

- [HTML5 Semantics](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
- [CSS3 Syntax](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript ES6](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Cookie Management](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)
- [CORS Handling in Flask](https://flask-cors.readthedocs.io/en/latest/)
- [W3C Validator](https://validator.w3.org/)

---

## 👥 Authors

- **Roche Samira** – [@StrawberSam](https://github.com/StrawberSam)
