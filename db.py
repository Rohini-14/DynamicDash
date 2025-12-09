import sqlite3, os, bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        name TEXT,
        password_hash BLOB NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        message TEXT,
        rating INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()

    cur.execute("SELECT COUNT(*) as c FROM users WHERE email=?", ("admin@example.com",))
    row = cur.fetchone()
    if row is None or row["c"] == 0:
        hashed = bcrypt.hashpw(b"admin123", bcrypt.gensalt())
        cur.execute("INSERT OR REPLACE INTO users (email, name, password_hash, role) VALUES (?, ?, ?, ?)",
                    ("admin@example.com", "Admin", hashed, "admin"))
        conn.commit()

def create_user(email: str, name: str, password: str, role: str = "user"):
    conn = get_conn()
    cur = conn.cursor()
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    cur.execute("INSERT OR REPLACE INTO users (email, name, password_hash, role) VALUES (?, ?, ?, ?)",
                (email.lower(), name, hashed, role))
    conn.commit()

def get_user(email: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email.lower(),))
    row = cur.fetchone()
    return dict(row) if row else None

def verify_user(email: str, password: str):
    u = get_user(email)
    if not u:
        return None
    ok = bcrypt.checkpw(password.encode("utf-8"), u["password_hash"])
    return u if ok else None

def list_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT email, name, role, created_at FROM users ORDER BY created_at DESC")
    return [dict(r) for r in cur.fetchall()]

def insert_feedback(email: str, message: str, rating: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO feedback (user_email, message, rating) VALUES (?, ?, ?)",
                (email.lower(), message, int(rating)))
    conn.commit()
