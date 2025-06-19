# Django REST API with Authentication

A Django REST API project with email-based authentication using Django REST Framework.

## Features

- **Email-based Login**: Login using email and password
- **User Registration**: Create new user accounts
- **Token Authentication**: Secure API access using tokens
- **Logout Functionality**: Invalidate user tokens
- **CORS Support**: Cross-origin resource sharing enabled

## Setup Instructions

### 1. Install Dependencies

```bash
# Activate virtual environment
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install requirements
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Start Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

## API Endpoints

### Base URL

```
http://localhost:8000/api/auth/
```

### 1. User Registration

**POST** `/register/`

**Request Body:**

```json
{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**Response:**

```json
{
  "token": "your_auth_token",
  "user_id": 1,
  "username": "your_username",
  "email": "your_email@example.com",
  "message": "User created successfully"
}
```

### 2. User Login

**POST** `/login/`

**Request Body:**

```json
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**Response:**

```json
{
  "token": "your_auth_token",
  "user_id": 1,
  "username": "your_username",
  "email": "your_email@example.com",
  "message": "Login successful"
}
```

### 3. User Logout

**POST** `/logout/`

**Headers:**

```
Authorization: Token your_auth_token
```

**Response:**

```json
{
  "message": "Logout successful"
}
```

## Testing the API

### Using the Test Script

1. Install requests library:

```bash
pip install requests
```

2. Run the test script:

```bash
python test_api.py
```

### Using curl

**Register a new user:**

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
```

**Login:**

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

**Logout:**

```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Token your_token_here"
```

### Using Postman

1. **Register**: POST `http://localhost:8000/api/auth/register/`

   - Body (JSON): `{"username": "testuser", "email": "test@example.com", "password": "testpass123"}`

2. **Login**: POST `http://localhost:8000/api/auth/login/`

   - Body (JSON): `{"email": "test@example.com", "password": "testpass123"}`

3. **Logout**: POST `http://localhost:8000/api/auth/logout/`
   - Headers: `Authorization: Token your_token_here`

## Project Structure

```
pos_project/
├── app/
│   ├── views.py          # Authentication views
│   ├── urls.py           # App URL configuration
│   └── ...
├── pos_project/
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── ...
├── manage.py
├── requirements.txt
├── test_api.py
└── README.md
```

## Security Notes

- This is a development setup with `DEBUG = True`
- CORS is set to allow all origins for development
- For production, update settings accordingly
- Use HTTPS in production
- Implement proper password validation
- Consider rate limiting for login attempts

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to manage users and tokens.

## Next Steps

- Add password reset functionality
- Implement email verification
- Add user profile management
- Implement role-based permissions
- Add API documentation with drf-yasg or drf-spectacular
