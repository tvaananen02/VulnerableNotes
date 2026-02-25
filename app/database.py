import aiosqlite
import os
import bcrypt
from .config import DATABASE_URL
async def get_db():
    db = await aiosqlite.connect(DATABASE_URL)
    db.row_factory = aiosqlite.Row
    return db
    
async def init_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            is_private INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (note_id) REFERENCES notes(id)
        );        
        """)
        await db.commit()
        await create_test_users(db)

async def create_test_users(db):
    result = await fetch_one("SELECT 1 FROM users LIMIT 1")
    if result:
        print("Test users already exist, skipping creation...")
        return
    print("Creating test users...")
    test_users = [
        ("John", "john@vulnerablenotes.com", "mypasswd123", 0),
        ("Jane", "jane@vulnerablenotes.com", "123dwssap", 0),
        ("admin", "admin@vulnerablenotes.com", "admin#234", 1)
    ]
    #FLAW 2 | part2 (A04): storing default users with plaintext passwords, also vulnerable to sql injection
    for username, email, password, is_admin in test_users:
        await db.execute(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            (username, email, password, is_admin) 
        )
    # #FIX: store hashed passwords on default
    # for username, email, password, is_admin in test_users:
    #     hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    #     await db.execute(
    #         "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
    #         (username, email, hashed.decode('utf-8'), is_admin)
    #     )

    demo_notes = [
        (1, "John's Secret", "I sure hope my secret file wont get leaked anywhere!", 1),
        (1, "John's public note", "We should use sense in what we write and upload here...just in case.", 0),        
        (2, "Jane's Private Note", "Gosh I sure hope John does not see this! I dislike him!!", 1),
        (2, "Janes's Public Note", "We sure are safe here!", 0),
        (3, "Admin's private note", "System update scheduled for tomorrow even though it is Friday! System logs as attachements.", 1),
    ]
    for user_id, title, content, is_private in demo_notes:
        await db.execute(
            "INSERT INTO notes (user_id, title, content, is_private) VALUES (?, ?, ?, ?)",
            (user_id, title, content, is_private)
        )
    os.makedirs("app/static/uploads", exist_ok=True)
    demo_files = [
        (1, "johns_secret.txt", "app/static/uploads/johns_secret.txt"),
        (3, "janes_secret.txt", "app/static/uploads/janes_secre.txt"),
        (5, "admin_logs.md", "app/static/uploads/admin_logs.md")
    ]
    for note_id, filename, filepath in demo_files:
        await db.execute(
            "INSERT INTO files (note_id, filename, filepath) VALUES (?, ?, ?)",
            (note_id, filename, filepath)
        )
    await db.commit()
    print("Test users, demo notes and demo files created!")

async def fetch_one(query: str, params: tuple = ()):
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, params) as cursor:
            return await cursor.fetchone()
        
async def fetch_all(query: str, params: tuple = ()):
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, params) as cursor:
            return await cursor.fetchall()
        
async def execute_query(query: str, params: tuple = ()):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute(query, params)
        await db.commit()
        return db.total_changes