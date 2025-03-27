from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.routes.authRoutes import auth_bp
from app.routes.clientRoutes import client_bp
from app.routes.freelancerRoutes import freelancer_bp
import os  # Import os to generate a random secret key

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'sureConnectPython',
    'host': 'localhost',
    'port': 27017
}
app.config['JWT_SECRET_KEY'] = os.urandom(24)  # Set a random JWT secret key
app.secret_key = os.urandom(24)  # Set a random secret key for sessions

db = MongoEngine(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(client_bp, url_prefix='/api/clients')
app.register_blueprint(freelancer_bp, url_prefix='/api/freelancers')