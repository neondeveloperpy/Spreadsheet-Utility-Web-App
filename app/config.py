# App Settings 
from pathlib import Path 

BASE_DIR = Path(__file__).parent 

STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = BASE_DIR / "uploads"
EXPORT_DIR = BASE_DIR / "exports"

MAX_UPLOAD_SIZE = 25 * 1024 * 1024  # 25MB

ALLOWED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls"
}

APP_NAME = "TabulaFlow"

APP_DESCRIPTION = "Free Spreadsheet Utilities"

DEBUG = True