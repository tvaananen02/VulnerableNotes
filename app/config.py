import secrets
DATABASE_URL = "vulnerablenotes.db"
APP_TITLE = "VulnerableNotes"
SECRET_KEY = secrets.token_urlsafe(32)
SESSION_EXPIRATION_HOURS = 1
DATABASE_URL = "vulnerablenotes.db"
UPLOAD_DIR = "app/static/uploads"
ALLOWED_FILE_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.md'}
MAX_FILE_SIZE = 5*1024*1024