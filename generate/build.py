"""Build every lesson from generate/lessons/lNN.py.

Usage (from the repo root): python3 generate/build.py
Writes the public website to site/ and the answers to teacher/ (not in git).
"""

import importlib.util
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from extra_pages import cheatsheet_page, overview_page, playground_page  # noqa: E402
from account import login_page, parent_page, teacher_page  # noqa: E402
from game import game_page  # noqa: E402
from html_kit import tags_in  # noqa: E402
from pages import answers_page, homework_page, index_page, lesson_page, practice_page  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
TEACHER = ROOT / "teacher"
LESSONS_DIR = Path(__file__).resolve().parent / "lessons"


def load_lessons():
    lessons = []
    for f in sorted(LESSONS_DIR.glob("l[0-9]*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        lessons.append(mod.LESSON)
    learned = set()
    for L in lessons:  # tags from this lesson and every one before it, for the "your idea" task
        learned |= set(tags_in(" ".join(code for code, _ in L["cheats"])))
        L["learned"] = sorted(learned)
    return lessons


def check_template(L):
    """Every lesson follows the same template. Stops the build if one does not."""
    name = f'lesson {L["n"]}'
    parts = []
    for b in L["blocks"]:
        if b[0] == "h":
            parts.append([0, 0])
        elif b[0] in ("quiz", "try"):
            assert parts, f"{name}: a block comes before the first part heading"
            parts[-1][b[0] == "try"] += 1
    assert 1 <= len(parts) <= 4, f"{name}: {len(parts)} parts, the template allows 1 to 4"
    per_part = L.get("quizzes_per_part", 1)  # the review lesson asks more
    for k, (quizzes, tries) in enumerate(parts, 1):
        assert quizzes == per_part, f"{name} part {k}: {quizzes} quiz questions, needs {per_part}"
        assert tries >= 1, f"{name} part {k}: needs at least 1 'try' editor"
    assert len(L["review"]) == (0 if L["n"] == 1 else 3), f"{name}: warm-up needs 3 quiz questions"
    assert len(L["practice"]) == 5, f"{name}: {len(L['practice'])} practice tasks, needs 5"
    for i, t in enumerate(L["practice"], 1):
        assert len(t["hints"]) == 2, f"{name} practice {i}: needs 2 hints"
    assert len(L["homework"]) == 2, f"{name}: needs 2 homework tasks (task 3, your idea, is added)"
    assert L["cheats"], f"{name}: needs cheat sheet entries"
    assert 3 <= len(L["mistakes"]) <= 5, f"{name}: needs 3 to 5 mistakes"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    lessons = load_lessons()
    for L in lessons:
        check_template(L)
    shutil.rmtree(SITE, ignore_errors=True)  # site/ is only build output
    shutil.copytree(ROOT / "assets", SITE / "assets")
    shutil.copytree(ROOT / "demo", SITE / "demo")
    for L in lessons:
        out = SITE / L["folder"]
        write(out / "lesson.html", lesson_page(L))
        write(out / "practice.html", practice_page(L))
        write(out / "homework.html", homework_page(L))
        write(TEACHER / f'lesson{L["n"]:02d}_answers.html', answers_page(L))
        print("built", L["folder"])
    write(SITE / "index.html", index_page(lessons))
    write(SITE / "cheatsheet.html", cheatsheet_page(lessons))
    write(SITE / "playground.html", playground_page())
    write(SITE / "game.html", game_page())
    write(SITE / "login.html", login_page())
    write(SITE / "teacher.html", teacher_page(lessons))
    write(SITE / "parent.html", parent_page(lessons))
    write(TEACHER / "overview.html", overview_page(lessons))
    print("built index, cheat sheet, playground, game, login, teacher panel, parent page, teacher overview")


if __name__ == "__main__":
    main()
