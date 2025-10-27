# GetYourGuide Clone

A full-stack web application clone of GetYourGuide.com built with FastAPI (backend) and Next.js (frontend).

## Project Structure

```
site-get-your-guide/
├── backend/           # FastAPI backend application
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── init_db.py    # Database initialization with demo data
│   └── requirements.txt
└── frontend/          # Next.js frontend application
    ├── app/          # Next.js pages (App Router)
    ├── components/   # React components
    ├── lib/          # Utilities and API client
    └── types/        # TypeScript type definitions
```

## Features

### Customer Features ✅
- **Homepage**: Hero search, featured destinations, categories, bestselling activities
- **Search & Browse**: Advanced filters (price, duration, rating, features), sorting, pagination
- **Activity Details**: Image gallery, highlights, inclusions, meeting point, FAQs, booking widget
- **Booking Flow**: Date/participant selection, cart management, checkout
- **User Account**: Registration, login, profile management, booking history
- **Destinations**: Browse destinations, destination detail pages

### Backend Features ✅
- **Authentication**: JWT-based auth with refresh tokens
- **Activities API**: Search, filter, sort, CRUD operations
- **Booking System**: Create bookings, view booking history
- **Shopping Cart**: Session-based cart (no auth required)
- **Reviews**: Activity reviews and ratings
- **Wishlist**: Save favorite activities
- **Multi-role Support**: Customer, Vendor, Admin roles

### Vendor Portal 🚧 (Pending)
- Activity management dashboard
- Booking management
- Analytics and reports

### Admin Dashboard 🚧 (Pending)
- User management
- Activity approval workflow
- Platform analytics

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Authentication**: JWT with python-jose
- **Password Hashing**: passlib with bcrypt
- **Migrations**: Alembic
- **Validation**: Pydantic

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **State Management**: React Hooks
- **Icons**: Lucide React

## Setup Instructions

### Prerequisites
- Python 3.12.8
- Node.js 18+
- PostgreSQL 14+
- pyenv (for Python virtual environment)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment** (using pyenv):
   ```bash
   pyenv virtualenv 3.12.8 getyourguide
   pyenv local getyourguide
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database** (create `.env` file):
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/getyourguide
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Initialize database**:
   ```bash
   python init_db.py
   ```

6. **Start backend server**:
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

Frontend will be available at: http://localhost:3000

## Demo Data

The `init_db.py` script creates demo data including:

- **5 Demo Vendors**
- **12 Categories**: Tours, Museums, Day Trips, Water Sports, Outdoor Activities, Food & Drink, Cruises, Transport, Shows & Entertainment, Adventure Sports, Cultural Experiences, Nature & Wildlife
- **10+ Destinations**: Paris, London, Rome, Barcelona, Amsterdam, Berlin, Prague, Vienna, Lisbon, Athens
- **50+ Activities** across various categories and destinations

### Demo Accounts

```
Admin Account:
- Email: admin@getyourguide.com
- Password: admin123

Customer Account:
- Email: customer@example.com
- Password: customer123

Vendor Accounts:
- Email: vendor1@example.com - vendor5@example.com
- Password: vendor123
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT tokens
- `GET /api/v1/auth/me` - Get current user profile
- `PUT /api/v1/auth/me` - Update user profile

### Activities
- `GET /api/v1/activities` - Search and filter activities
- `GET /api/v1/activities/{id}` - Get activity details
- `GET /api/v1/activities/slug/{slug}` - Get activity by slug
- `POST /api/v1/activities` - Create activity (vendor/admin only)
- `PUT /api/v1/activities/{id}` - Update activity
- `DELETE /api/v1/activities/{id}` - Delete activity

### Bookings
- `GET /api/v1/bookings` - List user bookings
- `GET /api/v1/bookings/{id}` - Get booking details
- `POST /api/v1/bookings` - Create new booking
- `PUT /api/v1/bookings/{id}` - Update booking
- `DELETE /api/v1/bookings/{id}` - Cancel booking

### Cart
- `GET /api/v1/cart` - List cart items
- `POST /api/v1/cart` - Add item to cart
- `DELETE /api/v1/cart/{id}` - Remove item from cart
- `GET /api/v1/cart/total` - Get cart totals

### Categories & Destinations
- `GET /api/v1/categories` - List all categories
- `GET /api/v1/destinations` - List all destinations
- `GET /api/v1/destinations/featured` - Get featured destinations

### Reviews
- `GET /api/v1/activities/{id}/reviews` - List activity reviews
- `POST /api/v1/activities/{id}/reviews` - Create review
- `PUT /api/v1/reviews/{id}` - Update review
- `DELETE /api/v1/reviews/{id}` - Delete review

## Design System

### Colors
- **Primary**: #FC6500 (GetYourGuide Orange)
- **Primary Hover**: #E55A00
- **Success**: #10B981
- **Background**: #F9FAFB

### Typography
- **Font**: System fonts (-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto)
- **Base Size**: 16px

### Components
- Rounded corners (8px standard)
- Shadow elevation system
- Consistent spacing (4px grid)

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests (if configured)
cd frontend
npm test
```

### Code Quality
```bash
# Backend
black .
flake8 .

# Frontend
npm run lint
```

## Database Schema

### Core Tables
- **users**: User accounts (customers, vendors, admins)
- **vendors**: Vendor profiles
- **categories**: Activity categories
- **destinations**: Travel destinations
- **activities**: Activity listings
- **bookings**: Booking records
- **reviews**: Activity reviews
- **cart_items**: Shopping cart items
- **wishlist**: User wishlists

### Relationships
- Activities belong to vendors
- Activities have many categories (many-to-many)
- Activities have many destinations (many-to-many)
- Bookings belong to users and activities
- Reviews belong to users and activities

## Features Roadmap

### Phase 1: Core Features ✅ (Completed)
- Homepage and navigation
- Activity search and filtering
- Activity detail pages
- Booking flow and cart
- User authentication
- Customer dashboard

### Phase 2: Additional Features 🚧 (In Progress)
- Vendor portal
- Admin dashboard
- Payment integration
- Email notifications
- Multi-language support

### Phase 3: Advanced Features 📋 (Planned)
- Real-time availability
- Dynamic pricing
- Mobile app
- Social features
- Recommendation engine

## Contributing

This is a learning/demo project. Feel free to fork and experiment!

## License

This project is for educational purposes only. GetYourGuide is a registered trademark of GetYourGuide AG.

## Acknowledgments

- Inspired by [GetYourGuide.com](https://www.getyourguide.com)
- Built with FastAPI and Next.js
- Design system based on GetYourGuide's branding