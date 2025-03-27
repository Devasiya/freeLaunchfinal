# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    # MongoDB Connection URI
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/freelaunch'

    # Secret key for sessions and JWT
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'

    # Debug mode (set to False in production)
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'