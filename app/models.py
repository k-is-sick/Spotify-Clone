from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import LONGBLOB, LONGTEXT

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100), nullable=False, default='Unknown')
    album = db.Column(db.String(100))
    # file_path stores only the filename; the full path is UPLOAD_FOLDER + filename
    file_path = db.Column(db.String(300), nullable=False)
    duration = db.Column(db.Float)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Use MySQL's LONGBLOB and LONGTEXT for larger data storage
    cover_art = db.Column(LONGBLOB, nullable=True)      # Store raw binary data of cover art (optional)
    cover_art_data_uri = db.Column(LONGTEXT, nullable=True)      # Store Base64 data URI of cover art for display

# Association table for many-to-many relationship between Playlist and Song
playlist_songs = db.Table('playlist_songs',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Song', secondary=playlist_songs, backref='playlists')
