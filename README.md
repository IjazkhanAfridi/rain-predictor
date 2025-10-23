# Rain Prediction Application

A full-stack web application for predicting rain based on location and date. Built with Django REST Framework (backend) and React.js (frontend).

## 🌟 Features

- User authentication (Signup/Login) with JWT tokens
- Rain prediction using Open-Meteo API (free, open-source weather API)
- User-specific prediction history tracking
- PostgreSQL database for data persistence
- RESTful API with Class-Based Views
- Modern React UI with responsive design

## 📁 Project Structure

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

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
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
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```powershell
   python manage.py createsuperuser
   ```

7. **Start Django development server:**
   ```powershell
   python manage.py runserver
   ```
   Backend will run on http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory (new terminal):**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Start React development server:**
   ```powershell
   npm start
   ```
   Frontend will run on http://localhost:3000

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

## 🗄️ Database Schema

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

## 🔧 Technologies Used

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

## 🎯 Key Features Implementation

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

## 🧪 Testing the Application

1. **Start both servers** (backend on port 8000, frontend on port 3000)
2. **Open browser** and navigate to http://localhost:3000
3. **Sign up** with a new account
4. **Login** with your credentials
5. **Make predictions** by entering a location and date
6. **View history** of all your predictions

## 📝 Development Notes

- Backend uses class-based views (CBV) instead of function-based views as per requirements
- All database credentials are stored in `config.json`
- Open-Meteo API is used as the weather prediction source (free and open-source)
- JWT tokens are used for authentication
- CORS is configured to allow requests from React frontend
- PostgreSQL is used for production-grade data storage

## 🚢 Deployment Considerations

1. Change `DEBUG = False` in production
2. Update `ALLOWED_HOSTS` with your domain
3. Use environment variables for sensitive data
4. Set up proper PostgreSQL user with limited privileges
5. Use gunicorn or uwsgi for Django in production
6. Build React app with `npm run build`
7. Serve React build files with a web server (Nginx/Apache)

## 📄 License

This project is for educational purposes.

## 👥 Author

Developed as a full-stack web application demonstration project.

---

## 🔗 GitHub Repository

After pushing to GitHub, the repository will contain:
- Complete source code
- requirements.txt for backend dependencies
- package.json for frontend dependencies
- Comprehensive README with API documentation
- CURL commands for testing all endpoints
- Database schema documentation

To push to GitHub:
```powershell
git init
git add .
git commit -m "Initial commit: Rain prediction application"
git branch -M main
git remote add origin https://github.com/yourusername/rain-prediction-app.git
git push -u origin main
```
#   r a i n - p r e d i c t o r  
 