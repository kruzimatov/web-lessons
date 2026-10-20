const store = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); } catch {} },
  drop(key) { try { localStorage.removeItem(key); } catch {} },
};

// In form lessons a sent form stays on the page and says "Sent!" instead of leaving.
const FORM_HELPER = `<script>
document.addEventListener("submit", (e) => {
  e.preventDefault();
  const note = document.createElement("p");
  note.textContent = "Sent! (On a real website it goes to the server.)";
  note.style.cssText = "background:#e3f6ec;color:#16794a;padding:8px;font-weight:bold";
  e.target.after(note);
});
<\/script>`;

// Lazy boxes (data-lazy) start only when a page calls setupPlay, so hidden editors cost nothing.
function setupPlay(box) {
  if (box.dataset.ready) return;
  box.dataset.ready = "1";
  const code = box.querySelector("textarea.src");
  const view = box.querySelector("iframe");
  const result = box.querySelector(".checked");
  const start = code.value;
  const key = box.dataset.save && "code:" + box.dataset.save;
  const forms = view.sandbox.contains("allow-forms");
  const show = () => { view.srcdoc = code.value + (forms ? FORM_HELPER : ""); };
  if (key && store.get(key) !== null) code.value = store.get(key);
  const run = () => {
    show();
    result.replaceChildren();
    if (key) store.set(key, code.value);
  };

  // Colored editor with line numbers and auto-closing tags. Without internet, the plain box still works.
  let editor = null;
  if (window.CodeMirror) {
    editor = CodeMirror.fromTextArea(code, {
      mode: "htmlmixed", lineNumbers: true,
      autoCloseTags: { whenOpening: true, whenClosing: true, indentTags: [] }, // <p> gives <p></p> on one line
      tabSize: 2, indentUnit: 2, lineWrapping: true, viewportMargin: Infinity,
    });
    editor.on("change", () => { editor.save(); run(); });
  } else {
    code.addEventListener("input", run);
    code.addEventListener("keydown", (e) => {
      if (e.key !== "Tab") return;
      e.preventDefault();
      code.setRangeText("  ", code.selectionStart, code.selectionEnd, "end");
      run();
    });
  }

  box.querySelector(".reset").addEventListener("click", () => {
    if (editor) editor.setValue(start); else { code.value = start; run(); }
    if (key) store.drop(key);
  });

  const needs = (box.dataset.needs || "").split(" ").filter(Boolean);
  box.querySelector(".check-btn").addEventListener("click", () => {
    const missing = needs.filter((t) => !new RegExp(`<${t}[\\s>/]`, "i").test(code.value));
    const notes = missing.map((t) => `The task needs <${t}>. You have not used it yet`);
    const problems = notes.concat((window.checkHTML ? checkHTML(code.value) : []).map((p) => `Line ${p.line}: ${p.msg}`));
    const list = document.createElement(problems.length ? "ul" : "p");
    if (problems.length) {
      for (const text of problems) {
        const li = document.createElement("li");
        li.textContent = text;
        list.append(li);
      }
    } else {
      list.textContent = needs.length
        ? "No mistakes, and every tag the task needs is there. Read the task once more: is everything done?"
        : "No mistakes found. Does the page on the right look the way you want?";
    }
    result.className = "checked " + (problems.length ? "bad" : "good");
    result.replaceChildren(list);
  });
  show();
}
document.querySelectorAll(".play:not([data-lazy])").forEach(setupPlay);

// One right answer locks the question. Wrong answers lock one by one, so guessing shows.
document.querySelectorAll(".quiz").forEach((quiz) => {
  const verdict = quiz.querySelector(".verdict");
  const buttons = quiz.querySelectorAll("button");
  let tries = 0;
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      tries += 1;
      btn.disabled = true;
      if (btn.dataset.ok === "1") {
        btn.classList.add("right");
        buttons.forEach((b) => { b.disabled = true; });
        verdict.textContent = tries === 1 ? "Correct on the first try! Barakalla!" : `Correct! It took ${tries} tries.`;
      } else {
        btn.classList.add("wrong");
        verdict.textContent = "Not this one. Try again!";
      }
    });
  });
});

// Finished homework wins diamonds once per lesson. The Game Zone (game.js) reads the same save.
function homeworkReward(key) {
  const done = [...document.querySelectorAll(".play textarea.src")].every((t) =>
    t.value.trim() && t.value.trim() !== t.defaultValue.trim() && !(window.checkHTML && checkHTML(t.value).length));
  if (!done) return " Finish every task with no mistakes to win 10 diamonds.";
  let game = {};
  try { game = JSON.parse(store.get("game")) || {}; } catch {}
  game.homework = game.homework || {};
  if (game.homework[key]) return "";
  game.homework[key] = true;
  game.gems = (game.gems || 0) + 10;
  store.set("game", JSON.stringify(game));
  return " +10 diamonds! Spend them in the Game Zone.";
}

document.querySelectorAll(".copy-all").forEach((btn) => {
  const note = btn.parentElement.querySelector(".copied");
  btn.addEventListener("click", async () => {
    const tasks = [...document.querySelectorAll(".play textarea.src")]
      .map((t, i) => `Task ${i + 1}:\n${t.value.trim() || "(empty)"}`);
    const text = btn.dataset.title + "\n\n" + tasks.join("\n\n");
    const reward = btn.dataset.reward ? homeworkReward(btn.dataset.reward) : "";
    try {
      await navigator.clipboard.writeText(text);
      note.textContent = "Copied! Now paste it in Telegram." + reward;
    } catch {
      note.textContent = "Could not copy. Ask your teacher for help." + reward;
    }
  });
});

document.querySelectorAll(".anim").forEach((fig) => {
  const play = () => { fig.classList.remove("on"); void fig.offsetWidth; fig.classList.add("on"); };
  fig.querySelector(".replay").addEventListener("click", play);
  new IntersectionObserver((seen, watcher) => {
    if (seen[0].isIntersecting) { play(); watcher.disconnect(); }
  }, { threshold: 0.6 }).observe(fig);
});

// Remember the last lesson he opened, and offer it on the home page.
const here = document.getElementById("here");
if (here) store.set("last", JSON.stringify(here.dataset));
const resume = document.getElementById("continue");
if (resume) {
  try {
    const last = JSON.parse(store.get("last"));
    if (last && last.href) {
      resume.href = last.href;
      resume.textContent = `Continue: Lesson ${last.n}`;
    }
  } catch {}
}
