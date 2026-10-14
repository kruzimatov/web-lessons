"""The four pages of every lesson, plus the course home page."""

from html_kit import SANDBOX, blocks_html, esc, fmt, page, part_titles, plain, play

LEVELS = ["Easy", "Medium", "Find the bug", "Medium", "Mini project"]

IDEAS = [
    "my dream house, my favorite cartoon, a day at the zoo",
    "a superhero I made up, my football team, space and planets",
    "my favorite food, dinosaurs, a trip I want to take",
    "my best friend, robots, the sea and fish",
    "a game I invented, my pet, my school",
    "cars, a magic world, my birthday party",
]

STUCK = """<details class="stuck" open><summary>When I'm stuck</summary><ol>
<li>Read my code slowly, line by line.</li>
<li>Press <strong>Check my code</strong> and read what it says.</li>
<li>Check that every tag that opens also closes.</li>
<li>Look it up in <a href="../../cheatsheet.html">My tags</a>.</li>
<li>Compare with the example in the lesson.</li>
<li>Try Hint 1, then Hint 2.</li>
<li>Still stuck? Ask your teacher.</li>
</ol></details>"""


def homework_tasks(L):
    """The 2 written tasks, then a "your idea" task he picks himself."""
    tags = ", ".join(f"`{code}`" for code, _ in L["cheats"][:4])
    topics = IDEAS[L["n"] % len(IDEAS)]
    idea = {
        "task": f"Your idea! Build any page you like. Use at least 3 things from today, for example {tags}. "
                f"No idea? Try: {topics}.",
        "answer": "(his own page: check that it uses at least 3 things from today and that every tag closes)",
    }
    return L["homework"] + [idea]


def header(L, current):
    links = [("lesson.html", "Lesson"), ("practice.html", "Practice"), ("homework.html", "Homework")]
    mark = ' aria-current="page"'
    nav = "".join(f'<a href="{href}"{mark if href == current else ""}>{name}</a>' for href, name in links)
    return (
        f'<h1><small>Lesson {L["n"]} &middot; Week {L["week"]}</small>{fmt(L["title"])}</h1>'
        f'<div class="subnav">{nav}</div>'
    )


def lesson_page(L):
    jumps = ['<a href="#warm-up">Warm-up</a>'] if L["review"] else []
    jumps += [f'<a href="#part-{k}">{fmt(t.split(":")[0])}</a>' for k, t in enumerate(part_titles(L["blocks"]), 1)]
    jumps.append('<a href="#watch-out">Watch out</a>')
    parts = [header(L, "lesson.html"), f'<p class="goal">{fmt(L["goal"])}</p>',
             f'<nav class="jump" aria-label="On this page">{"".join(jumps)}</nav>']
    if L["review"]:
        parts += ['<h2 id="warm-up">Warm-up</h2>', blocks_html(L["review"])]
    parts.append(blocks_html(L["blocks"], L.get("sandbox", SANDBOX)))
    items = "".join(f"<li>{fmt(m)}</li>" for m in L["mistakes"])
    parts += ['<h2 id="watch-out">Watch out!</h2>', f'<ul class="mistakes">{items}</ul>']
    parts.append('<footer>Next: <a href="practice.html">Practice tasks</a></footer>')
    return page(f'Lesson {L["n"]}: {plain(L["title"])}', "\n".join(parts))


def practice_page(L):
    parts = [header(L, "practice.html"), STUCK]
    for i, t in enumerate(L["practice"], 1):
        parts.append(f"<h3>Task {i} &middot; {LEVELS[i - 1]}</h3>")
        parts.append(play(t["start"], t["task"], save=f"p{L['n']}-{i}", sandbox=L.get("sandbox", SANDBOX)))
        parts.append('<div class="hints">' + "".join(
            f'<details class="hint"><summary>Hint {k}</summary><p>{fmt(h)}</p></details>'
            for k, h in enumerate(t["hints"], 1)) + "</div>")
    return page(f'Practice {L["n"]}: {plain(L["title"])}', "\n".join(parts))


def homework_page(L):
    parts = [header(L, "homework.html"),
             "<p>Write your code in the boxes. It saves by itself. When you finish, press "
             "<strong>Copy my homework</strong> and send it to your teacher on Telegram. "
             "Finish your homework on the same device you started on.</p>", STUCK]
    for i, t in enumerate(homework_tasks(L), 1):
        parts.append(f"<h3>Task {i}{' &middot; Your idea' if i == 3 else ''}</h3>")
        parts.append(play(t.get("start", ""), t["task"], save=f"h{L['n']}-{i}", sandbox=L.get("sandbox", SANDBOX)))
    parts.append(f'<p><button type="button" class="copy-all" data-title="Lesson {L["n"]} homework">'
                 'Copy my homework</button> <span class="copied" aria-live="polite"></span></p>')
    return page(f'Homework {L["n"]}: {plain(L["title"])}', "\n".join(parts))


def answers_page(L):
    """Teacher only. Lives in teacher/, outside site/, never published."""
    parts = [f'<h1><small>Teacher only &middot; Lesson {L["n"]}</small>Answers: {fmt(L["title"])}</h1>']
    for name, tasks in (("Practice", L["practice"]), ("Homework", homework_tasks(L))):
        parts.append(f"<h2>{name}</h2>")
        for i, t in enumerate(tasks, 1):
            parts.append(f'<h3>Task {i}</h3><p>{fmt(t["task"])}</p>'
                         f'<figure class="code"><pre><code>{esc(t["answer"])}</code></pre></figure>')
    return page(f'Answers {L["n"]}: {plain(L["title"])}', "\n".join(parts), root="../site/")


def index_page(lessons):
    rows = "".join(
        f'<tr><td>{L["n"]}</td><td>{L["week"]}</td>'
        f'<td><a href="{L["folder"]}/lesson.html">{fmt(L["title"])}</a></td></tr>'
        for L in lessons
    )
    body = (
        '<h1><small>HTML + CSS from zero</small>My Web Course</h1>'
        '<p class="goal">Every lesson: learn, practise, then 3 homework tasks. '
        '<a href="demo/index.html">See what you will build</a>.</p>'
        f'<div class="scroll"><table><thead><tr><th>#</th><th>Week</th><th>Lesson</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div>'
    )
    return page("My Web Course", body, root="")
