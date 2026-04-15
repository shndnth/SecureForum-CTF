"""
Run this once to create and seed the SQLite database.
  python init_db.py
"""

import sqlite3

conn = sqlite3.connect("app.db")
c = conn.cursor()

# ── Users table ─────────────────────────────────────────────────────────────
c.execute("DROP TABLE IF EXISTS users")
c.execute("""
CREATE TABLE users (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    username     TEXT NOT NULL,
    password     TEXT NOT NULL,
    role         TEXT DEFAULT 'user',
    private_note TEXT
)
""")

# Seed users
# id=1  →  regular player account (used to log in during CTF)
# id=2  →  victim account whose private note contains the IDOR flag
# id=3  →  admin account
c.executemany(
    "INSERT INTO users (username, password, role, private_note) VALUES (?,?,?,?)",
    [
        ("player",  "player123",  "user",  "Nothing interesting here."),
        ("alice",   "alice456",   "user",  "FLAG{1d0r_us3r_3xp0s3d}"),   # IDOR flag
        ("admin",   "adm1n!pass", "admin", "Admin private data."),
    ],
)

# ── Secrets table (holds the SQLi flag — discoverable via UNION injection) ──
c.execute("DROP TABLE IF EXISTS secrets")
c.execute("""
CREATE TABLE secrets (
    id    INTEGER PRIMARY KEY,
    value TEXT
)
""")
c.execute("INSERT INTO secrets (value) VALUES ('FLAG{sql_1nj3ct10n_pwn3d}')")

# ── Comments table (Stored XSS) ─────────────────────────────────────────────
c.execute("DROP TABLE IF EXISTS comments")
c.execute("""
CREATE TABLE comments (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    author  TEXT,
    content TEXT
)
""")

# Seed an innocent comment so the page isn't empty
c.execute(
    "INSERT INTO comments (author, content) VALUES (?,?)",
    ("alice", "Welcome to SecureForum! Feel free to leave a comment."),
)

conn.commit()
conn.close()
print("Database initialised successfully.")
