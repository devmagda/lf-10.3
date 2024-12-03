import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database configuration with defaults
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'dbdev')

    # Database URI for SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable unnecessary modifications tracking

    # Flask secret key for sessions and cookies
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')

    # Flask-specific configurations
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    TEMPLATES_AUTO_RELOAD = os.getenv('TEMPLATES_AUTO_RELOAD', 'False').lower() in ('true', '1', 't')
    SEND_FILE_MAX_AGE_DEFAULT = int(os.getenv('SEND_FILE_MAX_AGE_DEFAULT', 0))
