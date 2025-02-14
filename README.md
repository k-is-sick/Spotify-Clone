# Spotify Clone

A web-based music streaming application built with Flask, SQLAlchemy, Flask-Migrate, Mutagen, and JavaScript. This project mimics basic Spotify functionality by allowing user authentication, song uploads with metadata extraction, and audio playback with custom controls.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [License](#license)

## Features

- **User Authentication:** Register, login, and logout.
- **Song Uploads:** Upload songs with automatic metadata extraction (title, artist, album, duration, cover art).
- **Audio Playback:** Global audio player with play/pause, next, previous, and seek controls.
- **Now Playing Page:** A dedicated page displaying the currently playing song with full details (cover art, title, artist, album) and its own control bar.
- **Responsive Design:** Clean, dark-themed UI that adapts to different screen sizes.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/k-is-sick/Spotify-Clone.git
cd spotify-clone
```

### 2. Create and Activate a Virtual Environment

- **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **On Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

## Database Setup

### 1. Configure the Application

Edit `config.py` and set your secret key, database URI, and upload folder. For example:

```python
import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///spotify_clone.db'  # or your MySQL URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
```

Make sure the folder specified by `UPLOAD_FOLDER` exists.

### 2. Initialize and Migrate the Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Running the Application

Start the Flask development server:

```bash
python run.py
```

The application should now be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Deployment

### Heroku Deployment

1. **Create a `Procfile`** in the root directory with the following content:

```
web: gunicorn run:app
```

2. **Deploy the Application:**

```bash
heroku create
git push heroku main
heroku run flask db upgrade
```

3. **Access Your Deployed Application:**  
Visit the URL provided by Heroku.

### Other Platforms (e.g., Render)

1. **Create a New Web Service:**  
Connect your GitHub repository and set the build command (e.g., `pip install -r requirements.txt`) and the start command (e.g., `gunicorn run:app`).

2. **Configure Environment Variables:**  
Set variables like `SECRET_KEY` and `DATABASE_URL` in your deployment dashboard.

## Usage

- **Home Page:**  
  Displays a welcome message and a brief description of the application.

- **User Authentication:**  
  Users can register, log in, and log out.

- **Dashboard:**  
  Users can upload songs and view the list of uploaded songs. Global player controls are hidden on this page.

- **Now Playing Page:**  
  Displays the currently playing song with its cover art, title, artist, and album. It includes its own control bar (play/pause, next, previous, and a progress bar with timestamps). Use the control buttons to switch tracks and update the displayed song details.

## Technologies Used

- **Flask:** Web framework.
- **SQLAlchemy & Flask-Migrate:** ORM and database migration tool.
- **Mutagen:** Library for extracting audio metadata.
- **HTML/CSS/JavaScript:** Front-end design and interactivity.
- **Gunicorn:** Production WSGI server.
- **MySQL/SQLite:** Database backend (configurable via `config.py`) 
