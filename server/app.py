"""Web Lessons API: login, saving a student's work, and the teacher panel.
The parent page reads one student's progress through a secret link.
Python standard library only. Runs behind nginx on 127.0.0.1, the site reaches it as /api/.

Run:      WL_DB=data/lessons.db python3 server/app.py
Add user: python3 server/app.py adduser <username> <student|teacher>   (password is read from stdin)
"""

import json
import math
import os
import re
import sys
import threading
import time
import traceback
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import store

PORT = int(os.environ.get("WL_PORT", "8750"))
COOKIE = "wl_session"
KEY = re.compile(r"^(code:[\w-]{1,40}|game|last)$")  # only what the site saves
USERNAME = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")
MAX_BODY, MAX_VALUE = 1_000_000, 50_000

ANSWERS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "answers.json")  # written by generate/build.py
hits, hits_lock = {}, threading.Lock()


def limited(bucket, per_minute):
    key = (bucket, int(time.time() // 60))
    with hits_lock:
        if len(hits) > 20_000:
            hits.clear()
        hits[key] = hits.get(key, 0) + 1
        return hits[key] > per_minute


class Fail(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


def need(ok, message, status=400):
    if not ok:
        raise Fail(status, message)


class App(BaseHTTPRequestHandler):
    server_version = "web-lessons"

    def log_message(self, *args):
        pass  # nginx keeps the access log

    def do_GET(self):
        self.handle_api("GET")

    def do_POST(self):
        self.handle_api("POST")

    def handle_api(self, method):
        url = urlparse(self.path)
        forwarded = self.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        self.ip = forwarded or self.client_address[0]
        try:
            need(not limited(("all", self.ip), 300), "Too many requests. Wait a minute.", 429)
            route = ROUTES.get((method, url.path))
            need(route, "Not found", 404)
            self.query = {k: v[0] for k, v in parse_qs(url.query).items()}
            self.body = self.read_json() if method == "POST" else {}
            self.cookies = []
            self.reply(200, route(self))
        except Fail as e:
            self.reply(e.status, {"error": str(e)})
        except Exception:
            traceback.print_exc()
            self.reply(500, {"error": "Server error"})

    def read_json(self):
        need("application/json" in self.headers.get("Content-Type", ""), "Send JSON", 415)
        size = int(self.headers.get("Content-Length") or 0)
        need(size <= MAX_BODY, "Too big", 413)
        try:
            body = json.loads(self.rfile.read(size) or b"{}")
        except ValueError:
            raise Fail(400, "Bad JSON") from None
        need(isinstance(body, dict), "Bad JSON")
        return body

    def reply(self, status, data):
        raw = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(raw)))
        for c in getattr(self, "cookies", []):
            self.send_header("Set-Cookie", c)
        self.end_headers()
        self.wfile.write(raw)

    def set_cookie(self, value, age):
        self.cookies.append(f"{COOKIE}={value}; Max-Age={age}; Path=/; HttpOnly; Secure; SameSite=Lax")

    def token(self):
        jar = SimpleCookie(self.headers.get("Cookie", ""))
        return jar[COOKIE].value if COOKIE in jar else ""

    def user(self, role=None):
        user = store.user_for(self.token()) if self.token() else None
        need(user, "Please log in", 401)
        need(role is None or user["role"] == role, "Not allowed", 403)
        return user

    def text(self, name, longest=200):
        value = self.body.get(name)
        need(isinstance(value, str) and 0 < len(value) <= longest, f"{name} is missing")
        return value

    def number(self, name):
        value = self.body.get(name, self.query.get(name))
        try:
            return int(value)
        except (TypeError, ValueError):
            raise Fail(400, f"{name} is missing") from None


def login(req):
    username, password = req.text("username", 30), req.text("password")
    need(not limited(("login", req.ip), 10) and not limited("login-all", 60), "Too many tries. Wait a minute.", 429)
    found = store.login(username, password)
    need(found, "Wrong username or password", 401)
    token, role, age = found
    req.set_cookie(token, age)
    return {"role": role}


def logout(req):
    if req.token():
        store.logout(req.token())
    req.set_cookie("", 0)
    return {"ok": True}


def me(req):
    user = req.user()
    return {**user, "items": store.items(user["id"]) if user["role"] == "student" else {}}


def sync(req):
    user = req.user("student")
    items = req.body.get("items")
    need(isinstance(items, dict) and len(items) <= store.MAX_KEYS, "Bad items")
    now, clean = time.time() * 1000, {}
    for key, item in items.items():
        need(KEY.match(key) and isinstance(item, dict), "Bad item")
        value, t = item.get("v"), item.get("t")
        need(value is None or (isinstance(value, str) and len(value) <= MAX_VALUE), "Item too big")
        need(isinstance(t, (int, float)) and math.isfinite(t), "Bad time")
        clean[key] = (value, min(t, now))  # a wrong clock on his device cannot lock the value forever
    store.save_items(user["id"], clean)
    return {"ok": True}


def teacher_students(req):
    req.user("teacher")
    return {"students": store.students()}


def teacher_student(req):
    req.user("teacher")
    found = store.student(req.number("id"))
    need(found, "No such student", 404)
    return found


def teacher_answers(req):
    req.user("teacher")
    with open(ANSWERS, encoding="utf-8") as f:
        return {"answers": json.load(f)}


def teacher_parent_link(req):
    req.user("teacher")
    key = store.parent_key(req.number("id"), new=req.body.get("new") is True)
    need(key, "No such student", 404)
    return {"key": key}


def parent(req):
    """Public and read-only: a parent opens the secret link and sees the progress, no login."""
    need(not limited(("parent", req.ip), 30) and not limited("parent-all", 300), "Too many requests. Wait a minute.", 429)
    key = req.query.get("k", "").strip()
    found = store.student_by_key(key) if 8 <= len(key) <= 100 else None
    need(found, "This link does not work. Ask the teacher for a new one.", 404)
    return found


def password_ok(password):
    need(len(password) >= 8, "Password needs at least 8 characters")
    return password


def teacher_add(req):
    req.user("teacher")
    username = req.text("username", 30)
    need(USERNAME.match(username), "Username: 3 to 30 letters, numbers, _ . -")
    need(not store.q("SELECT 1 FROM users WHERE username = ?", username), "This username is taken")
    return {"id": store.add_user(username, password_ok(req.text("password")), "student")}


def teacher_password(req):
    teacher = req.user("teacher")
    user_id = req.number("id") if "id" in req.body else teacher["id"]
    is_student = store.q("SELECT 1 FROM users WHERE id = ? AND role = 'student'", user_id)
    need(user_id == teacher["id"] or is_student, "No such student", 404)
    store.set_password(user_id, password_ok(req.text("password")))
    return {"ok": True}


def teacher_delete(req):
    req.user("teacher")
    store.delete_student(req.number("id"))
    return {"ok": True}


def health(req):
    store.q("SELECT 1")
    return {"ok": True}


ROUTES = {
    ("POST", "/api/login"): login,
    ("POST", "/api/logout"): logout,
    ("GET", "/api/me"): me,
    ("POST", "/api/sync"): sync,
    ("GET", "/api/teacher/students"): teacher_students,
    ("GET", "/api/teacher/student"): teacher_student,
    ("GET", "/api/teacher/answers"): teacher_answers,
    ("POST", "/api/teacher/students"): teacher_add,
    ("POST", "/api/teacher/password"): teacher_password,
    ("POST", "/api/teacher/delete"): teacher_delete,
    ("POST", "/api/teacher/parent-link"): teacher_parent_link,
    ("GET", "/api/parent"): parent,
    ("GET", "/api/health"): health,
}


def main():
    store.open_db(os.environ.get("WL_DB", "data/lessons.db"))
    if sys.argv[1:2] == ["adduser"]:
        username, role = sys.argv[2], sys.argv[3]
        assert role in ("student", "teacher") and USERNAME.match(username), "usage: adduser <username> <student|teacher>"
        password = sys.stdin.readline().rstrip("\n")
        assert password, "give the password on stdin"
        print("added user", store.add_user(username, password, role))
        return
    print(f"web-lessons API on 127.0.0.1:{PORT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), App).serve_forever()


if __name__ == "__main__":
    main()
