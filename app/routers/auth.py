# Authentication routes(login, register, logout)
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
import bcrypt
from .. import database
from .. import password_checker
from ..config import SESSION_EXPIRATION_HOURS

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """Register new user"""
    username = username.strip()
    email = email.strip()
    password = password.strip()
    
    # FLAW 3 (A07): No password strength requirements
    
    # FIX for FLAW 3 (commented out):
    # is_valid, error_message = password_checker.validate_password_strength(password)
    # if not is_valid:
    #     return templates.TemplateResponse("register.html", {
    #         "request": request,
    #         "error": error_message,
    #         "username": username,
    #         "email": email
    #     })
    
    # FLAW 1 (A04): Storing password in plain text
    await database.execute_query(
        "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
        (username, email, password, 0)
    )
    
    # FIX for FLAW 1 (commented out):
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # await database.execute_query(
    #     "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
    #     (username, email, hashed_password.decode('utf-8'), 0)
    # )
    return RedirectResponse("/login", status_code=303)

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    username = username.strip()
    password = password.strip()

    # FLAW 2 (A05): SQL Injection - building query with f-string
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    user = await database.fetch_one(query, ())
    
    # FIX for FLAW 2 (commented out):
    # user = await database.fetch_one(
    #     "SELECT * FROM users WHERE username = ?",
    #     (username,)
    # )
    # if user:
    #     if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
    #         user = None
    if user:
        request.session["user_id"] = user["id"]
        request.session["expires_at"] = (
            datetime.now() + timedelta(hours=SESSION_EXPIRATION_HOURS)
        ).isoformat()
        return RedirectResponse("/dashboard", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid credentials"
        })

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")
