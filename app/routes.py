# app/routes.py
from flask import render_template, current_app, send_from_directory, abort, Blueprint
from app.models import Song

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html', disable_player=True)

@main_bp.route('/dashboard')
def dashboard():
    songs = Song.query.all()
    # Pass disable_player=True to disable global controls on dashboard if desired.
    return render_template('dashboard.html', songs=songs, disable_player=True)

@main_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main_bp.route('/now_playing/<int:song_id>')
def now_playing(song_id):
    song = Song.query.get_or_404(song_id)
    return render_template('now_playing.html', song=song)
