import os
ALLOWED_FILE_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.md'}
MAX_FILE_SIZE = 5*1024*1024

def validate_file(filename: str, file_content: bytes) -> tuple[bool, str]:
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in ALLOWED_FILE_EXTENSIONS:
        return False, f"Filetype {file_ext} not allowed. Allowed types are: .txt, .pdf, .png, .jpg, .md"

    if len(file_content) > MAX_FILE_SIZE:
        size_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, f"File too large (max {size_mb:.0f}MB)"
    return True, ""            
