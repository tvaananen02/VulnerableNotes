# CRUD operations for notes
from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import uuid
from .. import database
from .. import file_validator
from ..dependencies import get_current_user
from ..config import UPLOAD_DIR

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
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
    
@router.get("/create-note", response_class=HTMLResponse)
async def create_note_page(request: Request):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    
    return templates.TemplateResponse("create_note.html", {
        "request": request,
        "user": user
    })

@router.post("/create-note")
async def create_note(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    is_private: bool = Form(False),
    file: UploadFile = File(None)
):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    file_content = None
    # Validate and read file if provided
    if file and file.filename:
        # FLAW 4 (A08): No file type validation or integrity checks
        # Read file content
        file_content = await file.read()
        # # FIX for FLAW 4: Validate using external module
        # is_valid, error_message = file_validator.validate_file(file.filename, file_content)
        # if not is_valid:
        #     return templates.TemplateResponse("create_note.html", {
        #         "request": request,
        #         "user": user,
        #         "error": error_message
        #     })
    is_private_int = 1 if is_private else 0
    await database.execute_query(
        "INSERT INTO notes (user_id, title, content, is_private) VALUES (?, ?, ?, ?)",
        (user["id"], title, content, is_private_int)
    )
    note = await database.fetch_one(
        "SELECT id FROM notes WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user["id"],)
    )
    if file_content:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        disk_path = f"{UPLOAD_DIR}/{unique_filename}"
        web_path = f"static/uploads/{unique_filename}"
        
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(disk_path, "wb") as f:
            f.write(file_content)
        await database.execute_query(
            "INSERT INTO files (note_id, filename, filepath) VALUES (?, ?, ?)",
            (note["id"], file.filename, web_path)
        )
    return RedirectResponse("/dashboard", status_code=303)


@router.get("/note/{note_id}", response_class=HTMLResponse)
async def view_note(request: Request, note_id: int):
    user = await get_current_user(request)
    if not user:
        return RedirectResponse("/login")
    # FLAW 5 (A01): Not checking if note belongs to user
    note = await database.fetch_one(
        "SELECT * FROM notes WHERE id = ?",
        (note_id,)
    )
    # FIX for FLAW 5 :
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

@router.post("/note/{note_id}/delete")
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
            filename = file["filepath"].split('/')[-1]
            filepath = f"{UPLOAD_DIR}/{filename}"
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error deleting file: {e}")
    await database.execute_query(
        "DELETE FROM files WHERE note_id = ?",
        (note_id,)
    )
    await database.execute_query(
        "DELETE FROM notes WHERE id = ? AND user_id = ?",
        (note_id, user["id"])
    )
    return RedirectResponse("/dashboard", status_code=303)