"""SQLite storage: users, login sessions, and each student's saved work (code, game, homework)."""

import hashlib
import hmac
import json
import secrets
import sqlite3
import threading
import time

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT NOT NULL UNIQUE COLLATE NOCASE,
  pw_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('student', 'teacher')),
  created REAL NOT NULL,
  updated REAL
);
CREATE TABLE IF NOT EXISTS sessions (
  token_hash TEXT PRIMARY KEY,
  user INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  expires REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS items (
  user INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  key TEXT NOT NULL,
  value TEXT,
  t REAL NOT NULL,
  PRIMARY KEY (user, key)
);
"""
DAY = 86400
SESSION_DAYS = {"student": 365, "teacher": 30}  # a student logs in once per device
MAX_KEYS = 400
KEY_LETTERS = "abcdefghjkmnpqrstuvwxyz23456789"  # no 0/o, 1/l/i: easy to read out

lock = threading.RLock()
db = None


def open_db(path):
    global db
    db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA journal_mode = WAL")
    db.executescript(SCHEMA)
    if "parent_key" not in {row[1] for row in db.execute("PRAGMA table_info(users)")}:
        db.execute("ALTER TABLE users ADD COLUMN parent_key TEXT")  # older databases
    db.execute("CREATE UNIQUE INDEX IF NOT EXISTS users_parent_key ON users (parent_key)")


def q(sql, *args):
    with lock:
        return db.execute(sql, args).fetchall()


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def hash_password(password, salt=None):
    salt = salt or secrets.token_bytes(16)
    key = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return f"scrypt${salt.hex()}${key.hex()}"


DUMMY = hash_password("timing filler")


def check_password(password, stored):
    salt = bytes.fromhex(stored.split("$")[1])
    return hmac.compare_digest(hash_password(password, salt), stored)


def add_user(username, password, role):
    q("INSERT INTO users (username, pw_hash, role, created) VALUES (?, ?, ?, ?)",
      username, hash_password(password), role, time.time())
    return q("SELECT id FROM users WHERE username = ?", username)[0][0]


def set_password(user_id, password):
    q("UPDATE users SET pw_hash = ? WHERE id = ?", hash_password(password), user_id)
    q("DELETE FROM sessions WHERE user = ?", user_id)  # log out every device


def login(username, password):
    """A new session token, or None. Unknown names still hash, so timing says nothing."""
    rows = q("SELECT id, pw_hash, role FROM users WHERE username = ?", username)
    if not rows:
        check_password(password, DUMMY)
        return None
    user_id, pw_hash, role = rows[0]
    if not check_password(password, pw_hash):
        return None
    token = secrets.token_urlsafe(32)
    days = SESSION_DAYS[role]
    q("DELETE FROM sessions WHERE expires < ?", time.time())
    q("INSERT INTO sessions VALUES (?, ?, ?)", sha(token), user_id, time.time() + days * DAY)
    return token, role, days * DAY


def user_for(token):
    rows = q("SELECT u.id, u.username, u.role FROM sessions s JOIN users u ON u.id = s.user "
             "WHERE s.token_hash = ? AND s.expires > ?", sha(token), time.time())
    return dict(zip(("id", "username", "role"), rows[0])) if rows else None


def logout(token):
    q("DELETE FROM sessions WHERE token_hash = ?", sha(token))


def items(user_id):
    return {k: {"v": v, "t": t} for k, v, t in q("SELECT key, value, t FROM items WHERE user = ?", user_id)}


def save_items(user_id, new):
    """Newest change wins for each key, so two devices can both save."""
    with lock:
        count = q("SELECT COUNT(*) FROM items WHERE user = ?", user_id)[0][0]
        for key, (value, t) in new.items():
            exists = q("SELECT 1 FROM items WHERE user = ? AND key = ?", user_id, key)
            if not exists and count >= MAX_KEYS:
                continue
            count += not exists
            q("INSERT INTO items VALUES (?, ?, ?, ?) ON CONFLICT (user, key) "
              "DO UPDATE SET value = excluded.value, t = excluded.t WHERE excluded.t > items.t",
              user_id, key, value, t)
        q("UPDATE users SET updated = ? WHERE id = ?", time.time(), user_id)


def summary(game_json):
    try:
        game = json.loads(game_json or "{}")
        stars = game.get("stars", {})
        return {"levels": len(stars), "stars": sum(stars.values()), "gems": game.get("gems", 0),
                "best": game.get("best", 0), "homework": sorted(int(n) for n in game.get("homework", {}))}
    except (ValueError, TypeError, AttributeError):
        return {}


def students():
    rows = q("SELECT u.id, u.username, u.updated, i.value FROM users u "
             "LEFT JOIN items i ON i.user = u.id AND i.key = 'game' WHERE u.role = 'student' ORDER BY u.username")
    return [{"id": i, "username": name, "updated": updated, **summary(game)} for i, name, updated, game in rows]


def student(user_id):
    rows = q("SELECT username, updated FROM users WHERE id = ? AND role = 'student'", user_id)
    return {"username": rows[0][0], "updated": rows[0][1], "items": items(user_id)} if rows else None


def parent_key(user_id, new=False):
    """The secret in a student's parent link. A new one turns the old link off."""
    rows = q("SELECT parent_key FROM users WHERE id = ? AND role = 'student'", user_id)
    if not rows:
        return None
    if rows[0][0] and not new:
        return rows[0][0]
    key = "".join(secrets.choice(KEY_LETTERS) for _ in range(8))
    q("UPDATE users SET parent_key = ? WHERE id = ?", key, user_id)
    return key


def student_by_key(key):
    rows = q("SELECT id FROM users WHERE parent_key = ? COLLATE NOCASE AND role = 'student'", key)
    return student(rows[0][0]) if rows else None


def delete_student(user_id):
    q("DELETE FROM users WHERE id = ? AND role = 'student'", user_id)
