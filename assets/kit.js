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

  box.querySelector(".check-btn").addEventListener("click", () => {
    const problems = window.checkHTML ? checkHTML(code.value) : [];
    const list = document.createElement(problems.length ? "ul" : "p");
    if (problems.length) {
      for (const p of problems) {
        const li = document.createElement("li");
        li.textContent = `Line ${p.line}: ${p.msg}`;
        list.append(li);
      }
    } else {
      list.textContent = "No problems found. Does the page on the right look the way you want?";
    }
    result.className = "checked " + (problems.length ? "bad" : "good");
    result.replaceChildren(list);
  });
  show();
});

document.querySelectorAll(".quiz").forEach((quiz) => {
  const verdict = quiz.querySelector(".verdict");
  quiz.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", () => {
      const ok = btn.dataset.ok === "1";
      btn.classList.add(ok ? "right" : "wrong");
      verdict.textContent = ok ? "Correct! Barakalla!" : "Not this one. Try again!";
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
