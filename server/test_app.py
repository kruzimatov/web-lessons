"""Run: python3 server/test_app.py  (starts the API on a free port with a temporary database)"""

import json
import sys
import tempfile
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).parent))
import app  # noqa: E402
import store  # noqa: E402

store.open_db(str(Path(tempfile.mkdtemp()) / "test.db"))
store.add_user("teach", "teacher-pass-1", "teacher")
store.add_user("kid", "kid-pass-12", "student")
server = ThreadingHTTPServer(("127.0.0.1", 0), app.App)
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{server.server_address[1]}"


def call(path, body=None, cookie=""):
    req = urllib.request.Request(BASE + path, method="POST" if body is not None else "GET",
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json", "Cookie": cookie})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.load(r), r.headers.get("Set-Cookie", "")
    except HTTPError as e:
        return e.code, json.load(e), ""


def session(username, password):
    status, data, header = call("/api/login", {"username": username, "password": password})
    assert status == 200 and "HttpOnly" in header and "Secure" in header, (status, data)
    return header.split(";")[0]


assert call("/api/login", {"username": "kid", "password": "wrong"})[0] == 401
assert call("/api/login", {"username": "nobody", "password": "x"})[0] == 401
assert call("/api/me")[0] == 401
kid = session("KID", "kid-pass-12")  # usernames ignore case
teach = session("teach", "teacher-pass-1")

assert call("/api/sync", {"items": {"code:h1-1": {"v": "<h1>Hi</h1>", "t": 100}, "game": {"v": "{\"stars\":{\"sign\":3},\"gems\":15}", "t": 100}}}, kid)[0] == 200
assert call("/api/sync", {"items": {"code:h1-1": {"v": "old", "t": 50}}}, kid)[0] == 200  # older loses
assert call("/api/sync", {"items": {"secret": {"v": "x", "t": 1}}}, kid)[0] == 400
assert call("/api/sync", {"items": {"code:x": {"v": "x" * 60_000, "t": 1}}}, kid)[0] == 400
assert call("/api/me", cookie=kid)[1]["items"]["code:h1-1"]["v"] == "<h1>Hi</h1>"

assert call("/api/teacher/students", cookie=kid)[0] == 403
listing = call("/api/teacher/students", cookie=teach)[1]["students"]
assert listing[0]["username"] == "kid" and listing[0]["stars"] == 3 and listing[0]["gems"] == 15, listing
kid_id = listing[0]["id"]
assert call(f"/api/teacher/student?id={kid_id}", cookie=teach)[1]["items"]["code:h1-1"]["v"] == "<h1>Hi</h1>"
assert call("/api/teacher/students", {"username": "kid", "password": "another-1"}, teach)[0] == 400
assert call("/api/teacher/students", {"username": "kid2", "password": "short"}, teach)[0] == 400
assert call("/api/teacher/students", {"username": "kid2", "password": "long-enough"}, teach)[0] == 200

assert call("/api/teacher/parent-link", {"id": kid_id}, kid)[0] == 403
assert call("/api/parent?k=" + "x" * 43)[0] == 404
key = call("/api/teacher/parent-link", {"id": kid_id}, teach)[1]["key"]
assert len(key) == 8 and set(key) <= set(store.KEY_LETTERS), key
assert call("/api/parent?k=" + key.upper())[0] == 200  # typed in capitals still works
assert call("/api/teacher/parent-link", {"id": kid_id}, teach)[1]["key"] == key  # same link until a new one
found = call("/api/parent?k=" + key)[1]
assert found["username"] == "kid" and found["items"]["code:h1-1"]["v"] == "<h1>Hi</h1>", found
new_key = call("/api/teacher/parent-link", {"id": kid_id, "new": True}, teach)[1]["key"]
assert new_key != key and call("/api/parent?k=" + key)[0] == 404 and call("/api/parent?k=" + new_key)[0] == 200
assert call("/api/teacher/password", {"id": kid_id, "password": "new-kid-pass"}, teach)[0] == 200
assert call("/api/me", cookie=kid)[0] == 401  # new password logs out his devices
assert call("/api/teacher/delete", {"id": kid_id}, teach)[0] == 200
assert call("/api/login", {"username": "kid", "password": "new-kid-pass"})[0] == 401
assert call("/api/health")[1] == {"ok": True}
print("server: all tests pass")
