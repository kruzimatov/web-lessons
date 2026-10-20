// Levels, badges and progress bars, all worked out from the one save in kit.js.
// kit.js calls drawProgress() after every won task; a new badge or level pops up as a toast.
(() => {
  const LESSONS = 16;
  const TASK_IDS = (n) => [1, 2, 3, 4, 5].map((k) => `p${n}-${k}`).concat([1, 2, 3].map((k) => `h${n}-${k}`));
  const LEVELS = [[0, "Beginner"], [50, "Explorer"], [150, "Builder"], [300, "Coder"], [600, "Web Wizard"], [1000, "HTML Hero"], [2000, "Legend"]];
  const sum = (o) => Object.values(o || {}).reduce((a, b) => a + b, 0);

  function facts() {
    const tasks = save.tasks || {};
    const lessonDone = (n) => TASK_IDS(n).every((id) => tasks[id]);
    const lessons = Array.from({ length: LESSONS }, (_, i) => i + 1);
    return {
      done: Object.keys(tasks).length,
      perfect: Object.values(tasks).filter((s) => s === 3).length,
      fullLessons: lessons.filter(lessonDone).length,
      week1: [1, 2, 3, 4, 5, 6].every(lessonDone),
      homework: Object.keys(save.homework || {}).length,
      levels: Object.keys(save.stars || {}).length,
      xp: 10 * (sum(tasks) + sum(save.stars)),
    };
  }

  const BADGES = [
    ["First step", "Pass your first task", (f) => f.done >= 1],
    ["Ten tasks", "Pass 10 tasks", (f) => f.done >= 10],
    ["Perfect five", "Get 3 stars on 5 tasks", (f) => f.perfect >= 5],
    ["Lesson master", "Pass all 8 tasks of one lesson", (f) => f.fullLessons >= 1],
    ["Homework hero", "Finish the homework of 3 lessons", (f) => f.homework >= 3],
    ["Fifty tasks", "Pass 50 tasks", (f) => f.done >= 50],
    ["Week 1 done", "Pass every task in lessons 1 to 6", (f) => f.week1],
    ["Block builder", "Finish 5 Game Zone levels", (f) => f.levels >= 5],
    ["Speed racer", "Score 20 in Tag Racer", () => (save.best || 0) >= 20],
    ["Car collector", "Own 3 cars", () => (save.cars || []).length >= 3],
    ["Diamond rich", "Have 100 diamonds", () => (save.gems || 0) >= 100],
    ["Course champion", "Pass all 128 tasks", (f) => f.done >= LESSONS * 8],
  ];

  function level(xp) {
    let k = 0;
    while (k + 1 < LEVELS.length && xp >= LEVELS[k + 1][0]) k += 1;
    const next = LEVELS[k + 1];
    return { n: k + 1, name: LEVELS[k][1], from: LEVELS[k][0], to: next ? next[0] : null };
  }

  const make = (tag, cls, text) => Object.assign(document.createElement(tag), { className: cls, textContent: text ?? "" });
  function bar(part, whole) {
    const box = make("div", "bar");
    box.setAttribute("role", "progressbar");
    box.setAttribute("aria-valuemin", "0");
    box.setAttribute("aria-valuemax", String(whole));
    box.setAttribute("aria-valuenow", String(part));
    box.append(make("i"));
    box.firstChild.style.width = `${whole ? Math.round((100 * part) / whole) : 0}%`;
    return box;
  }

  function toast(text) {
    let box = document.querySelector(".toasts");
    if (!box) {
      box = make("div", "toasts");
      box.setAttribute("aria-live", "polite");
      document.body.append(box);
    }
    const t = make("p", "toast", text);
    box.append(t);
    setTimeout(() => t.remove(), 4000);
  }

  // Lesson cards on the home page and the bar under a lesson's menu.
  function lessonBar(n) {
    const ids = TASK_IDS(n);
    const passed = ids.filter((id) => save.tasks[id]).length;
    const stars = ids.reduce((a, id) => a + (save.tasks[id] || 0), 0);
    const box = make("div", "lesson-progress" + (passed === ids.length ? " full" : ""));
    box.append(bar(passed, ids.length),
      make("small", "", passed === ids.length ? `All ${ids.length} tasks done! ★ ${stars}` : `${passed} of ${ids.length} tasks done · ★ ${stars}`));
    return box;
  }

  function playerCard(f, lv) {
    const card = document.getElementById("me");
    if (!card) return;
    const head = make("div", "player-head");
    head.append(make("span", "player-level", String(lv.n)));
    const who = make("div");
    who.append(make("strong", "", `Level ${lv.n}: ${lv.name}`),
      make("small", "", lv.to ? `${f.xp} XP · ${lv.to - f.xp} XP to level ${lv.n + 1}` : `${f.xp} XP · top level!`));
    head.append(who);
    const nums = make("p", "player-nums");
    nums.append(make("span", "", `★ ${sum(save.tasks) + sum(save.stars)} stars`), make("span", "", `◆ ${save.gems} diamonds`),
      make("span", "", `${f.done} of ${LESSONS * 8} tasks`));
    const badges = make("ul", "badges");
    for (const [name, how, test] of BADGES) {
      const got = test(f);
      const li = make("li", got ? "got" : "");
      li.append(make("strong", "", name), make("span", "", got ? "Unlocked!" : how));
      badges.append(li);
    }
    card.replaceChildren(make("h2", "", "My trophies"), head, bar(f.xp - lv.from, (lv.to || f.xp) - lv.from), nums, badges);
    card.hidden = false;
  }

  function navChip(f, lv) {
    const nav = document.querySelector("nav.top");
    if (!nav || location.pathname.startsWith("/teacher")) return;
    let chip = nav.querySelector(".xp-chip");
    if (!chip) {
      chip = make("a", "xp-chip");
      chip.href = nav.querySelector("a").getAttribute("href") + "#me"; // the first link is Home
      nav.insertBefore(chip, nav.querySelector(".theme-btn"));
    }
    chip.textContent = `Lv ${lv.n} · ★ ${sum(save.tasks) + sum(save.stars)} · ◆ ${save.gems}`;
    chip.title = `Level ${lv.n}: ${lv.name}. See my trophies`;
  }

  window.drawProgress = () => {
    const f = facts();
    const lv = level(f.xp);
    // New badges and levels since last time: celebrate once, remember in the save (it syncs).
    const got = BADGES.filter(([, , test]) => test(f)).map(([name]) => name);
    const seen = save.badges || [];
    const fresh = got.filter((name) => !seen.includes(name));
    if (save.badges && fresh.length) fresh.forEach((name) => toast(`New badge: ${name}!`));
    if (save.level && lv.n > save.level) toast(`Level up! You are a ${lv.name} now.`);
    if (fresh.length || save.level !== lv.n) {
      save.badges = got;
      save.level = lv.n;
      keep();
    }
    navChip(f, lv);
    playerCard(f, lv);
    document.querySelectorAll(".card[data-n]").forEach((c) => {
      c.querySelector(".lesson-progress")?.remove();
      c.querySelector("h3").after(lessonBar(Number(c.dataset.n)));
    });
    const here = document.getElementById("here");
    const sub = document.querySelector(".subnav");
    if (here && sub) {
      document.querySelector(".subnav + .lesson-progress")?.remove();
      sub.after(lessonBar(Number(here.dataset.n)));
    }
  };
  drawProgress();
  document.addEventListener("visibilitychange", () => { if (!document.hidden) { freshSave(); drawProgress(); } });
})();
