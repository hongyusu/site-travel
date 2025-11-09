# FindTravelMate - Project Requirements Document

## Table of Contents

1. [Project Overview](#project-overview)
2. [Feature Specifications](#feature-specifications)
3. [Technical Architecture](#technical-architecture)
4. [Database Schema](#database-schema)
5. [API Documentation](#api-documentation)
6. [UI/UX Specifications](#uiux-specifications)
7. [User Flows](#user-flows)
8. [Implementation Plan](#implementation-plan)
9. [Demo Data Strategy](#demo-data-strategy)
10. [Success Criteria](#success-criteria)

---

## Project Overview

### Scope

- **Full marketplace functionality**: Browse, search, book activities
- **Multi-user system**: Customers, Vendors, Admins
- **No payment processing initially**: Mock checkout (Stripe integration later)
- **English only**: No multi-language support
- **EUR currency only**: No currency conversion
- **Desktop & Mobile responsive**: Match FindTravelMate's design

### Key Statistics (from FindTravelMate)

- 150,000+ experiences
- 12,000+ cities worldwide
- 30,000+ experience partners (vendors)
- 200+ million tickets sold

---

## Feature Specifications

### 1. Public Features (No Login Required)

#### 1.1 Homepage

- **Hero Section**
  - Background image with overlay
  - Tagline: "Travel memories you'll never forget"
  - Search widget:
    - Destination autocomplete input
    - Date picker
    - Search button
- **Popular Destinations**: 6-8 city cards with images
- **Top Categories**: Icons + labels (Tours, Museums, Day Trips, etc.)
- **Featured Activities**: Horizontal scrollable carousel
- **Trust Indicators**: "200M+ tickets sold", star ratings

#### 1.2 Search & Browse Page (`/s/{destination}`)

- **Search Bar**: Persistent at top with destination and date
- **Results Header**: "1,234 things to do in {destination}"
- **Sort Dropdown**: Recommended, Price (low/high), Rating, Duration
- **Filter Sidebar** (left):
  - Price range slider (€0-500+)
  - Duration checkboxes
  - Time of day
  - Categories (multi-select)
  - Rating (4+ stars)
  - Features (free cancellation, skip-the-line)
- **Activity Cards**:
  - Image (with gallery indicator)
  - Title (max 2 lines)
  - Duration badge
  - Rating + review count
  - Price "From €XX"
  - Badges (Bestseller, Free cancellation)
- **Pagination**: Load more button

#### 1.3 Activity Detail Page (`/activity/{id}`)

- **Breadcrumbs**: Home > City > Category > Activity
- **Title Section**: H1 title + quick stats
- **Image Gallery**: Main image + thumbnails
- **Sticky Booking Widget** (right side):
  - Date calendar picker
  - Time slots (if applicable)
  - Participants selector
  - Price breakdown
  - "Check availability" button
  - "Free cancellation" notice
- **Content Sections**:
  - Overview (bullet points)
  - What's included/excluded
  - Meeting point (map embed)
  - Important information
  - Reviews section
  - FAQs
- **Similar Activities**: Bottom carousel

#### 1.4 Destination Pages (`/destinations/{city}`)

- City hero image
- Top attractions
- Categories specific to city
- All activities link

### 2. Customer Features (Login Required)

#### 2.1 Authentication

- **Register**: Email, password, full name
- **Login**: Email + password
- **Guest Checkout**: Optional for bookings

#### 2.2 Booking Flow

- **Cart** (`/cart`):
  - List of activities
  - Edit dates/participants
  - Remove items
  - Price summary
  - Continue to checkout
- **Checkout** (`/checkout`):
  - Contact details
  - Traveler information
  - Payment section (mock)
  - Terms acceptance
  - Complete booking button
- **Confirmation**:
  - Booking reference
  - QR code (mock)
  - Email confirmation

#### 2.3 Account Dashboard (`/my-account`)

- **My Bookings**: Upcoming & past
- **Wishlist**: Saved activities
- **Profile**: Edit personal info
- **Settings**: Preferences

### 3. Vendor Features (`/partner`)

#### 3.1 Vendor Registration

- Business information form
- Verification (manual by admin)
- Commission agreement

#### 3.2 Vendor Dashboard

- **Overview**:
  - Today's bookings
  - Revenue (mock)
  - Recent reviews
  - Quick stats
- **Activity Management**:
  - List all activities
  - Create/Edit activity:
    - Basic info (title, description)
    - Images (multiple)
    - Pricing (per person/group)
    - Duration
    - Languages offered
    - Category selection
    - Meeting point
    - What's included/excluded
    - Availability calendar
    - Cancellation policy
- **Bookings**:
  - Calendar view
  - List view with filters
  - Customer details
  - Check-in functionality
- **Analytics**:
  - Booking trends
  - Popular activities
  - Customer demographics

### 4. Admin Features (`/admin`)

#### 4.1 Dashboard

- Platform statistics
- Recent activity
- Alerts/issues

#### 4.2 Management

- **Users**: View/edit customers and vendors
- **Activities**: Approve/reject, featured selection
- **Bookings**: View all, handle issues
- **Reviews**: Moderation
- **Categories**: Add/edit/delete
- **Destinations**: Manage cities

#### 4.3 Settings

- Platform configuration
- Commission rates
- Email templates

---

## Technical Architecture

### Technology Stack

#### Backend (Python/FastAPI)

```
- FastAPI 0.104+
- Python 3.11+
- PostgreSQL 15+
- SQLAlchemy 2.0 (ORM)
- Alembic (migrations)
- Pydantic (validation)
- JWT (authentication)
- Uvicorn (ASGI server)
- Redis (caching - optional)
```

#### Frontend (Next.js/TypeScript)

```
- Next.js 14+ (App Router)
- TypeScript 5+
- React 18+
- Tailwind CSS 3+
- shadcn/ui components
- React Query (data fetching)
- React Hook Form (forms)
- Zod (validation)
```

### Project Structure

```
site-get-your-guide/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Settings
│   │   ├── database.py          # DB connection
│   │   │
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── activity.py
│   │   │   ├── booking.py
│   │   │   ├── vendor.py
│   │   │   ├── review.py
│   │   │   └── destination.py
│   │   │
│   │   ├── schemas/             # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── activity.py
│   │   │   ├── booking.py
│   │   │   └── common.py
│   │   │
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── activities.py
│   │   │       ├── bookings.py
│   │   │       ├── search.py
│   │   │       ├── reviews.py
│   │   │       ├── vendors.py
│   │   │       ├── admin.py
│   │   │       └── deps.py      # Dependencies
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py     # JWT, passwords
│   │   │   ├── email.py        # Email service
│   │   │   └── storage.py      # File uploads
│   │   │
│   │   └── services/            # Business logic
│   │       ├── __init__.py
│   │       ├── booking_service.py
│   │       ├── search_service.py
│   │       └── availability_service.py
│   │
│   ├── alembic/                 # DB migrations
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── app/                     # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx             # Homepage
│   │   ├── globals.css
│   │   │
│   │   ├── s/
│   │   │   └── [destination]/
│   │   │       └── page.tsx    # Search results
│   │   │
│   │   ├── activity/
│   │   │   └── [id]/
│   │   │       └── page.tsx    # Activity detail
│   │   │
│   │   ├── destinations/
│   │   │   └── [slug]/
│   │   │       └── page.tsx    # City page
│   │   │
│   │   ├── cart/
│   │   │   └── page.tsx
│   │   │
│   │   ├── checkout/
│   │   │   └── page.tsx
│   │   │
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── register/
│   │   │
│   │   ├── (account)/
│   │   │   ├── my-account/
│   │   │   ├── bookings/
│   │   │   └── wishlist/
│   │   │
│   │   ├── partner/             # Vendor portal
│   │   │   ├── dashboard/
│   │   │   ├── activities/
│   │   │   ├── bookings/
│   │   │   └── analytics/
│   │   │
│   │   └── admin/               # Admin panel
│   │       ├── dashboard/
│   │       ├── users/
│   │       ├── activities/
│   │       └── settings/
│   │
│   ├── components/
│   │   ├── ui/                  # shadcn components
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Navigation.tsx
│   │   ├── search/
│   │   │   ├── SearchBar.tsx
│   │   │   ├── FilterSidebar.tsx
│   │   │   └── ActivityCard.tsx
│   │   ├── booking/
│   │   │   ├── BookingWidget.tsx
│   │   │   ├── DatePicker.tsx
│   │   │   └── ParticipantSelector.tsx
│   │   └── common/
│   │       ├── RatingStars.tsx
│   │       ├── PriceDisplay.tsx
│   │       └── ImageGallery.tsx
│   │
│   ├── lib/
│   │   ├── api-client.ts        # API communication
│   │   ├── auth.ts              # Auth helpers
│   │   ├── utils.ts
│   │   └── constants.ts
│   │
│   ├── types/
│   │   ├── activity.ts
│   │   ├── booking.ts
│   │   ├── user.ts
│   │   └── api.ts
│   │
│   ├── public/
│   │   └── images/
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── next.config.js
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Database Schema

### Users & Authentication

```sql
-- Users table (customers, vendors, admins)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    role VARCHAR(20) DEFAULT 'customer', -- customer, vendor, admin
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Vendors table (extends users)
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    description TEXT,
    logo_url VARCHAR(500),
    commission_rate DECIMAL(5,2) DEFAULT 20.00, -- percentage
    is_verified BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Activities & Content

```sql
-- Categories
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(50),
    parent_id INTEGER REFERENCES categories(id),
    order_index INTEGER DEFAULT 0
);

-- Destinations
CREATE TABLE destinations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    country VARCHAR(100),
    country_code VARCHAR(2),
    image_url VARCHAR(500),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Activities
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    vendor_id INTEGER REFERENCES vendors(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE NOT NULL,
    description TEXT,
    short_description TEXT,
    price_adult DECIMAL(10, 2) NOT NULL,
    price_child DECIMAL(10, 2),
    price_currency VARCHAR(3) DEFAULT 'EUR',
    duration_minutes INTEGER,
    max_group_size INTEGER,
    instant_confirmation BOOLEAN DEFAULT TRUE,
    free_cancellation_hours INTEGER DEFAULT 24,
    languages TEXT[], -- Array of language codes
    is_bestseller BOOLEAN DEFAULT FALSE,
    is_skip_the_line BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Activity Images
CREATE TABLE activity_images (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    alt_text VARCHAR(255),
    is_primary BOOLEAN DEFAULT FALSE,
    order_index INTEGER DEFAULT 0
);

-- Activity Categories (many-to-many)
CREATE TABLE activity_categories (
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (activity_id, category_id)
);

-- Activity Destinations (many-to-many)
CREATE TABLE activity_destinations (
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    destination_id INTEGER REFERENCES destinations(id) ON DELETE CASCADE,
    PRIMARY KEY (activity_id, destination_id)
);

-- Activity Highlights
CREATE TABLE activity_highlights (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    text VARCHAR(500) NOT NULL,
    order_index INTEGER DEFAULT 0
);

-- Activity Includes/Excludes
CREATE TABLE activity_includes (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    item VARCHAR(500) NOT NULL,
    is_included BOOLEAN DEFAULT TRUE, -- true for included, false for excluded
    order_index INTEGER DEFAULT 0
);

-- Activity FAQs
CREATE TABLE activity_faqs (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    order_index INTEGER DEFAULT 0
);

-- Meeting Points
CREATE TABLE meeting_points (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    address TEXT NOT NULL,
    instructions TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);
```

### Booking System

```sql
-- Bookings
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    booking_ref VARCHAR(20) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    activity_id INTEGER REFERENCES activities(id),
    vendor_id INTEGER REFERENCES vendors(id),
    booking_date DATE NOT NULL,
    booking_time TIME,
    adults INTEGER DEFAULT 1,
    children INTEGER DEFAULT 0,
    total_participants INTEGER NOT NULL,
    price_per_adult DECIMAL(10, 2),
    price_per_child DECIMAL(10, 2),
    total_price DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    status VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, cancelled, completed
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    customer_phone VARCHAR(50),
    special_requirements TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    confirmed_at TIMESTAMP,
    cancelled_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Availability
CREATE TABLE availability (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    spots_available INTEGER,
    spots_total INTEGER,
    price_adult DECIMAL(10, 2),
    price_child DECIMAL(10, 2),
    is_available BOOLEAN DEFAULT TRUE,
    UNIQUE(activity_id, date, start_time)
);

-- Cart Items (for session-based cart)
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    booking_date DATE NOT NULL,
    booking_time TIME,
    adults INTEGER DEFAULT 1,
    children INTEGER DEFAULT 0,
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_session (session_id)
);
```

### Reviews & Ratings

```sql
-- Reviews
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER REFERENCES bookings(id),
    user_id INTEGER REFERENCES users(id),
    activity_id INTEGER REFERENCES activities(id),
    vendor_id INTEGER REFERENCES vendors(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    comment TEXT,
    is_verified_booking BOOLEAN DEFAULT TRUE,
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Review Images
CREATE TABLE review_images (
    id SERIAL PRIMARY KEY,
    review_id INTEGER REFERENCES reviews(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    caption VARCHAR(255)
);
```

### Supporting Tables

```sql
-- Wishlist
CREATE TABLE wishlist (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, activity_id)
);

-- Email Templates
CREATE TABLE email_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    subject VARCHAR(500),
    body TEXT,
    variables TEXT[], -- List of available variables
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Platform Settings
CREATE TABLE settings (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Documentation

### Base URL

```
Development: http://localhost:8000/api/v1
Production: https://api.yourdomain.com/v1
```

### Authentication

```
POST   /auth/register       - User registration
POST   /auth/login          - User login
POST   /auth/refresh        - Refresh JWT token
POST   /auth/logout         - Logout
GET    /auth/me             - Get current user
```

### Activities

```
GET    /activities          - List activities (with filters)
GET    /activities/{id}     - Get activity details
POST   /activities          - Create activity (vendor)
PUT    /activities/{id}     - Update activity (vendor)
DELETE /activities/{id}     - Delete activity (vendor)
GET    /activities/{id}/availability - Get availability
POST   /activities/{id}/availability - Set availability (vendor)
```

### Search & Discovery

```
GET    /search              - Search activities
GET    /destinations        - List destinations
GET    /destinations/{slug} - Get destination details
GET    /categories          - List categories
GET    /featured            - Get featured activities
```

### Bookings

```
POST   /bookings            - Create booking
GET    /bookings/{ref}      - Get booking details
GET    /bookings/my         - My bookings (customer)
PUT    /bookings/{ref}      - Update booking
DELETE /bookings/{ref}      - Cancel booking
GET    /vendor/bookings     - Vendor bookings
PUT    /vendor/bookings/{id}/checkin - Check-in customer
```

### Reviews

```
GET    /activities/{id}/reviews - Get activity reviews
POST   /reviews             - Create review
PUT    /reviews/{id}        - Update review
DELETE /reviews/{id}        - Delete review
```

### Cart

```
GET    /cart                - Get cart items
POST   /cart/add            - Add to cart
PUT    /cart/update         - Update cart item
DELETE /cart/remove         - Remove from cart
DELETE /cart/clear          - Clear cart
```

### Vendor Portal

```
GET    /vendor/dashboard    - Dashboard stats
GET    /vendor/activities   - My activities
GET    /vendor/bookings     - My bookings
GET    /vendor/analytics    - Analytics data
PUT    /vendor/profile      - Update vendor profile
```

### Admin

```
GET    /admin/users         - List all users
PUT    /admin/users/{id}    - Update user
DELETE /admin/users/{id}    - Delete user
GET    /admin/vendors       - List vendors
PUT    /admin/vendors/{id}/verify - Verify vendor
GET    /admin/activities    - All activities
PUT    /admin/activities/{id}/feature - Feature activity
GET    /admin/bookings      - All bookings
GET    /admin/stats         - Platform statistics
```

### Response Format

```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Success message",
  "errors": null,
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### Error Response

```json
{
  "success": false,
  "data": null,
  "message": "Error message",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

---

## UI/UX Specifications

### Design System

#### Colors

```css
:root {
  /* Primary Colors */
  --primary-orange: #FC6500;      /* CTAs, buttons */
  --primary-orange-hover: #E55A00;

  /* Secondary Colors */
  --success-green: #0A8800;       /* Free cancellation badge */
  --info-blue: #0066CC;           /* Links */
  --warning-yellow: #FFC107;      /* Warnings */
  --danger-red: #DC3545;          /* Errors, urgent */

  /* Text Colors */
  --text-primary: #1A2B49;        /* Headers, main text */
  --text-secondary: #6B7280;      /* Descriptions */
  --text-muted: #9CA3AF;          /* Disabled, hints */

  /* Background Colors */
  --bg-white: #FFFFFF;
  --bg-gray-light: #F7F7F7;
  --bg-gray: #EEEEEE;

  /* Border Colors */
  --border-light: #E5E5E5;
  --border-default: #D1D5DB;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);
}
```

#### Typography

```css
/* Font Family */
--font-primary: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;

/* Font Sizes */
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 30px;
--text-4xl: 36px;

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

#### Spacing

```css
/* Spacing Scale */
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
--space-3xl: 64px;
```

#### Breakpoints

```css
/* Responsive Breakpoints */
--screen-sm: 640px;   /* Mobile landscape */
--screen-md: 768px;   /* Tablet */
--screen-lg: 1024px;  /* Desktop */
--screen-xl: 1280px;  /* Large desktop */
--screen-2xl: 1536px; /* Extra large */
```

### Component Specifications

#### Activity Card

```
- Dimensions: 100% width in grid
- Image: 16:9 aspect ratio
- Border radius: 8px
- Shadow on hover
- Content padding: 16px
- Title: 2 lines max, ellipsis
- Rating: Stars + number + count
- Price: Bold, primary color
- Badges: Rounded, small caps
```

#### Search Filter Sidebar

```
- Width: 280px desktop, full mobile
- Sticky position on scroll
- Collapsible sections
- Clear all filters button
- Apply button on mobile
```

#### Booking Widget

```
- Width: 380px desktop
- Sticky position: top 80px
- White background
- Border: 1px solid
- Shadow: medium
- Padding: 24px
- CTA button: Full width, primary color
```

#### Navigation Header

```
- Height: 64px
- White background
- Logo left aligned
- Search center (desktop)
- User menu right
- Mobile: Hamburger menu
```

---

## User Flows

### 1. Customer Booking Flow

```
1. Homepage
   └─> Search destination
       └─> Browse activities
           └─> View activity details
               └─> Select date/participants
                   └─> Add to cart
                       └─> View cart
                           └─> Checkout (login/guest)
                               └─> Enter details
                                   └─> Confirm booking
                                       └─> Receive confirmation
```

### 2. Vendor Activity Creation

```
1. Vendor login
   └─> Dashboard
       └─> Activities section
           └─> Create new activity
               └─> Fill basic info
                   └─> Add images
                       └─> Set pricing
                           └─> Define availability
                               └─> Add details
                                   └─> Submit for review
                                       └─> Admin approval
                                           └─> Activity live
```

### 3. Search & Filter Flow

```
1. Enter destination
   └─> View results
       └─> Apply filters
           ├─> Price range
           ├─> Duration
           ├─> Categories
           ├─> Rating
           └─> Features
               └─> Sort results
                   └─> Load more
                       └─> View activity
```

---

## Implementation Plan

### Phase 1: Backend Foundation (Day 1)

- [ ] Project setup & configuration
- [ ] Database schema creation
- [ ] User authentication system
- [ ] Basic CRUD APIs
- [ ] Search & filter logic

### Phase 2: Frontend Core (Day 2)

- [ ] Next.js setup
- [ ] Component library setup
- [ ] Homepage
- [ ] Search/browse page
- [ ] Activity detail page

### Phase 3: Booking System (Day 3)

- [ ] Cart functionality
- [ ] Checkout flow
- [ ] Booking management
- [ ] Email notifications (mock)

### Phase 4: Vendor Portal (Day 4)

- [ ] Vendor registration
- [ ] Activity management
- [ ] Booking management
- [ ] Basic analytics

### Phase 5: Admin & Polish (Day 5)

- [ ] Admin dashboard
- [ ] Content moderation
- [ ] Demo data generation
- [ ] Testing & bug fixes

---

## Demo Data Strategy

### Cities (10 destinations)

1. **Paris, France** - 200+ activities
2. **London, UK** - 180+ activities
3. **New York, USA** - 150+ activities
4. **Rome, Italy** - 170+ activities
5. **Tokyo, Japan** - 140+ activities
6. **Barcelona, Spain** - 160+ activities
7. **Dubai, UAE** - 130+ activities
8. **Amsterdam, Netherlands** - 120+ activities
9. **Prague, Czech Republic** - 110+ activities
10. **Istanbul, Turkey** - 125+ activities

### Categories Distribution

- **Tours & Sightseeing**: 30%
- **Museums & Attractions**: 20%
- **Day Trips**: 15%
- **Food & Drink**: 15%
- **Adventure & Nature**: 10%
- **Shows & Entertainment**: 5%
- **Transportation**: 5%

### Price Ranges

- Budget (€10-30): 25%
- Mid-range (€30-100): 50%
- Premium (€100-300): 20%
- Luxury (€300+): 5%

### Sample Vendors (5)

1. **City Explorer Tours** - Multi-city operator
2. **Local Flavors** - Food experiences
3. **Adventure Seekers** - Outdoor activities
4. **Cultural Connections** - Museums & history
5. **VIP Experiences** - Luxury tours

### Reviews

- Each activity: 10-50 reviews
- Rating distribution: 4.0-5.0 (weighted toward 4.5+)
- Mix of short and detailed reviews
- Some with photos

---

## Success Criteria

### Functional Requirements ✓

- [ ] Homepage with search functionality
- [ ] Browse page with working filters
- [ ] Activity detail pages with all sections
- [ ] Complete booking flow (without payment)
- [ ] User registration and login
- [ ] Vendor can create/edit activities
- [ ] Admin can moderate content
- [ ] Cart functionality works
- [ ] Responsive on mobile devices

### Visual Requirements ✓

- [ ] Matches FindTravelMate color scheme
- [ ] Similar layout and structure
- [ ] Activity cards look authentic
- [ ] Booking widget is sticky
- [ ] Filter sidebar works properly
- [ ] Image galleries function

### Performance Requirements ✓

- [ ] Page load < 3 seconds
- [ ] Search results < 1 second
- [ ] Smooth scrolling
- [ ] Images optimized
- [ ] No console errors

### Data Requirements ✓

- [ ] 10+ destinations available
- [ ] 100+ activities total
- [ ] Multiple categories
- [ ] Realistic pricing
- [ ] Sample reviews
- [ ] Demo bookings

### User Experience ✓

- [ ] Intuitive navigation
- [ ] Clear CTAs
- [ ] Error handling
- [ ] Loading states
- [ ] Empty states
- [ ] Success messages

---

## Notes & Considerations

### Future Enhancements (Post-MVP)

1. **Payment Integration**: Stripe/PayPal
2. **Email System**: SendGrid/AWS SES
3. **SMS Notifications**: Twilio
4. **Multi-language**: i18n support
5. **Currency Conversion**: Real-time rates
6. **Mobile Apps**: React Native
7. **Advanced Search**: Elasticsearch
8. **Real-time Chat**: Customer support
9. **AI Recommendations**: Personalization
10. **Social Login**: Google/Facebook

### Security Considerations

- JWT token expiration
- Password hashing (bcrypt)
- SQL injection prevention
- XSS protection
- CORS configuration
- Rate limiting
- Input validation
- File upload restrictions

### SEO Considerations

- Meta tags for all pages
- Sitemap generation
- Structured data (JSON-LD)
- Clean URLs
- Image alt texts
- Page load speed
- Mobile responsiveness

### Deployment

- Backend: Docker + AWS/DigitalOcean
- Frontend: Vercel/Netlify
- Database: PostgreSQL (managed)
- File storage: AWS S3/Cloudinary
- CDN: CloudFlare

---

## Contact & Support

For questions about this project:

- Documentation: This file (REQUIREMENTS.md)
- Technical decisions: See Technical Architecture section
- API details: See API Documentation section
- UI specifications: See UI/UX Specifications section

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Ready for Implementation
