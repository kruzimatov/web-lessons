"""Course-wide pages: the student's tag cheat sheet and playground, and the teacher overview."""

from html_kit import esc, fmt, page, part_titles, play
from pages import LEVELS, homework_tasks

FREE_SANDBOX = "allow-forms allow-scripts allow-popups allow-popups-to-escape-sandbox"


def cheatsheet_page(lessons):
    parts = ['<h1><small>Look it up here</small>My tags</h1>',
             '<p class="goal">Forgot a tag? Find the lesson, copy the example, change it.</p>']
    for L in lessons:
        rows = "".join(f"<tr><td><code>{esc(code)}</code></td><td>{fmt(meaning)}</td></tr>"
                       for code, meaning in L["cheats"])
        parts.append(f'<h2 id="lesson-{L["n"]}">Lesson {L["n"]}: {fmt(L["title"])}</h2>'
                     f'<div class="scroll"><table class="cheats"><tbody>{rows}</tbody></table></div>')
    return page("My Tags", "\n".join(parts), root="", current="cheatsheet.html")


def playground_page():
    parts = ['<h1><small>No tasks, no rules</small>My playground</h1>',
             '<p class="goal">Build anything you want. Your code saves by itself in this browser.</p>',
             play("<!-- Build anything you like! -->\n<h1>My page</h1>\n", save="free-1", sandbox=FREE_SANDBOX, big=True)]
    return page("My Playground", "\n".join(parts), root="", current="playground.html")


def anims_of(L):
    return [b[1] for b in L["blocks"] if b[0] == "anim"]


def overview_page(lessons):
    """Teacher only: every lesson on one page, made from the same lesson files."""
    rows = "".join(
        f'<tr><td><a href="#lesson-{L["n"]}">{L["n"]}</a></td><td>{L["week"]}</td><td>{fmt(L["title"])}</td>'
        f'<td>{len(part_titles(L["blocks"]))}</td><td>{len(anims_of(L))}</td>'
        f'<td>{", ".join(esc(c) for c, _ in L["cheats"][:3])}</td></tr>'
        for L in lessons)
    parts = ['<h1><small>Teacher only</small>Course overview</h1>',
             f'<p class="goal">All {len(lessons)} lessons on one page. Click a number to jump to it. '
             'Every lesson: warm-up, parts, watch out, 5 practice tasks with 2 hints each, 3 homework tasks.</p>',
             '<div class="scroll"><table><thead><tr><th>#</th><th>Week</th><th>Lesson</th><th>Parts</th>'
             f'<th>Animations</th><th>Main tags</th></tr></thead><tbody>{rows}</tbody></table></div>']
    for L in lessons:
        f = f'../site/{L["folder"]}'
        links = " &middot; ".join(
            f'<a href="{href}">{name}</a>' for href, name in (
                (f"{f}/lesson.html", "Lesson"), (f"{f}/practice.html", "Practice"),
                (f"{f}/homework.html", "Homework"), (f"lesson{L['n']:02d}_answers.html", "Answers"),
                (f"{f}/slides.pptx", "Slides")))
        part_list = "".join(f"<li>{fmt(t)}</li>" for t in part_titles(L["blocks"]))
        practice = "".join(
            f'<li><strong>{LEVELS[i]}:</strong> {fmt(t["task"])}'
            f'<br><small>Hints: {fmt(t["hints"][0])} / {fmt(t["hints"][1])}</small></li>'
            for i, t in enumerate(L["practice"]))
        homework = "".join(f"<li>{fmt(t['task'])}</li>" for t in homework_tasks(L))
        parts.append(
            f'<section class="lesson-card" id="lesson-{L["n"]}">'
            f'<h2>Lesson {L["n"]} &middot; Week {L["week"]}: {fmt(L["title"])}</h2>'
            f'<p>{fmt(L["goal"])}</p><p>{links}</p>'
            f'<h3>Parts</h3><ol>{part_list}</ol>'
            f'<p><strong>Animations:</strong> {", ".join(anims_of(L)) or "none (practice day)"}</p>'
            f'<p><strong>Warm-up questions:</strong> {len(L["review"])} &middot; '
            f'<strong>Mistakes listed:</strong> {len(L["mistakes"])}</p>'
            f'<h3>Practice</h3><ol>{practice}</ol>'
            f'<h3>Homework</h3><ol>{homework}</ol></section>')
    return page("Course Overview", "\n".join(parts), root="../site/")
