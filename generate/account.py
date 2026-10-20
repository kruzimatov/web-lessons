"""Login page (students and teacher) and the teacher panel. The API lives in server/."""

from html_kit import page

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


def teacher_page():
    body = f"""<h1><small>Teacher only</small>Teacher panel</h1>
<div id="gate" hidden><p class="goal">Please <a href="login.html">log in</a> with your teacher account.</p></div>
<div id="panel" hidden>
<h2>Students</h2>
<p>Updates by itself every 30 seconds.</p>
<div class="scroll"><table class="students"><thead><tr><th>Student</th><th>Last active</th><th>Levels</th>
<th>Stars</th><th>Diamonds</th><th>Best race</th><th>Homework done</th><th></th></tr></thead>
<tbody id="students"></tbody></table></div>
<section id="work" aria-live="polite"></section>
<h2>Add a student</h2>
<form id="add-form" class="account-form">
<label for="new-username">Username</label>
<input id="new-username" name="username" autocomplete="off" autocapitalize="off" spellcheck="false" required>
{password_field("Password (at least 8 characters)", "new-password").replace('id="password"', 'id="new-password"').replace('for="password"', 'for="new-password"')}
<button type="submit" class="btn">Add student</button>
<p class="checked" aria-live="polite"></p>
</form>
<h2>Change my password</h2>
<form id="pw-form" class="account-form">
{password_field("New password (at least 8 characters)", "new-password").replace('id="password"', 'id="my-password"').replace('for="password"', 'for="my-password"')}
<button type="submit" class="btn">Change password</button>
<p class="checked" aria-live="polite"></p>
</form>
</div>"""
    return page("Teacher Panel", body, root="", head=NOINDEX, scripts=("teacher.js",))
