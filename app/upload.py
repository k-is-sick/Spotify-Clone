# app/upload.py
import os
from flask import Blueprint, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app.models import Song, db
from app.utils import extract_metadata, cover_art_to_data_uri

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check for file in request
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # Extract metadata using our utility function
            metadata = extract_metadata(file_path)
            cover_art_data_uri = cover_art_to_data_uri(metadata.get('cover_art'))
            
            # Create a new Song instance with the extracted metadata
            new_song = Song(
                title = metadata.get('title', 'Unknown Title'),
                artist = metadata.get('artist', 'Unknown Artist'),
                album = metadata.get('album', 'Unknown Album'),
                file_path = filename,  # storing only the filename; the full path is defined by UPLOAD_FOLDER
                duration = metadata.get('duration', 0),
                cover_art = metadata.get('cover_art'),
                cover_art_data_uri = cover_art_data_uri
            )
            db.session.add(new_song)
            db.session.commit()
            flash("Song uploaded and metadata extracted successfully!")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid file type")
            return redirect(request.url)
    # For GET, redirect to dashboard
    return redirect(url_for('main.dashboard'))
