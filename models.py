# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from datetime import datetime

# db = SQLAlchemy()

# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(20), default='customer')  # 'admin' or 'customer'
#     # bookings = db.relationship('Booking', backref='user', lazy=True)
#     bookings = db.relationship(
#     'Booking',
#     backref='user',
#     lazy=True,
#     cascade="all, delete"
# )

# class Room(db.Model):
#     __tablename__ = 'rooms'
#     id = db.Column(db.Integer, primary_key=True)
#     room_number = db.Column(db.String(10), unique=True, nullable=False)
#     room_type = db.Column(db.String(50), nullable=False)  # Single, Double, Suite, etc.
#     price = db.Column(db.Float, nullable=False)
#     capacity = db.Column(db.Integer, nullable=False)
#     status = db.Column(db.String(20), default='available')  # 'available' or 'booked'
#     description = db.Column(db.Text)
#     image = db.Column(db.String(200), default='default_room.jpg')
#     # bookings = db.relationship('Booking', backref='room', lazy=True)
#     bookings = db.relationship(
#     'Booking',
#     backref='room',
#     lazy=True,
#     cascade="all, delete"
# )

# class Booking(db.Model):
#     __tablename__ = 'bookings'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
#     check_in = db.Column(db.Date, nullable=False)
#     check_out = db.Column(db.Date, nullable=False)
#     total_price = db.Column(db.Float, nullable=False)
#     status = db.Column(db.String(20), default='pending')  # 'pending', 'confirmed', 'cancelled'
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer')

    bookings = db.relationship(
        'Booking',
        backref='user',
        lazy=True
    )


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='available')
    description = db.Column(db.Text)
    image = db.Column(db.String(200), default='default_room.jpg')

    bookings = db.relationship(
        'Booking',
        backref='room',
        lazy=True
    )


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey('rooms.id'),
        nullable=False
    )

    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    status = db.Column(
        db.String(20),
        default='pending'
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )