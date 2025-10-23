
#  Rain Prediction Application

### A full-stack web application for predicting rain based on location and date

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Tech Stack:** Django REST Framework • React.js • PostgreSQL • JWT • Open-Meteo API

[Features](#-features) • [Installation](#setup-instructions) • [API Docs](#-api-endpoints) • [Demo](#-testing-the-application)

</div>

---

## Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Setup Instructions](#️-setup-instructions)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#️-database-schema)
- [Technologies Used](#-technologies-used)
- [Testing](#-testing-the-application)
- [Deployment](#-deployment-considerations)
- [Repository](#-github-repository)

---

## Features

- User authentication (Signup/Login) with JWT tokens
- Rain prediction using Open-Meteo API (free, open-source weather API)
- User-specific prediction history tracking
- PostgreSQL database for data persistence
- RESTful API with Class-Based Views
- Modern React UI with responsive design

## Project Structure

```
task/
├── backend/                      # Django Backend
│   ├── rain_prediction/         # Main Django project
│   │   ├── __init__.py
│   │   ├── settings.py          # Django settings with PostgreSQL config
│   │   ├── urls.py              # Main URL configuration
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── api/                     # API application
│   │   ├── __init__.py
│   │   ├── admin.py             # Admin interface configuration
│   │   ├── apps.py
│   │   ├── models.py            # Database models (PredictionRequest)
│   │   ├── serializers.py       # DRF serializers
│   │   ├── views.py             # Class-Based Views for API endpoints
│   │   ├── urls.py              # API URL routing
│   │   ├── services.py          # Weather prediction service
│   │   └── tests.py
│   ├── manage.py                # Django management script
│   ├── requirements.txt         # Python dependencies
│   └── config.json             # Database credentials
│
└── frontend/                    # React Frontend
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── pages/
    │   │   ├── Signup.js        # User registration page
    │   │   ├── Login.js         # User login page
    │   │   └── Dashboard.js     # Main dashboard with predictions
    │   ├── services/
    │   │   └── api.js           # API service with axios
    │   ├── App.js               # Main App component with routing
    │   ├── App.css              # Application styles
    │   ├── index.js             # React entry point
    │   └── index.css            # Global styles
    └── package.json             # Node.js dependencies
```

## Setup Instructions

### Prerequisites

- ![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white) Python 3.8+
- ![Node.js](https://img.shields.io/badge/Node.js-14+-green?logo=node.js&logoColor=white) Node.js 14+
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-316192?logo=postgresql&logoColor=white) PostgreSQL 12+
- ![Git](https://img.shields.io/badge/Git-Latest-F05032?logo=git&logoColor=white) Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL Database:**
   - Create a PostgreSQL database named `rain_prediction_db`
   - Update `config.json` with your database credentials:
   ```json
   {
       "database": {
           "ENGINE": "django.db.backends.postgresql",
           "NAME": "rain_prediction_db",
           "USER": "your_postgres_username",
           "PASSWORD": "your_postgres_password",
           "HOST": "localhost",
           "PORT": "5432"
       }
   }
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Django development server:**
   ```bash
   python manage.py runserver
   ```
   Backend will run on **http://localhost:8000**

### Frontend Setup

1. **Navigate to frontend directory (new terminal):**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start React development server:**
   ```bash
   npm start
   ```
   Frontend will run on **http://localhost:3000**

##  API Endpoints

### Authentication Endpoints

#### 1. User Signup
- **URL:** `/api/signup/`
- **Method:** `POST`
- **Authentication:** None required
- **Request Body:**
  ```json
  {
      "email": "user@example.com",
      "password": "password123"
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
      "success": true,
      "message": "User registered successfully",
      "data": {
          "user": {
              "id": 1,
              "email": "user@example.com",
              "username": "user@example.com"
          },
          "tokens": {
              "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
              "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
          }
      }
  }
  ```
- **CURL Command:**
  ```bash
  curl -X POST http://localhost:8000/api/signup/ \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"user@example.com\",\"password\":\"password123\"}"
  ```

#### 2. User Login
- **URL:** `/api/login/`
- **Method:** `POST`
- **Authentication:** None required
- **Request Body:**
  ```json
  {
      "email": "user@example.com",
      "password": "password123"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
      "success": true,
      "message": "Login successful",
      "data": {
          "user": {
              "id": 1,
              "email": "user@example.com",
              "username": "user@example.com"
          },
          "tokens": {
              "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
              "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
          }
      }
  }
  ```
- **CURL Command:**
  ```bash
  curl -X POST http://localhost:8000/api/login/ \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"user@example.com\",\"password\":\"password123\"}"
  ```

### Prediction Endpoints

#### 3. Make Prediction
- **URL:** `/api/predict/`
- **Method:** `POST`
- **Authentication:** Bearer Token required
- **Request Body:**
  ```json
  {
      "location": "London",
      "date": "2025-10-25"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
      "success": true,
      "message": "Prediction completed successfully",
      "data": {
          "id": 1,
          "location": "London",
          "date": "2025-10-25",
          "prediction": "Rain",
          "confidence": 0.75,
          "weather_data": {
              "location": "London",
              "latitude": 51.5074,
              "longitude": -0.1278,
              "date": "2025-10-25",
              "precipitation_sum": 5.2,
              "precipitation_probability": 75,
              "weathercode": 61
          },
          "created_at": "2025-10-22T10:30:00Z"
      }
  }
  ```
- **CURL Command:**
  ```bash
  curl -X POST http://localhost:8000/api/predict/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    -d "{\"location\":\"London\",\"date\":\"2025-10-25\"}"
  ```

#### 4. Get Prediction History
- **URL:** `/api/history/`
- **Method:** `GET`
- **Authentication:** Bearer Token required
- **Success Response (200 OK):**
  ```json
  {
      "success": true,
      "message": "History retrieved successfully",
      "data": {
          "count": 2,
          "predictions": [
              {
                  "id": 2,
                  "user": 1,
                  "user_email": "user@example.com",
                  "location": "Paris",
                  "date": "2025-10-26",
                  "prediction_result": "No Rain",
                  "confidence": 0.85,
                  "weather_data": {...},
                  "created_at": "2025-10-22T11:00:00Z",
                  "updated_at": "2025-10-22T11:00:00Z"
              },
              {
                  "id": 1,
                  "user": 1,
                  "user_email": "user@example.com",
                  "location": "London",
                  "date": "2025-10-25",
                  "prediction_result": "Rain",
                  "confidence": 0.75,
                  "weather_data": {...},
                  "created_at": "2025-10-22T10:30:00Z",
                  "updated_at": "2025-10-22T10:30:00Z"
              }
          ]
      }
  }
  ```
- **CURL Command:**
  ```bash
  curl -X GET http://localhost:8000/api/history/ \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
  ```

#### 5. Get User Profile
- **URL:** `/api/profile/`
- **Method:** `GET`
- **Authentication:** Bearer Token required
- **Success Response (200 OK):**
  ```json
  {
      "success": true,
      "data": {
          "user": {
              "id": 1,
              "email": "user@example.com",
              "username": "user@example.com",
              "date_joined": "2025-10-22T09:00:00Z"
          }
      }
  }
  ```
- **CURL Command:**
  ```bash
  curl -X GET http://localhost:8000/api/profile/ \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
  ```

## Database Schema

### User Model (Django Built-in)
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password` (Hashed)
- `date_joined`

### PredictionRequest Model
- `id` (Primary Key)
- `user` (Foreign Key to User)
- `location` (CharField, max 255)
- `date` (DateField)
- `prediction_result` (CharField, max 50)
- `confidence` (FloatField)
- `weather_data` (JSONField)
- `created_at` (DateTimeField, auto)
- `updated_at` (DateTimeField, auto)

## Technologies Used

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework 3.14.0** - API framework
- **djangorestframework-simplejwt 5.3.0** - JWT authentication
- **psycopg2-binary 2.9.9** - PostgreSQL adapter
- **django-cors-headers 4.3.0** - CORS handling
- **requests 2.31.0** - HTTP library for API calls

### Frontend
- **React 18.2.0** - UI library
- **React Router DOM 6.20.0** - Routing
- **Axios 1.6.2** - HTTP client

### External API
- **Open-Meteo API** - Free, open-source weather API (no authentication required)
  - https://open-meteo.com/

## Key Features Implementation

### 1. Class-Based Views
All views in the backend use Django REST Framework's `APIView` class:
- `SignupView` - User registration
- `LoginView` - User authentication
- `PredictView` - Rain prediction
- `HistoryView` - Prediction history
- `UserProfileView` - User profile

### 2. JWT Authentication
- Token-based authentication using `djangorestframework-simplejwt`
- Access token lifetime: 1 day
- Refresh token lifetime: 7 days
- Tokens stored in localStorage on frontend

### 3. Database Configuration
- PostgreSQL database configuration loaded from `config.json`
- All credentials secured in config file
- Database indexes on frequently queried fields

### 4. Weather Prediction Service
- Uses Open-Meteo API (free, no authentication required)
- Geocoding service to convert location names to coordinates
- Weather forecast retrieval
- Rain prediction based on precipitation data and weather codes

### 5. Request Tracking
- Every prediction request is saved to the database
- Associated with the authenticated user
- Includes full weather data for historical reference

## Testing the Application

1. **Start both servers** (backend on port 8000, frontend on port 3000)
2. **Open browser** and navigate to http://localhost:3000
3. **Sign up** with a new account
4. **Login** with your credentials
5. **Make predictions** by entering a location and date
6. **View history** of all your predictions

## Development Notes

- Backend uses class-based views (CBV) instead of function-based views as per requirements
- All database credentials are stored in `config.json`
- Open-Meteo API is used as the weather prediction source (free and open-source)
- JWT tokens are used for authentication
- CORS is configured to allow requests from React frontend
- PostgreSQL is used for production-grade data storage
