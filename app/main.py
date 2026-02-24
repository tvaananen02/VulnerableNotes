from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .config import APP_TITLE, SECRET_KEY
from .routers import pages, auth, notes
from . import database

app = FastAPI(title=APP_TITLE)
app.mount("/static", StaticFiles(directory="app/static"))
app.add_middleware(SessionMiddleware, secret_key = SECRET_KEY)
app.include_router(pages.router, tags=["pages"])
app.include_router(auth.router, tags=["auth"])
app.include_router(notes.router, tags=["notes"])

@app.on_event("startup")
async def startup_event():
    await database.init_db()
    print("App created and database initialized. Be safe ;)")