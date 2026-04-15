from flask import Flask, request, session, redirect, url_for, render_template, g
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # Weak secret key (intentional)

DATABASE = "app.db"


# ─────────────────────────────────────────────
# Database helpers
# ─────────────────────────────────────────────

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", user=session.get("username"))


# ── VULNERABILITY 1: SQL Injection ──────────────────────────────────────────
# The login query is built using raw string concatenation.
# Payload: username = ' OR '1'='1' --   password = anything
# This bypasses authentication entirely.
# Flag stored inside the 'secrets' table, retrieved via UNION injection.

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # VULNERABLE: raw string concatenation — never do this in real code!
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        db = get_db()
        try:
            user = db.execute(query).fetchone()
        except Exception as e:
            error = f"DB Error: {e}"
            return render_template("login.html", error=error)

        if user:
            session["username"] = user["username"]
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect(url_for("index"))
        else:
            error = "Invalid credentials."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ── VULNERABILITY 2: Stored XSS ─────────────────────────────────────────────
# Comments are stored in the DB and rendered with | safe in the template,
# meaning HTML/JS is never escaped.
# Payload: <script>alert('XSS: FLAG{xss_st0r3d_4tt4ck}')</script>
# The flag pops up in an alert for anyone viewing the comments page.

@app.route("/comments", methods=["GET", "POST"])
def comments():
    db = get_db()
    if request.method == "POST":
        if not session.get("username"):
            return redirect(url_for("login"))
        content = request.form["content"]
        # VULNERABLE: no sanitization before storing
        db.execute(
            "INSERT INTO comments (author, content) VALUES (?, ?)",
            (session["username"], content),
        )
        db.commit()

    all_comments = db.execute("SELECT * FROM comments ORDER BY id DESC").fetchall()
    return render_template("comments.html", comments=all_comments, user=session.get("username"))


# ── VULNERABILITY 3: Broken Access Control ──────────────────────────────────
# The /admin route has NO session or role check.
# Any user (or even an unauthenticated visitor) can access it directly.
# Flag is displayed on the admin dashboard page.

@app.route("/admin")
def admin():
    db = get_db()
    users = db.execute("SELECT id, username, role FROM users").fetchall()
    # VULNERABLE: missing  →  if session.get("role") != "admin": abort(403)
    return render_template("admin.html", users=users)


# ── VULNERABILITY 4: IDOR (Insecure Direct Object Reference) ────────────────
# The profile page accepts a user id via the URL parameter with no ownership check.
# A logged-in user can change ?id=3 to ?id=2 to read another user's private data.
# Flag is hidden in the private_note field of user id=2.

@app.route("/profile")
def profile():
    if not session.get("username"):
        return redirect(url_for("login"))

    user_id = request.args.get("id", session.get("user_id"))
    db = get_db()
    # VULNERABLE: no check that user_id == session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()

    if not user:
        return "User not found.", 404

    return render_template("profile.html", profile=user, current_user=session.get("username"))


# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
