# SecureApp – Two-Factor Authentication System

A modern authentication system built with Vue.js (frontend) and FastAPI (backend).  
Features TOTP-based 2FA, JWT authentication, bcrypt password hashing, PostgreSQL, and full Docker support.

This project demonstrates production-ready secure authentication.

---

## How to Run the App (Docker Only)

### 1. Clone the Repository

```sh
git clone https://github.com/Spyou/2fa-app.git
cd 2fa-app
```

---

## 2. Create Environment Variables

Inside the `backend/` folder, create a `.env` file.

### Generate a secure JWT key:

```sh
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Create `backend/.env`:

```
JWT_SECRET_KEY=your_generated_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://user:pass@db:5432/app
```

---

## 3. Start the App Using Docker

```sh
docker-compose up --build
```

### After the build completes:

- Frontend: http://localhost:5173  
- Backend API: http://localhost:5000  

You can now register, enable 2FA, log in, and access the dashboard.

---

## Features

- Secure user registration and login  
- TOTP-based two-factor authentication  
- JWT token-based session management  
- bcrypt password hashing  
- PostgreSQL with SQLAlchemy ORM  
- QR code generation for 2FA setup  
- Fully containerized frontend, backend, and database  
- Minimal and clean dashboard UI  

---

## Tech Stack

### Frontend
- Vue.js 3  
- Vue Router  
- Vite  
- Axios  

### Backend
- FastAPI  
- SQLAlchemy ORM  
- PostgreSQL  
- python-jose (JWT)  
- bcrypt  
- pyotp (TOTP)  

### Infrastructure
- Docker  
- Docker Compose  

---

## API Endpoints

| Endpoint        | Method | Description |
|----------------|--------|-------------|
| `/`            | GET    | Health check |
| `/register`    | POST   | Create a user |
| `/login`       | POST   | Login and receive JWT |
| `/me`          | GET    | Get the authenticated user's details |
| `/2fa/enable`  | POST   | Generate QR code for 2FA setup |
| `/2fa/verify`  | POST   | Verify TOTP code and enable 2FA |

---

Spyou  
GitHub: https://github.com/Spyou


https://github.com/user-attachments/assets/45337073-8ffc-4678-8dc1-cf7648b24981

<img width="1512" height="982" alt="Screenshot 2025-11-20 at 9 13 49 PM" src="https://github.com/user-attachments/assets/21da33de-7820-42fb-a0f7-77e04aab826e" />

