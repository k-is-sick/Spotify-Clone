import os
from werkzeug.utils import secure_filename
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.easyid3 import EasyID3
import base64
from mutagen import File

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, upload_folder):
    """Save the uploaded file securely and return its filename."""
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return filename


def extract_metadata(file_path):
    """
    Extracts metadata from an MP3 file.
    Returns a dictionary with keys: title, artist, album, and cover_art.
    cover_art is the binary data of the image (if found).
    """
    metadata = {}
    
    # Try to read basic ID3 tags using EasyID3
    try:
        audio = EasyID3(file_path)
        metadata['title'] = audio.get('title', ['Unknown Title'])[0]
        metadata['artist'] = audio.get('artist', ['Unknown Artist'])[0]
        metadata['album'] = audio.get('album', ['Unknown Album'])[0]
    except Exception as e:
        # If no ID3 tags are found, set default values
        metadata['title'] = 'Unknown Title'
        metadata['artist'] = 'Unknown Artist'
        metadata['album'] = 'Unknown Album'

    # Use mutagen.File to get duration
    audio_file = File(file_path)
    if audio_file and audio_file.info:
        metadata['duration'] = audio_file.info.length
    else:
        metadata['duration'] = 0
    
    # Try to extract cover art using ID3 APIC frames:
    try:
        id3 = ID3(file_path)
        apic_frames = id3.getall("APIC")
        if apic_frames:
            # Use the first APIC frame's data
            metadata['cover_art'] = apic_frames[0].data
        else:
            metadata['cover_art'] = None
    except Exception:
        metadata['cover_art'] = None
    
    return metadata

def cover_art_to_data_uri(cover_art_binary, mime_type="image/jpeg"):
    """
    Converts binary cover art data to a Base64 data URI.
    Returns a string like "data:image/jpeg;base64,..." or None if cover_art_binary is None.
    """
    if cover_art_binary:
        base64_str = base64.b64encode(cover_art_binary).decode("utf-8")
        return f"data:{mime_type};base64,{base64_str}"
    return None