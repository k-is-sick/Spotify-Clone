import os

class Config:
    SECRET_KEY = 'e8b13f1a6c7d8f4d9e6a2c3b5f7e1d9f3c2a8b4e5d6f1a2c7e9b0d5a4c3f8e7'  # Replace with a secure secret key
    # For development, using SQLite; in production, consider PostgreSQL/MySQL.
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:3301@localhost/spotify_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
