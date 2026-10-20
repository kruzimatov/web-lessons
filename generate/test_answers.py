"""Every model answer passes its "Check my answer" goals; unchanged start code does not.
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

RUN = """
const out = [];
for (const t of TASKS) {
  const rules = t.rules.map(([rule, n]) => {
    const li = document.createElement("li");
    const kind = rule.startsWith("/") ? "re" : rule.startsWith("any:") ? "any" : "sel";
    li.dataset[kind] = kind === "any" ? rule.slice(4) : rule;
    li.dataset.n = n;
    return li;
  });
  const passes = (src) => {
    const doc = new DOMParser().parseFromString(src, "text/html");
    return rules.filter((li) => !meetsRule(li, src, doc)).map((li) => li.dataset.re || li.dataset.sel || li.dataset.any);
  };
  const bad = t.rules.filter(([rule]) => !rule.startsWith("/")).flatMap(([rule]) =>
    (rule.startsWith("any:") ? rule.slice(4).split(",") : [rule]).filter((sel) => {
      try { document.querySelectorAll(sel); return false; } catch { return true; }
    }));
  bad.forEach((sel) => out.push(`${t.key}: invalid selector ${sel}`));
  if (t.answer !== null) {
    passes(t.answer).forEach((rule) => out.push(`${t.key}: model answer fails ${rule}`));
    checkHTML(t.answer).forEach((p) => out.push(`${t.key}: model answer has a mistake: ${p.msg}`));
  }
  if (!passes(t.start).length && !checkHTML(t.start).length) out.push(`${t.key}: start code already passes`);
}
document.getElementById("out").textContent = JSON.stringify(out);
"""


def tasks():
    for L in load_lessons():
        for kind, items in (("p", L["practice"]), ("h", homework_tasks(L))):
            for i, t in enumerate(items, 1):
                key = f"{kind}{L['n']}-{i}"
                rules = t.get("checks") or checks_for(key)
                answer = None if t["answer"].startswith("(") else t["answer"]
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
