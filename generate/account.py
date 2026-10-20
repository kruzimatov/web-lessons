"""Login page (students and teacher) and the teacher panel. The API lives in server/."""

import json

from game_data import MISSIONS
from html_kit import page, plain
from pages import homework_tasks

NOINDEX = '<meta name="robots" content="noindex">\n'


def password_field(label="Password", auto="current-password"):
    return (f'<label for="password">{label}</label><span class="pw-row">'
            f'<input id="password" name="password" type="password" autocomplete="{auto}" required>'
            '<button type="button" class="show-pw">Show</button></span>')


def login_page():
    body = f"""<h1><small>Save your work everywhere</small>Log in</h1>
<p class="goal">Log in once on each computer or iPad. After that your code, stars and diamonds save by themselves.</p>
<form id="login-form" class="account-form">
<label for="username">Username</label>
<input id="username" name="username" autocomplete="username" autocapitalize="off" spellcheck="false" required>
{password_field()}
<button type="submit" class="btn">Log in</button>
<p id="login-note" class="checked" aria-live="polite"></p>
</form>"""
    return page("Log In", body, root="", head=NOINDEX)


def course_data(lessons):
    """What the teacher panel needs to label his work: task texts, starter code, game levels."""
    tasks = lambda items: [{"task": plain(t["task"]), "start": t.get("start", "")} for t in items]
    return {
        "lessons": [{"n": L["n"], "title": plain(L["title"]), "practice": tasks(L["practice"]),
                     "homework": tasks(homework_tasks(L))} for L in lessons],
        "levels": [{"id": m["id"], "title": m["title"], "lesson": m["lesson"], "start": m["start"]} for m in MISSIONS],
    }


def dialog(name, title, fields, button, danger=False):
    return (f'<dialog id="{name}-dialog" class="tp-dialog"><form method="dialog" id="{name}-form">'
            f'<h2>{title}</h2>{fields}<p class="checked" aria-live="polite"></p>'
            '<div class="tp-dialog-actions"><button type="button" class="tp-btn ghost" data-close>Cancel</button>'
            f'<button type="submit" class="tp-btn{" danger" if danger else ""}">{button}</button></div></form></dialog>')


def teacher_page(lessons):
    data = json.dumps(course_data(lessons)).replace("</", "<\\/")  # starter code contains </p>
    pw = password_field("Password (at least 8 characters)", "new-password")
    body = f"""<div class="tp-page"><h1><small>Teacher</small>Teacher panel</h1>
<div id="gate" hidden><p class="goal">Please <a href="/login">log in</a> with your teacher account.</p></div>
<div id="panel" class="tp" hidden>
<aside class="tp-side">
<div class="tp-side-head"><h2>Students</h2><button type="button" class="tp-btn small" id="add-open">+ Add student</button></div>
<ul class="tp-list" id="students"></ul>
<p class="tp-sync">Updated <span id="synced">now</span> &middot; <button type="button" class="tp-text-btn" id="refresh">Refresh</button></p>
<button type="button" class="tp-text-btn" id="pw-open">Change my password</button>
</aside>
<section class="tp-main" id="detail" aria-live="polite"><p class="tp-empty">Pick a student on the left.</p></section>
</div>
</div>
{dialog("add", "Add a student", '<label for="add-username">Username</label><input id="add-username" name="username" autocomplete="off" autocapitalize="off" spellcheck="false" required>' + pw.replace('id="password"', 'id="add-password"').replace('for="password"', 'for="add-password"'), "Add student")}
{dialog("pw", "Change my password", pw.replace('id="password"', 'id="pw-password"').replace('for="password"', 'for="pw-password"'), "Change password")}
{dialog("student-pw", "New password for <span data-name></span>", pw.replace('id="password"', 'id="spw-password"').replace('for="password"', 'for="spw-password"') + '<p class="tp-note">He will need to log in again on every device.</p>', "Save password")}
{dialog("delete", "Delete <span data-name></span>?", '<p>This deletes the account and <strong>all saved work</strong>: code, stars and diamonds. It cannot be undone.</p>', "Delete forever", danger=True)}
<dialog id="viewer" class="tp-viewer"><div class="tp-viewer-head"><div><p class="tp-kicker" id="v-kicker"></p><h2 id="v-title"></h2></div>
<div class="tp-viewer-nav"><button type="button" class="tp-btn ghost" id="v-prev">&larr; Previous</button>
<button type="button" class="tp-btn ghost" id="v-next">Next &rarr;</button><button type="button" class="tp-btn" data-close>Close</button></div></div>
<p class="tp-task" id="v-task"></p><div id="v-checks"></div>
<div class="tp-viewer-panes"><pre id="v-code"></pre><iframe id="v-view" title="His page" sandbox=""></iframe></div></dialog>
<script type="application/json" id="course">{data}</script>"""
    return page("Teacher Panel", body, root="", head=NOINDEX + '<link rel="stylesheet" href="assets/teacher.css">\n',
                scripts=("teacher-view.js", "teacher.js"))
