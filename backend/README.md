# GetYourGuide Clone - Backend

FastAPI backend for the GetYourGuide clone project.

## Setup Instructions

### 1. Prerequisites

- Python 3.11+
- PostgreSQL (via Docker or local installation)
- pip or poetry

### 2. Database Setup

Start PostgreSQL using Docker Compose:

```bash
cd .. # Go to project root
docker-compose up -d postgres
```

This will start PostgreSQL on port 5432 with:
- Database: `getyourguide`
- Username: `postgres`
- Password: `password`

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or with virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

The default `.env` file is already configured to work with the Docker PostgreSQL.

### 5. Initialize Database

Run the initialization script to create tables and demo data:

```bash
python init_db.py
```

This will create:
- Database tables
- Admin user: `admin@getyourguide.com` / `admin123`
- Customer user: `customer@example.com` / `customer123`
- 5 Vendor accounts: `vendor1-5@example.com` / `vendor123`
- 10 destinations (cities)
- 8 categories
- 25+ sample activities

### 6. Run the Backend

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Or:

```bash
python -m app.main
```

The backend will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## API Documentation

### Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Main Endpoints

#### Auth Endpoints
- `POST /api/v1/auth/register` - Register new customer
- `POST /api/v1/auth/register-vendor` - Register new vendor
- `POST /api/v1/auth/login` - Login (returns JWT tokens)
- `GET /api/v1/auth/me` - Get current user profile
- `POST /api/v1/auth/refresh` - Refresh access token

#### Activity Endpoints (Coming soon)
- `GET /api/v1/activities` - List activities with filters
- `GET /api/v1/activities/{id}` - Get activity details
- `POST /api/v1/activities` - Create activity (vendor only)
- `PUT /api/v1/activities/{id}` - Update activity (vendor only)

#### Booking Endpoints (Coming soon)
- `POST /api/v1/bookings` - Create booking
- `GET /api/v1/bookings/my` - Get user's bookings
- `GET /api/v1/bookings/{ref}` - Get booking details

## Testing

Test the authentication endpoints:

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "customer123"
  }'
```

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── deps.py         # API dependencies
│   │   └── v1/            # API v1 endpoints
│   │       └── auth.py    # Authentication endpoints
│   ├── core/
│   │   └── security.py   # JWT and password utilities
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── config.py        # App configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI application
├── init_db.py           # Database initialization
├── requirements.txt     # Python dependencies
└── .env                # Environment variables
```

## Development

### Adding New Endpoints

1. Create schema in `app/schemas/`
2. Create API route in `app/api/v1/`
3. Add business logic in `app/services/`
4. Include router in `app/main.py`

### Database Migrations

For production, use Alembic for database migrations:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running: `docker-compose ps`
- Check DATABASE_URL in `.env` file
- Verify PostgreSQL is accessible on port 5432

### Import Errors
- Ensure you're in the correct virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use
- Change the PORT in `.env` file
- Or stop the process using port 8000