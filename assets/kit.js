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

document.querySelectorAll(".play").forEach((box) => {
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
});

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

document.querySelectorAll(".copy-all").forEach((btn) => {
  const note = btn.parentElement.querySelector(".copied");
  btn.addEventListener("click", async () => {
    const tasks = [...document.querySelectorAll(".play textarea.src")]
      .map((t, i) => `Task ${i + 1}:\n${t.value.trim() || "(empty)"}`);
    const text = btn.dataset.title + "\n\n" + tasks.join("\n\n");
    try {
      await navigator.clipboard.writeText(text);
      note.textContent = "Copied! Now paste it in Telegram.";
    } catch {
      note.textContent = "Could not copy. Ask your teacher for help.";
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
