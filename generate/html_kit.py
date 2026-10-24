"""Small HTML building blocks shared by every page."""

import html
import re
from pathlib import Path

ANIMS_DIR = Path(__file__).resolve().parent / "anims"
SANDBOX = "allow-popups allow-popups-to-escape-sandbox"

CM = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16"
EDITOR_FILES = [
    "codemirror.min.js", "mode/xml/xml.min.js", "mode/javascript/javascript.min.js", "mode/css/css.min.js",
    "mode/htmlmixed/htmlmixed.min.js", "addon/fold/xml-fold.min.js", "addon/edit/closetag.min.js",
]


def esc(text):
    return html.escape(text, quote=False)


def fmt(text):
    """Escape, then `code` and **bold**."""
    t = esc(text)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)


def plain(text):
    return text.replace("`", "").replace("**", "")


def tags_in(code):
    """Tag names used in a piece of HTML, for example {"h1", "p"}."""
    return sorted({t.lower() for t in re.findall(r"<([a-zA-Z][a-zA-Z0-9]*)", code)})


def attr(text):
    return html.escape(text, quote=True)


def need_item(label, rule, n):
    """One goal: a CSS selector, a /regex/, "any:a,b,c" or "tags:" (check.js, meetsRule)."""
    kind = "re" if rule.startswith("/") else "any" if rule.startswith("any:") else "tags" if rule == "tags:" else "sel"
    rule = rule[4:] if kind == "any" else "" if kind == "tags" else rule
    return f'<li data-{kind}="{attr(rule)}" data-n="{n}">{fmt(label)}</li>'


def play(start, task="", save="", sandbox=SANDBOX, checks=(), big=False, lazy=False):
    """Live editor. With `save`, his code is kept in the browser between visits.
    `checks`: the task's goals (answer_checks.py); "Check my answer" ticks them and gives stars.
    `lazy`: the editor starts only when the page calls setupPlay (kit.js)."""
    head = f'<p class="task">{fmt(task)}</p>' if task else ""
    keep = f' data-save="{save}"' if save else ""
    keep += " data-lazy" if lazy else ""
    goals = ('<ul class="goals" aria-label="Goals">' + "".join(need_item(*c) for c in checks) + "</ul>") if checks else ""
    answer = '<button type="button" class="answer-btn">Check my answer</button>' if checks else ""
    return (
        f'<div class="play{" big" if big else ""}"{keep}>{head}{goals}<div class="panes">'
        f'<textarea class="src" spellcheck="false" autocapitalize="off" aria-label="Code">{esc(start)}</textarea>'
        f'<iframe title="Result" sandbox="{sandbox}"></iframe></div>'
        f'<div class="tools">{answer}<button type="button" class="check-btn">Check my code</button>'
        f'<button type="button" class="reset">Start again</button></div>'
        f'<div class="checked" aria-live="polite"></div></div>'
    )


def quiz(question, options, right):
    btns = "".join(
        f'<button type="button" data-ok="{int(i == right)}">{fmt(o)}</button>'
        for i, o in enumerate(options)
    )
    return (
        f'<div class="quiz"><p class="q">{fmt(question)}</p>'
        f'<div class="opts">{btns}</div><p class="verdict" aria-live="polite"></p></div>'
    )


def table(head, rows):
    th = "".join(f"<th>{fmt(h)}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td>{fmt(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def anim(name, caption):
    svg = (ANIMS_DIR / f"{name}.html").read_text(encoding="utf-8")
    return (
        f'<figure class="anim">{svg}<figcaption>{fmt(caption)}</figcaption>'
        f'<button type="button" class="replay">Play again</button></figure>'
    )


def code_block(code, caption=""):
    cap = f"<figcaption>{fmt(caption)}</figcaption>" if caption else ""
    return f'<figure class="code">{cap}<pre><code>{esc(code)}</code></pre></figure>'


BLOCKS = {
    "say": lambda t: f"<p>{fmt(t)}</p>",
    "uz": lambda t: f'<p class="uz" lang="uz">{fmt(t)}</p>',
    "big": lambda t: f'<p class="big">{fmt(t)}</p>',
    "code": code_block,
    "quiz": quiz,
    "table": table,
    "steps": lambda items: '<ol class="steps">' + "".join(f"<li>{fmt(i)}</li>" for i in items) + "</ol>",
    "anim": anim,
}


def part_titles(blocks):
    return [b[1] for b in blocks if b[0] == "h"]


def blocks_html(blocks, sandbox=SANDBOX):
    out, part = [], 0
    for b in blocks:
        if b[0] == "h":
            part += 1
            out.append(f'<h2 id="part-{part}">{fmt(b[1])}</h2>')
        elif b[0] == "try":
            out.append(play(b[2], b[1], sandbox=sandbox))
        else:
            out.append(BLOCKS[b[0]](*b[1:]))
    return "\n".join(out)


NAV = [("index.html", "Home"), ("cheatsheet.html", "My tags"), ("playground.html", "Playground"), ("game.html", "Game")]


def page(title, body, root="../../", current="", head="", scripts=(), bare=False):
    """A full page. `root` is the way back to the site root; `current` marks the open menu item.
    `head` and `scripts` add page-only styles and scripts (loaded after kit.js).
    `bare`: no menu, editor or game scripts, only `scripts` (the parent page)."""
    nav = "".join(
        f'<a href="{root}{href}"{" aria-current=\"page\"" if href == current else ""}>{name}</a>'
        for href, name in NAV)
    nav = "" if bare else f'<nav class="top">{nav}</nav>'
    kit = "" if bare else "".join(f'<script src="{CM}/{f}"></script>' for f in EDITOR_FILES) + "".join(
        f'\n<script src="{root}assets/{s}"></script>' for s in ("check.js", "kit.js", "progress.js", "sync.js"))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&display=swap">
{"" if bare else f'<link rel="stylesheet" href="{CM}/codemirror.min.css">'}
<link rel="stylesheet" href="{root}assets/style.css">
<script>try {{ const t = localStorage.getItem("theme"); if (t) document.documentElement.dataset.theme = t; }} catch {{}}</script>
{head}</head>
<body>
{nav}
{body}
{kit}
{"".join(f'<script src="{root}assets/{s}"></script>' for s in scripts)}
</body>
</html>
"""
