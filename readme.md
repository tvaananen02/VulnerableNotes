# VulnerableNotes

This project was done as a submission to Cyber Security Base 2025 Project 1


## Educational Purpose Disclaimer

This project is created for educational purposes to:
- Understand common web security vulnerabilities
- Learn secure coding practices especially with FastAPI and Python
- Practice identifying and fixing security flaws
- Study the OWASP Top 10

**⚠️ WARNING**

**This application contains intentional security vulnerabilities for educational purposes only.**
- **DO NOT store real sensitive data**
- **For learning and demonstration purposes only!!!**
---

## Prerequisites for running the app

- Python 3.8 or higher
- pip (Python package manager)
- Git (This is optional, for cloning the repo.)

---

## Technologies Used

- **FastAPI**
- **SQLite**
- **Jinja2** 
- **aiosqlite** 

---

## Running the app

### Linux(Ubuntu/Debian) 


1. Install Python and pip(if not already installed)
```bash
sudo apt install python3 python3-pip python3-venv
```
2. Clone or download the repository and cd into the root directory
```bash
git clone {repo_url}
cd VulnerableNotes
```
3. Create the virtual environment:
```bash
python3 -m venv venv
```
4. Activate the virtual environment
```bash
source venv/bin/activate
```
5. Install the required dependencies:
```bash
pip install -r requirements.txt
```
6. Run the application
```bash
uvicorn app.main:app --reload
```

7. Open browser at address http://localhost:8000 to view the app

8. Use this command to erase the database from the directory root (needed to implement fixes 2 and 3 atleast)
```bash
rm vulnerablenotes.db
```
9. How to access the database
```bash
sqlite3 vulnerablenotes.db
```
### macOs
1. **Install Python (if not already installed):**

Using Homebrew:
```bash
brew install python3
```

Or download from: https://www.python.org/downloads/

2. **Clone or download the repository:**
```bash
git clone 
cd VulnerableNotes
```

3. **Create virtual environment:**
```bash
python3 -m venv venv
```

4. **Activate virtual environment:**
```bash
source venv/bin/activate
```

5. **Install dependencies:**
```bash
pip install -r requirements.txt
```

6. **Run the application:**
```bash
uvicorn app.main:app --reload
```

7. **Open browser:**
```
http://localhost:8000
```

### Windows

1. **Install Python:**
- Download from https://www.python.org/downloads/
- **Important:** Check "Add Python to PATH" during installation

2. **Verify installation:**
```cmd
python --version
```

3. **Clone or download the repository:**
```cmd
git clone <your-repo-url>
cd VulnerableNotes
```

Or download ZIP and extract.

4. **Create virtual environment:**
```cmd
python -m venv venv
```

5. **Activate virtual environment:**

Command Prompt:
```cmd
venv\Scripts\activate.bat
```

PowerShell:
```powershell
venv\Scripts\Activate.ps1
```

If PowerShell gives an error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

6. **Install dependencies:**
```cmd
pip install -r requirements.txt
```

7. **Run the application:**
```cmd
python -m uvicorn app.main:app --reload
```

8. **Open browser:**
```
http://localhost:8000
```

## Stopping the app

Simply, press CTRL+C in the terminal where the app is running


## Features
- User registration and authentication
- Create, view, and delete notes
- File attachments for notes
- Private/public note visibility
- Test users pre-loaded with demo data
### Test users
The application comes with three pre-configured test accounts:

| Username | Password | Role |
|----------|----------|------|
| John | mypasswd123 | Regular User |
| Jane | 123dwssap | Regular User |
| admin | admin#234 | Admin User |

You can try to login as any of them and view the content.

---
## Security Flaws Implemented

This application intentionally contains the following OWASP Top 10 vulnerabilities (https://owasp.org/Top10/2025/):

1. **A01: Broken Access Control** - Users can view and delete other users' notes
2. **A04: Cryptographic Failures** - Passwords stored in plain text
3. **A05: Injection** - SQL injection vulnerability in login
4. **A07: Authentication Failures** - Weak session management
5. **A08: Software and Data Integrity Failures** - No file upload validation

All flaws include commented fixes in the source code.

---


```python
from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import secrets
import os
import uuid
import bcrypt
from datetime import datetime, timedelta
from . import database
from . import password_checker
from . import file_validator

app = FastAPI(
    title="VulnerableNotes"
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
SECRET_KEY = secrets.token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@app.on_event("startup")
async def startup_event():
    await database.init_db()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = await get_current_user(request)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request
    })
        
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {
        "request": request
    })
    
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    
    notes = await database.fetch_all(
        "SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC",
        (user["id"],)
    )
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "notes": notes
    })    
    
@app.post("/register")
async def register(request: Request):
    form = await request.form()
    username = form.get("username", "").strip()
    email = form.get("email", "").strip()
    password = form.get("password", "").strip()
    
    # FLAW 1 (A07): No password strength requirements
    # Accepts weak passwords like "123", "a", "password"
    # No minimum length, complexity, or common password checks
    
    # # FIX for FLAW 1: check password strength using the password checker modules
    # is_valid, error_message = password_checker.validate_password_strength(password)
    # if not is_valid:
    #     return templates.TemplateResponse("register.html", {
    #         "request": request,
    #         "error": error_message,
    #         "username": username,
    #         "email": email
    #     })
    
    # FLAW 2 (A04): Storing password in plain text
    await database.execute_query(
        "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
        (username, email, password, 0)
    )
    
    # FIX for FLAW 2 :
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # await database.execute_query(
    #     "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
    #     (username, email, hashed_password.decode('utf-8'), 0)
    # )
    
    return RedirectResponse("/login", status_code=303)

@app.post("/login")
async def login(request: Request):
    form = await request.form()
    username = form.get("username", "").strip()
    password = form.get("password", "").strip()

    # FLAW 3 (A05): SQL Injection - building query with f-string
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    user = await database.fetch_one(query, ())
    
    # # FIX for FLAW 3:
    # user = await database.fetch_one(
    #     "SELECT * FROM users WHERE username = ?",
    #     (username,)
    # )
    # if user:
    #     if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
    #         user = None
    
    if user:
        request.session["user_id"] = user["id"]
        request.session["expires_at"] = (datetime.now() + timedelta(hours=1)).isoformat()
        return RedirectResponse("/dashboard", status_code=303)
    else:    
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid credentials"
        })

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")

@app.get("/create-note", response_class=HTMLResponse)
async def create_note_page(request: Request):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    
    return templates.TemplateResponse("create_note.html", {
        "request": request,
        "user": user
    })

@app.post("/create-note")        
async def create_note(request: Request, file: UploadFile = File(None)):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    
    form = await request.form()
    title = form.get("title")
    content = form.get("content")
    is_private = 1 if form.get("is_private") else 0
    file_content = None    
    # Validate and read file if provided
    if file and file.filename:
        # FLAW 4 (A08): No file type validation or integrity checks, jumping straight to file reading
        file_content = await file.read()         
        # # FIX for FLAW 4: validate the file extension and size using file_validator
        # is_valid, error_message = file_validator.validate_file(file.filename, file_content)
        # if not is_valid:
        #     return templates.TemplateResponse("create_note.html", {
        #         "request": request,
        #         "user": user,
        #         "error": error_message
        #     })            
    # Create note (only reached if validation passed)
    await database.execute_query(
        "INSERT INTO notes (user_id, title, content, is_private) VALUES (?, ?, ?, ?)",
        (user["id"], title, content, is_private)
    )
    note = await database.fetch_one(
        "SELECT id FROM notes WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user["id"],)
    )
    if file_content:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = f"app/static/uploads/{unique_filename}"   
        os.makedirs("app/static/uploads", exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(file_content)

        await database.execute_query(
            "INSERT INTO files (note_id, filename, filepath) VALUES (?, ?, ?)",
            (note["id"], file.filename, filepath)
        )
    
    return RedirectResponse("/dashboard", status_code=303)
    
@app.get("/note/{note_id}", response_class=HTMLResponse)
async def view_note(request: Request, note_id: int):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    
    # FLAW 5 (A01): Not checking if note belongs to user
    note = await database.fetch_one(
        "SELECT * FROM notes WHERE id = ?",
        (note_id,)
    )
    
    # # FIX for FLAW 5: validate that the note's user id is the same as the current user's id
    # note = await database.fetch_one(
    #     "SELECT * FROM notes WHERE id = ? AND user_id = ?",
    #     (note_id, user["id"])
    # )
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    files = await database.fetch_all(
        "SELECT * FROM files WHERE note_id = ?",
        (note_id,)
    )
    
    return templates.TemplateResponse("note.html", {
        "request": request,
        "user": user,
        "note": note,
        "files": files
    })

@app.post("/note/{note_id}/delete")
async def delete_note(request: Request, note_id: int):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    
    files = await database.fetch_all(
        "SELECT * FROM files WHERE note_id = ?",
        (note_id,)
    )
    
    for file in files:
        try:
            filepath = file["filepath"]
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error deleting file: {e}")

    await database.execute_query(
        "DELETE FROM files WHERE note_id = ?",
        (note_id,)
    )
    
    # FLAW 6 (A01): Not checking if user owns the note before deleting
    await database.execute_query(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )
    
    # FIX for FLAW 6: validate that the note's user_id is the same as current user's id
    # await database.execute_query(
    #     "DELETE FROM notes WHERE id = ? AND user_id = ?",
    #     (note_id, user["id"])
    # )
    
    return RedirectResponse("/dashboard", status_code=303)

async def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    if datetime.now() > datetime.fromisoformat(request.session.get("expires_at")):
        request.session.clear()
        return None
    user = await database.fetch_one(
        "SELECT * FROM users WHERE id = ?", 
        (user_id,)
    )
    return user
    ```