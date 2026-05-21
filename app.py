from flask import Flask
from flask_login import LoginManager
import os
import urllib.parse

from models import db, User

from routs.public_routes import public_bp
from routs.auth_routes import auth_bp
from routs.customer_routes import customer_bp
from routs.admin_routes import admin_bp

from seed import seed_data

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hotel_secret_key_2024')

db_server = os.environ.get('DB_SERVER', r'(localdb)\mssqllocaldb')
db_name = os.environ.get('DB_NAME', 'HotelBooking')
db_user = os.environ.get('DB_USER', '')
db_password = os.environ.get('DB_PASSWORD', '')

if db_user and db_password:
    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={db_server};"
        f"DATABASE={db_name};"
        f"UID={db_user};"
        f"PWD={db_password};"
        "TrustServerCertificate=yes;"
    )
else:
    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={db_server};"
        f"DATABASE={db_name};"
        "Trusted_Connection=yes;"
    )

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(admin_bp)


seed_data(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)