from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.routes.authRoutes import auth_bp  # Import the auth blueprint
# from app.routes.clientRoutes import client_bp  # Import the client blueprint
# from app.routes.freelancerRoutes import freelancer_bp  # Import the freelancer blueprint

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'sureConnectPython',  # Replace with your actual database name
    'host': 'localhost',
    'port': 27017
}
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key

db = MongoEngine(app)  # Initialize MongoEngine once
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Register the blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(client_bp, url_prefix='/clients')
app.register_blueprint(freelancer_bp, url_prefix='/freelancers')