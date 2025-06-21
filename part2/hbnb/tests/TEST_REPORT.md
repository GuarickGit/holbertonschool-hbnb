# Test Report – HBnB API

## 1. Introduction

This document summarizes the manual test results performed on the HBnB API.
The goal is to verify the compliance of the endpoints with the specifications, including data validation, returned HTTP status codes, and error messages.

---

## 2. Test Environment

- Local server URL: `http://127.0.0.1:5000`
- Tools used: `curl` (command line)
- Date of tests: `22/06/2025`

---

## 3. Test Results

### 3.1 Users

| Test # | Description                    | Payload Sent                                  | Expected Result                    | Actual Result                    | HTTP Code | Comments                      |
|--------|-------------------------------|-----------------------------------------------|----------------------------------|---------------------------------|-----------|-------------------------------|
| 1      | Valid user creation            | `{ "first_name": "John", "last_name": "Doe", "email": "john.doe@mail.com" }` | User created with generated ID   | User created successfully with unique ID | 201       | OK                            |
| 2      | User creation with invalid data| `{ "first_name": "", "last_name": "", "email": "invalid-email" }`            | Error: `Invalid first_name`       | Correct error returned           | 400       | Validation works correctly     |
| 3      | User creation with empty email | `{ "first_name": "John", "last_name": "Doe", "email": "" }`                  | Error: `Invalid email`            | Correct error returned           | 400       | Validation works correctly     |
| 4      | User retrieval with invalid ID | Request with nonexistent or invalid ID       | Error: `User not found`           | Correct error returned           | 404       | Proper error handling          |

---

### 3.2 Places

| Test # | Description                    | Payload Sent                                  | Expected Result                    | Actual Result                    | HTTP Code | Comments                      |
|--------|-------------------------------|-----------------------------------------------|----------------------------------|---------------------------------|-----------|-------------------------------|
| 1      | Valid place creation           | `{ "title": "Nice House", "description": "Lovely place", "price": 120, "latitude": 45.0, "longitude": 5.0, "owner_id": "<valid_user_id>", "amenities": ["<valid_amenity_id>"] }` | Place created with generated ID  | Place created successfully with unique ID | 201       | OK                            |
| 2      | Place creation with empty title| `{ "title": "", ... }`                         | Error: `Invalid title`            | Correct error returned           | 400       | Validation works correctly     |
| 3      | Place creation with negative price | `{ "price": -10, ... }`                      | Error: `Price must be positive`   | Correct error returned           | 400       | Validation works correctly     |
| 4      | Place creation with out-of-range latitude | `{ "latitude": 100.0, ... }`              | Error: `Latitude out of range`    | Correct error returned           | 400       | Validation works correctly     |

---

### 3.3 Reviews

| Test # | Description                    | Payload Sent                                  | Expected Result                    | Actual Result                    | HTTP Code | Comments                      |
|--------|-------------------------------|-----------------------------------------------|----------------------------------|---------------------------------|-----------|-------------------------------|
| 1      | Valid review creation          | `{ "text": "Great place!", "rating": 5, "user_id": "<valid_user_id>", "place_id": "<valid_place_id>" }` | Review created with generated ID | Review created successfully with unique ID | 201       | OK                            |
| 2      | Review creation with empty text| `{ "text": "", ... }`                         | Error: `Invalid review text`      | Correct error returned           | 400       | Validation works correctly     |
| 3      | Review creation with invalid rating | `{ "rating": 6, ... }`                      | Error: `Rating must be an integer between 1 and 5` | Correct error returned | 400       | Validation works correctly     |

---

### 3.4 Amenities

| Test # | Description                    | Payload Sent                                  | Expected Result                    | Actual Result                    | HTTP Code | Comments                      |
|--------|-------------------------------|-----------------------------------------------|----------------------------------|---------------------------------|-----------|-------------------------------|
| 1      | Valid amenity creation         | `{ "name": "WiFi" }`                          | Amenity created with generated ID | Amenity created successfully with unique ID | 201       | OK                            |
| 2      | Amenity creation with empty name | `{ "name": "" }`                            | Error: `Invalid amenity name`     | Correct error returned           | 400       | Validation works correctly     |

---

## 4. Conclusion

The tests demonstrate that the API enforces the defined validation rules and returns appropriate HTTP status codes.
Error handling is clear and consistent across endpoints.
