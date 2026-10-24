const store = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); } catch {} },
  drop(key) { try { localStorage.removeItem(key); } catch {} },
};

// One save for the Game Zone and the lessons: diamonds, stars per task and per level, cars.
const save = { gems: 0, stars: {}, tasks: {}, best: 0, cars: ["red"], car: "red", sound: true, upto: 0 };
function freshSave() { // another tab may have won diamonds since this page opened
  try { Object.assign(save, JSON.parse(store.get("game")) || {}); } catch {}
}
freshSave();
const keep = () => store.set("game", JSON.stringify(save));
const GEMS_PER_STAR = 2;

// A task passed with `stars` (1 to 3). Only new stars win diamonds, so redoing a task never farms them.
function winTask(id, stars) {
  freshSave();
  const before = save.tasks[id] || 0;
  const gems = Math.max(0, stars - before) * GEMS_PER_STAR;
  save.tasks[id] = Math.max(before, stars);
  save.gems += gems;
  keep();
  return gems;
}
const starText = (n) => "★".repeat(n) + "☆".repeat(3 - n);

let audio = null;
function beep(freq, ms = 120) {
  if (!save.sound) return;
  try {
    audio = audio || new AudioContext();
    const osc = audio.createOscillator();
    const vol = audio.createGain();
    const end = audio.currentTime + ms / 1000;
    osc.type = "square";
    osc.frequency.value = freq;
    vol.gain.setValueAtTime(0.06, audio.currentTime);
    vol.gain.exponentialRampToValueAtTime(0.001, end);
    osc.connect(vol).connect(audio.destination);
    osc.start();
    osc.stop(end);
  } catch {}
}
const tune = (notes) => notes.forEach((f, i) => setTimeout(() => beep(f, 150), i * 110));

function confetti() {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  let box = document.querySelector(".confetti");
  if (!box) {
    box = document.createElement("div");
    box.className = "confetti";
    box.setAttribute("aria-hidden", "true");
    document.body.append(box);
  }
  const colors = ["#5dbb3f", "#f4c430", "#26c6da", "#e53935", "#1e88e5"];
  for (let i = 0; i < 48; i++) {
    const bit = document.createElement("i");
    bit.style.left = Math.random() * 100 + "vw";
    bit.style.background = colors[i % colors.length];
    bit.style.animationDelay = Math.random() * 0.5 + "s";
    bit.style.setProperty("--dx", (Math.random() - 0.5) * 240 + "px");
    box.append(bit);
  }
  setTimeout(() => box.replaceChildren(), 3000);
}

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

  const say = (cls, items) => {
    const list = document.createElement(items.length > 1 ? "ul" : "p");
    if (items.length > 1) items.forEach((text) => list.append(Object.assign(document.createElement("li"), { textContent: text })));
    else list.textContent = items[0];
    result.className = "checked " + cls;
    result.replaceChildren(list);
  };
  const mistakes = () => (window.checkHTML ? checkHTML(code.value) : []).map((p) => `Line ${p.line}: ${p.msg}`);
  box.querySelector(".check-btn").addEventListener("click", () => {
    const problems = mistakes();
    if (problems.length) say("bad", problems);
    else say("good", ["No mistakes found. Does the page on the right look the way you want?"]);
  });

  // "Check my answer": ticks the goals. Fewer tries, more stars; new stars win diamonds.
  const answer = box.querySelector(".answer-btn");
  if (!answer) { show(); return; }
  const goals = [...box.querySelectorAll(".goals li")];
  const id = box.dataset.save;
  const badge = document.createElement("span");
  badge.className = "task-stars";
  const drawBadge = () => {
    const got = save.tasks[id] || 0;
    badge.textContent = got ? starText(got) : "";
    box.classList.toggle("won", got > 0);
  };
  answer.after(badge);
  drawBadge();
  let tries = 0;
  answer.addEventListener("click", () => {
    const doc = new DOMParser().parseFromString(code.value, "text/html");
    let left = 0;
    for (const li of goals) {
      const ok = meetsRule(li, code.value, doc);
      li.classList.toggle("done", ok);
      if (!ok) left += 1;
    }
    const problems = mistakes();
    if (left || problems.length) {
      tries += 1;
      beep(150, 300);
      box.classList.remove("shake");
      void box.offsetWidth;
      box.classList.add("shake");
      if (problems.length) say("bad", ["Fix these mistakes first:", ...problems]);
      else say("bad", [`Almost! ${left} goal${left > 1 ? "s" : ""} to go. Look for the goals without a tick.`]);
      return;
    }
    const stars = tries <= 3 ? 3 : 2; // checking is part of learning: 3 misses are free
    const gems = winTask(id, stars);
    drawBadge();
    const homework = document.querySelector(".copy-all[data-reward]");
    const bonus = homework ? homeworkReward(homework.dataset.reward) : "";
    say("good win", [`Task done! ${starText(stars)}` + (gems ? ` +${gems} diamonds!` : "") + bonus]);
    tune([523, 659, 784, 1047]);
    confetti();
    if (window.drawProgress) drawProgress();
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

// Every homework task of a lesson passed: +10 diamonds, once per lesson.
function homeworkReward(lesson) {
  freshSave();
  save.homework = save.homework || {};
  if (save.homework[lesson]) return "";
  const ids = [...document.querySelectorAll(".play[data-save]")].map((b) => b.dataset.save);
  if (!ids.every((id) => save.tasks[id])) return " Pass every task to win 10 bonus diamonds.";
  save.homework[lesson] = true;
  save.gems += 10;
  keep();
  return " All homework done: +10 bonus diamonds!";
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

// Light / dark switch. The page head applies the saved choice before the page draws.
const nav = document.querySelector("nav.top");
if (nav) {
  const dark = () => document.documentElement.dataset.theme === "dark"
    || (!document.documentElement.dataset.theme && matchMedia("(prefers-color-scheme: dark)").matches);
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "theme-btn";
  const label = () => { btn.textContent = dark() ? "Light" : "Dark"; btn.setAttribute("aria-label", `Switch to ${btn.textContent.toLowerCase()} mode`); };
  btn.addEventListener("click", () => {
    const next = dark() ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    store.set("theme", next);
    label();
  });
  label();
  nav.append(btn);
}
