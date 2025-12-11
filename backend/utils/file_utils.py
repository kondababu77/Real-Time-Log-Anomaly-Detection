"""
File utilities
"""
import os

ALLOWED_EXTENSIONS = {'log', 'txt'}

def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder(folder):
    """Ensure upload folder exists"""
    if not os.path.exists(folder):
        os.makedirs(folder)
