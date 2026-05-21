# LuxeStay — Hotel Booking System

A full-stack hotel booking web application built with Flask, SQLAlchemy, and Bootstrap.

## Technologies
- **Backend:** Flask (Python)
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Frontend:** HTML + CSS + Bootstrap 5
- **Authentication:** Flask-Login + Werkzeug password hashing

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python app.py

# 3. Open browser at:
http://localhost:5000
```

## Default Admin Account
- **Email:** admin@hotel.com
- **Password:** admin123

## Endpoints (12 total)

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/login` | User login |
| `/register` | User registration |
| `/logout` | Logout |
| `/rooms` | Browse all rooms + search by type |
| `/room/<id>` | Room details |
| `/book/<id>` | Book a room (customer) |
| `/my-bookings` | View my bookings (customer) |
| `/cancel-booking/<id>` | Cancel a booking |
| `/dashboard` | Admin dashboard |
| `/add-room` | Add new room (admin) |
| `/edit-room/<id>` | Edit room (admin) |
| `/delete-room/<id>` | Delete room (admin) |

## Database Schema (ERD)

```
Users (1) ──────── (*) Bookings (*) ──────── (1) Rooms
  id                     id                       id
  username               user_id (FK)             room_number
  email                  room_id (FK)             room_type
  password               check_in                 price
  role                   check_out                capacity
                         total_price              status
                         status                   description
                                                  image
```

## Folder Structure

```
hotel_booking/
├── app.py              # Main Flask application
├── models.py           # SQLAlchemy models
├── requirements.txt
├── database.db         # Auto-generated on first run
└── templates/
    ├── base.html       # Base layout
    ├── home.html       # Landing page
    ├── login.html      # Login form
    ├── register.html   # Registration form
    ├── rooms.html      # Room listing + search
    ├── room_details.html  # Single room view
    ├── book.html       # Booking form
    ├── my_bookings.html   # Customer bookings
    ├── dashboard.html  # Admin dashboard
    ├── add_room.html   # Add room form
    └── edit_room.html  # Edit room form
```
