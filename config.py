import os

class Config:
    SECRET_KEY = ''  # Replace with a secure secret key
    # For development, using SQLite; in production, consider PostgreSQL/MySQL.
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:yourpassword@localhost/spotify_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
