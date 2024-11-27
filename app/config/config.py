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

    # Secret key for sessions and cookies with a default if not set
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
