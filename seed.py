import os
import time
import pyodbc
from werkzeug.security import generate_password_hash
from models import db, User, Room

def create_database_if_not_exists():
    
    db_server = os.environ.get('DB_SERVER', 'db')
    db_name = os.environ.get('DB_NAME', 'HotelBooking')
    db_user = os.environ.get('DB_USER', 'sa')
    db_password = os.environ.get('DB_PASSWORD', '') 

    if not db_user or not db_password:
        return

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={db_server};"
        "DATABASE=master;"
        f"UID={db_user};"
        f"PWD={db_password};"
        "TrustServerCertificate=yes;"
    )

    retries = 5
    while retries > 0:
        try:
            conn = pyodbc.connect(conn_str, autocommit=True)
            cursor = conn.cursor()
            
            cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{db_name}') CREATE DATABASE {db_name}")
            
            cursor.close()
            conn.close()
            print(f"Database '{db_name}' checked/created successfully!")
            break
        except Exception as e:
            print(f"Waiting for SQL Server to be ready... ({retries} retries left)")
            retries -= 1
            time.sleep(3)

def seed_data(app):
    create_database_if_not_exists()

    with app.app_context():
        db.create_all() 

        if not User.query.filter_by(role='admin').first():
            admin = User(
                username='admin',
                email='admin@hotel.com',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)

        if Room.query.count() == 0:
            rooms = [
                Room(room_number='101', room_type='Single', price=80, capacity=1,
                     description='A cozy single room with garden view.', image='https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=600'),
                Room(room_number='102', room_type='Double', price=130, capacity=2,
                     description='Spacious double room with city view.', image='https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=600'),
                Room(room_number='201', room_type='Suite', price=250, capacity=4,
                     description='Luxury suite with panoramic views and jacuzzi.', image='https://images.unsplash.com/photo-1590490360182-c33d57733427?w=600'),
                Room(room_number='202', room_type='Double', price=140, capacity=2,
                     description='Premium double room with king-size bed.', image='https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=600'),
                Room(room_number='301', room_type='Single', price=75, capacity=1,
                     description='Compact single room, perfect for solo travelers.', image='https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=600'),
                Room(room_number='302', room_type='Suite', price=300, capacity=6,
                     description='Executive suite with private lounge and butler service.', image='https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=600'),
            ]
            db.session.add_all(rooms)

        db.session.commit()