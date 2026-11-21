import os
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "replace-this-secret")
DB_PATH = os.environ.get("DATABASE_PATH", str(Path(__file__).parent / "contacts.db"))

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, phone TEXT NOT NULL,
            email TEXT DEFAULT '', address TEXT DEFAULT '', notes TEXT DEFAULT ''
        )""")

@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    with db() as conn:
        if q:
            p = f"%{q}%"
            contacts = conn.execute("""SELECT * FROM contacts
                WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ? OR notes LIKE ?
                ORDER BY name COLLATE NOCASE""", (p,p,p,p,p)).fetchall()
        else:
            contacts = conn.execute("SELECT * FROM contacts ORDER BY name COLLATE NOCASE").fetchall()
        total = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    return render_template("index.html", contacts=contacts, total=total, query=q)

@app.post("/add")
def add():
    data = [request.form.get(k, "").strip() for k in ("name","phone","email","address","notes")]
    if not data[0] or not data[1]:
        flash("Name and phone number are required.", "error")
    else:
        with db() as conn:
            conn.execute("INSERT INTO contacts(name,phone,email,address,notes) VALUES(?,?,?,?,?)", data)
        flash("Contact added.", "success")
    return redirect(url_for("index"))

@app.post("/edit/<int:cid>")
def edit(cid):
    data = [request.form.get(k, "").strip() for k in ("name","phone","email","address","notes")]
    if not data[0] or not data[1]:
        flash("Name and phone number are required.", "error")
    else:
        with db() as conn:
            conn.execute("""UPDATE contacts SET name=?,phone=?,email=?,address=?,notes=? WHERE id=?""", (*data,cid))
        flash("Contact updated.", "success")
    return redirect(url_for("index"))

@app.post("/delete/<int:cid>")
def delete(cid):
    with db() as conn:
        conn.execute("DELETE FROM contacts WHERE id=?", (cid,))
    flash("Contact deleted.", "success")
    return redirect(url_for("index"))

@app.get("/health")
def health():
    return {"status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
