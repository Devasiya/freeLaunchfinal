# app/__init__.py

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.routes.authRoutes import auth_bp  # Import the auth blueprint

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database_name',
    'host': 'localhost',
    'port': 27017
}
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key

db = MongoEngine(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Register the auth blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')