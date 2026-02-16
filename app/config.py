import secrets

APP_TITLE = "VulnerableNotes"
SECRET_KEY = secrets.token_urlsafe(32)
SESSION_EXPIRATION_HOURS = 1
DATABASE_URL = "vulnerablenotes.db"
UPLOAD_DIR = "app/static/uploads"
