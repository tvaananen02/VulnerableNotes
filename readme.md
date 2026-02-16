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
