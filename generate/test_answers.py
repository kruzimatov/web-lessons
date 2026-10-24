"""Every task can be passed: its model answer (or a sample answer) passes its "Check my answer" goals,
also written kid-style with capital tags like <P> and with 'single quotes'; unchanged start code does not; no goal asks for more than it allows.
Runs the real check.js in headless Chrome, because the goals use the browser's own HTML parser.

Usage (from the repo root): python3 generate/test_answers.py
"""

import html
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build import ROOT, load_lessons  # noqa: E402
from pages import homework_tasks  # noqa: E402
from answer_checks import checks_for  # noqa: E402

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

RUN = r"""
const out = [];
for (const t of TASKS) {
  const rules = t.rules.map(([rule, n]) => {
    const li = document.createElement("li");
    const kind = rule.startsWith("/") ? "re" : rule.startsWith("any:") ? "any" : rule === "tags:" ? "tags" : "sel";
    li.dataset[kind] = kind === "any" ? rule.slice(4) : kind === "tags" ? "" : rule;
    li.dataset.n = n;
    return li;
  });
  const passes = (src) => {
    const doc = new DOMParser().parseFromString(src, "text/html");
    return rules.filter((li) => !meetsRule(li, src, doc)).map((li) => li.dataset.re || li.dataset.sel || li.dataset.any || "3 different tags");
  };
  const bad = t.rules.filter(([rule]) => !rule.startsWith("/") && rule !== "tags:").flatMap(([rule]) =>
    (rule.startsWith("any:") ? rule.slice(4).split(",") : [rule]).filter((sel) => {
      try { document.querySelectorAll(sel); return false; } catch { return true; }
    }));
  bad.forEach((sel) => out.push(`${t.key}: invalid selector ${sel}`));
  t.rules.filter(([rule, n]) => rule.startsWith("any:") && n > rule.slice(4).split(",").length)
    .forEach(([rule, n]) => out.push(`${t.key}: can never pass, needs ${n} of only ${rule.slice(4).split(",").length}: ${rule}`));
  const shout = t.answer.replace(/<(\/?)([a-z][a-z0-9]*)/g, (m, slash, tag) => `<${slash}${tag.toUpperCase()}`);
  passes(t.answer).forEach((rule) => out.push(`${t.key}: model answer fails ${rule}`));
  passes(shout).forEach((rule) => out.push(`${t.key}: answer with capital tags fails ${rule}`));
  const single = t.answer.replace(/="([^"']*)"/g, "='$1'");
  passes(single).forEach((rule) => out.push(`${t.key}: answer with 'single quotes' fails ${rule}`));
  checkHTML(t.answer).forEach((p) => out.push(`${t.key}: model answer has a mistake: ${p.msg}`));
  if (!passes(t.start).length && !checkHTML(t.start).length) out.push(`${t.key}: start code already passes`);
}
document.getElementById("out").textContent = JSON.stringify(out);
"""


# Tasks whose answer is his own work: a sample of what he might write.
SAMPLES = {
    "p16-2": '<nav><a href="index.html">Home</a> <a href="hobbies.html">Hobbies</a></nav>\n<table>\n<tr><th>Hobby</th></tr>\n'
             '<tr><td>Football</td></tr>\n</table>\n<iframe src="https://www.youtube.com/embed/x" title="Video"></iframe>',
    "p16-4": '<form>\n<label for="name">Name</label> <input id="name">\n<input type="radio" id="a" name="pet"> <label for="a">Cat</label>\n'
             '<input type="radio" id="b" name="pet"> <label for="b">Dog</label>\n<button>Send</button>\n</form>',
    "p16-5": "<p>My favorite page is hobbies because it has my football video.</p>",
    # His real lesson 1 idea, written after lesson 2: h1 and p from today, br sub sup strong from later.
    "h1-3": "<h1>Title</h1>\n<p>my note:</p>\n<p>hello guys im happy to see you<br>in my website<br>"
            "h20 to h<sub>2</sub>o 52 to 5<sup>2</sup> hello=<Strong>hello</Strong></p>\n<P>school is tomorrow</P>",
}


# Real answers he wrote (or would write) in his own words: each must pass too.
KID = {
    "p1-5": "<h1>My favorite ANIMAL is BEARR</h1>\n<!--no need-->\n<h2>it eats fish &amp; berries</h2>\n<p>yummy</p>\n"
            "<!-- part 2 -->\n<h2>lives at forest</h2>\n<p>nothing here</p>",
}


def tasks():
    for L in load_lessons():
        for kind, items in (("p", L["practice"]), ("h", homework_tasks(L))):
            for i, t in enumerate(items, 1):
                key = f"{kind}{L['n']}-{i}"
                rules = t.get("checks") or checks_for(key)
                answer = SAMPLES.get(key) or t["answer"]
                if answer.startswith("("):  # "your idea": a page like the lesson's mini project or first homework
                    answer = next(a for a in (L["practice"][4]["answer"], items[0]["answer"]) if not a.startswith("("))
                if key in KID:
                    yield {"key": key + " (his words)", "answer": KID[key], "start": t.get("start", ""), "rules": [[r, n] for _, r, n in rules]}
                yield {"key": key, "answer": answer, "start": t.get("start", ""), "rules": [[r, n] for _, r, n in rules]}


def main():
    data = list(tasks())
    check_js = (ROOT / "assets" / "check.js").read_text(encoding="utf-8")
    tasks_js = json.dumps(data).replace("</", "<\\/")  # answers like </p> must not end the script
    page = (f'<!DOCTYPE html><meta charset="utf-8"><pre id="out">not run</pre><script>{check_js}</script>'
            f'<script>const TASKS = {tasks_js};{RUN}</script>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(page)
    try:
        dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--dump-dom", f"file://{f.name}"],
                             capture_output=True, text=True, timeout=60).stdout
    finally:
        os.unlink(f.name)
    start = dom.index('<pre id="out">') + len('<pre id="out">')
    raw = dom[start:dom.index("</pre>", start)]
    if raw == "not run":
        sys.exit("answers: the test script did not run")
    problems = json.loads(html.unescape(raw))
    for p in problems:
        print(p)
    if problems:
        sys.exit(f"answers: {len(problems)} problems")
    print(f"answers: all {len(data)} tasks pass")


if __name__ == "__main__":
    main()
