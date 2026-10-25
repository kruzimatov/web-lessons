// Teacher panel: students on the left, the chosen student's progress and work on the right.
// Uses api, el, ago, STATUS, openViewer and formDialog from teacher-view.js.
(() => {
  const COURSE = JSON.parse(document.getElementById("course").textContent);
  const LESSON = Object.fromEntries(COURSE.lessons.map((L) => [L.n, L]));
  const LEVEL = Object.fromEntries(COURSE.levels.map((l) => [l.id, l]));
  const ONLINE_MS = 5 * 60000;
  const TABS = [["progress", "Progress"], ["homework", "Homework"], ["practice", "Practice"], ["lesson", "Lesson"], ["game", "Game"], ["playground", "Playground"]];
  const list = document.getElementById("students");
  const detail = document.getElementById("detail");
  let students = [];
  let current = null; // { id, username, items, works, game }
  let tab = "progress";
  try { tab = localStorage.getItem("tp-tab") || tab; } catch {}

  function statusOf(code, start) {
    if (!code || !code.trim()) return "empty";
    if (code.trim() === (start || "").trim()) return "started";
    return window.checkHTML && checkHTML(code).length ? "mistakes" : "written";
  }

  // Turns a saved key like code:p2-3 into a labelled piece of work.
  function describe(key, item, passed) {
    let m;
    let w = null;
    if ((m = /^code:([ph])(\d+)-(\d+)$/.exec(key))) {
      const kind = m[1] === "p" ? "practice" : "homework";
      const lesson = Number(m[2]);
      const n = Number(m[3]);
      const task = (LESSON[lesson] || {})[kind]?.[n - 1] || {};
      w = { kind, lesson, n, title: `Lesson ${lesson} · ${kind === "practice" ? "Practice" : "Homework"} task ${n}`,
        task: task.task, start: task.start, stars: passed[`${m[1]}${lesson}-${n}`] || 0 };
    } else if ((m = /^code:t(\d+)-(\d+)$/.exec(key))) {
      const lesson = Number(m[1]);
      const n = Number(m[2]);
      const task = (LESSON[lesson] || {}).lesson?.[n - 1] || {};
      w = { kind: "lesson", lesson, n, title: `Lesson ${lesson} · Your turn ${n}`, task: task.task, start: task.start };
    } else if ((m = /^code:game-(.+)$/.exec(key))) {
      const level = LEVEL[m[1]] || { title: m[1], lesson: 0 };
      w = { kind: "game", lesson: level.lesson, n: COURSE.levels.indexOf(level), level: m[1],
        title: `Game level: ${level.title}`, task: `Block Builder level for lesson ${level.lesson}.`, start: level.start };
    } else if (key === "code:free-1") {
      w = { kind: "playground", lesson: 0, n: 0, title: "Playground", task: "Free building, no task." };
    }
    if (!w) return null;
    return { ...w, key, code: item.v || "", t: item.t, status: w.stars ? "passed" : statusOf(item.v, w.start) };
  }

  const KIND = { lesson: 0, practice: 1, homework: 2, game: 3, playground: 4 };
  const byOrder = (a, b) => a.lesson - b.lesson || KIND[a.kind] - KIND[b.kind] || a.n - b.n;

  async function loadStudents() {
    ({ students } = await api.get("/api/teacher/students"));
    document.getElementById("synced").textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    drawList();
  }

  function drawList() {
    if (!students.length) {
      list.replaceChildren(el("li", "No students yet. Press + Add student.", "tp-empty"));
      return;
    }
    list.replaceChildren(...students.map((s) => {
      const li = el("li");
      const btn = el("button", null, "tp-student" + (current && current.id === s.id ? " on" : ""));
      btn.type = "button";
      const online = s.updated && Date.now() - s.updated * 1000 < ONLINE_MS;
      btn.append(el("span", s.username[0].toUpperCase(), "tp-avatar"));
      const text = el("span", null, "tp-student-text");
      text.append(el("strong", s.username),
        el("small", online ? "Online now" : `Active ${ago(s.updated * 1000)}`, online ? "tp-online" : ""));
      btn.append(text, el("span", `★ ${s.stars || 0}  ◆ ${s.gems || 0}`, "tp-mini"));
      btn.addEventListener("click", () => openStudent(s.id));
      li.append(btn);
      return li;
    }));
  }

  async function openStudent(id, keepScroll = false) {
    const data = await api.get(`/api/teacher/student?id=${id}`);
    let game = {};
    try { game = JSON.parse(data.items.game?.v || "{}") || {}; } catch {}
    const works = Object.entries(data.items).map(([k, item]) => describe(k, item, game.tasks || {})).filter(Boolean).sort(byOrder);
    current = { id, username: data.username, works, game, summary: students.find((s) => s.id === id) || {} };
    try { localStorage.setItem("tp-student", id); } catch {}
    drawList();
    drawDetail();
    if (!keepScroll && innerWidth < 900) detail.scrollIntoView({ behavior: "smooth" });
  }

  function stat(label, value, note) {
    const box = el("div", null, "tp-stat");
    box.append(el("strong", String(value)), el("span", label));
    if (note) box.append(el("small", note));
    return box;
  }

  function drawDetail() {
    const c = current;
    const s = c.summary;
    const online = s.updated && Date.now() - s.updated * 1000 < ONLINE_MS;
    const head = el("div", null, "tp-head");
    const who = el("div", null, "tp-who");
    who.append(el("span", c.username[0].toUpperCase(), "tp-avatar big"));
    const name = el("div");
    name.append(el("h2", c.username), el("p", online ? "● Online now" : `Last active ${ago(s.updated * 1000)}`, online ? "tp-online" : "tp-muted"));
    who.append(name);
    const manage = el("div", null, "tp-manage");
    const pw = el("button", "New password", "tp-btn ghost small");
    pw.type = "button";
    pw.onclick = () => openStudentPw(c.username);
    const del = el("button", "Delete", "tp-btn ghost small danger");
    del.type = "button";
    del.onclick = () => openDelete(c.username);
    const parent = el("button", "Parent link", "tp-btn ghost small");
    parent.type = "button";
    parent.onclick = () => showParentLink(c.username);
    manage.append(parent, pw, del);
    head.append(who, manage);

    const count = (kind, status) => c.works.filter((w) => w.kind === kind && (!status || w.status === status)).length;
    const homeworkLessons = Object.keys(c.game.homework || {}).length;
    const taskStars = Object.values(c.game.tasks || {}).reduce((a, b) => a + b, 0);
    const stats = el("div", null, "tp-stats");
    stats.append(
      stat("Practice passed", count("practice", "passed"), `of ${COURSE.lessons.length * 5} · ${count("practice")} saved`),
      stat("Homework passed", count("homework", "passed"), `all done in ${homeworkLessons} lessons`),
      stat("Task stars", taskStars, `of ${COURSE.lessons.length * 8 * 3}`),
      stat("Game levels", Object.keys(c.game.stars || {}).length, `of ${COURSE.levels.length} · ${s.stars || 0} stars`),
      stat("Diamonds", c.game.gems || 0),
      stat("Best race", c.game.best || 0, "right answers"),
    );

    const tabs = el("div", null, "tp-tabs");
    tabs.setAttribute("role", "tablist");
    TABS.forEach(([key, label]) => {
      const n = key === "progress" ? "" : ` ${c.works.filter((w) => w.kind === key).length}`;
      const b = el("button", label + n, "tp-tab");
      b.type = "button";
      b.setAttribute("role", "tab");
      b.setAttribute("aria-selected", key === tab);
      b.onclick = () => { tab = key; try { localStorage.setItem("tp-tab", key); } catch {} drawDetail(); };
      tabs.append(b);
    });

    detail.replaceChildren(head, stats, tabs, tab === "progress" ? progressGrid() : tab === "game" ? gameTab() : workList(tab));
  }

  function cell(work, label, list) {
    const td = el("td");
    if (!work) {
      td.append(el("span", "", "tp-cell empty"));
      return td;
    }
    const b = el("button", work.stars ? "★".repeat(work.stars) : label, `tp-cell ${work.status}`);
    b.type = "button";
    b.title = `${work.title}: ${STATUS[work.status]}${work.stars ? `, ${work.stars} stars` : ""}`;
    b.onclick = () => openViewer(list, list.indexOf(work));
    td.append(b);
    return td;
  }

  function progressGrid() {
    const tasks = current.works.filter((w) => w.kind === "practice" || w.kind === "homework");
    const find = (kind, lesson, n) => tasks.find((w) => w.kind === kind && w.lesson === lesson && w.n === n);
    const wrap = el("div", null, "tp-grid-wrap");
    const legend = el("p", null, "tp-legend");
    [["passed", "Passed"], ["written", "Written, not passed"], ["mistakes", "Has mistakes"], ["started", "Not changed"], ["empty", "Empty"]]
      .forEach(([k, t]) => legend.append(el("span", t, `tp-key ${k}`)));
    const table = el("table", null, "tp-grid");
    const head = el("tr");
    head.append(el("th", "Lesson"));
    ["P1", "P2", "P3", "P4", "P5"].forEach((t) => head.append(el("th", t)));
    ["H1", "H2", "H3"].forEach((t) => head.append(el("th", t, "hw")));
    const thead = el("thead");
    thead.append(head);
    const body = el("tbody");
    COURSE.lessons.forEach((L) => {
      const tr = el("tr");
      const name = el("th", null, "tp-lesson");
      name.append(el("span", String(L.n), "num"), document.createTextNode(" " + L.title));
      tr.append(name);
      for (let n = 1; n <= 5; n++) tr.append(cell(find("practice", L.n, n), String(n), tasks));
      for (let n = 1; n <= 3; n++) tr.append(cell(find("homework", L.n, n), String(n), tasks));
      body.append(tr);
    });
    table.append(thead, body);
    const scroll = el("div", null, "scroll");
    scroll.append(table);
    wrap.append(legend, scroll);
    return wrap;
  }

  function row(work, list) {
    const b = el("button", null, "tp-row");
    b.type = "button";
    const text = el("span", null, "tp-row-text");
    text.append(el("strong", work.title), el("small", work.task || ""));
    b.append(text, el("span", STATUS[work.status] + (work.stars ? " " + "★".repeat(work.stars) : ""), `tp-chip ${work.status}`), el("span", ago(work.t), "tp-muted"));
    b.onclick = () => openViewer(list, list.indexOf(work));
    return b;
  }

  function workList(kind) {
    const works = current.works.filter((w) => w.kind === kind);
    const box = el("div", null, "tp-rows");
    if (!works.length) {
      box.append(el("p", `No ${kind} saved yet.`, "tp-empty"));
      return box;
    }
    let lesson = null;
    works.forEach((w) => {
      if (kind !== "playground" && w.lesson !== lesson) {
        lesson = w.lesson;
        box.append(el("h3", `Lesson ${lesson}: ${(LESSON[lesson] || {}).title || ""}`));
      }
      box.append(row(w, works));
    });
    return box;
  }

  function gameTab() {
    const box = el("div", null, "tp-rows");
    const g = current.game;
    const owned = (g.cars || []).length;
    box.append(el("p", `Garage: ${owned} car${owned === 1 ? "" : "s"} · driving ${g.car || "red"} · homework diamonds from lessons: ${Object.keys(g.homework || {}).join(", ") || "none yet"}`, "tp-muted"));
    const works = current.works.filter((w) => w.kind === "game");
    COURSE.levels.forEach((level, i) => {
      const stars = (g.stars || {})[level.id] || 0;
      const work = works.find((w) => w.level === level.id);
      const line = el(work ? "button" : "div", null, "tp-row" + (work ? "" : " still"));
      const text = el("span", null, "tp-row-text");
      text.append(el("strong", `${i + 1}. ${level.title}`), el("small", `Lesson ${level.lesson}`));
      line.append(text, el("span", "★".repeat(stars) + "☆".repeat(3 - stars), "tp-stars"),
        el("span", work ? ago(work.t) : "not opened", "tp-muted"));
      if (work) {
        line.type = "button";
        line.onclick = () => openViewer(works, works.indexOf(work));
      }
      box.append(line);
    });
    return box;
  }

  const refresh = async () => {
    await loadStudents();
    if (current && !document.getElementById("viewer").open && !document.querySelector("dialog[open]")) {
      if (students.some((s) => s.id === current.id)) await openStudent(current.id, true);
      else { current = null; detail.replaceChildren(el("p", "Pick a student on the left.", "tp-empty")); }
    }
  };

  const openAdd = formDialog("add", async (f) => {
    const username = f.username.value.trim();
    await api.post("/api/teacher/students", { username, password: f.password.value });
    await loadStudents();
    const added = students.find((s) => s.username.toLowerCase() === username.toLowerCase());
    if (added) await openStudent(added.id);
  });
  const openPw = formDialog("pw", (f) => api.post("/api/teacher/password", { password: f.password.value }));
  const openStudentPw = formDialog("student-pw", (f) => api.post("/api/teacher/password", { id: current.id, password: f.password.value }));
  const openDelete = formDialog("delete", async () => {
    await api.post("/api/teacher/delete", { id: current.id });
    current = null;
    try { localStorage.removeItem("tp-student"); } catch {}
    detail.replaceChildren(el("p", "Pick a student on the left.", "tp-empty"));
    await loadStudents();
  });
  // The parent link: copy it for Telegram. "New link" turns the old one off, so it asks twice.
  const openParent = formDialog("parent", (f) => navigator.clipboard.writeText(f.url.value));
  const parentUrl = document.getElementById("parent-url");
  const parentNew = document.getElementById("parent-new");
  const fillParent = async (fresh) => {
    const { key } = await api.post("/api/teacher/parent-link", { id: current.id, new: fresh });
    parentUrl.value = `${location.origin}/parent?k=${key}`;
  };
  async function showParentLink(name) {
    openParent(name);
    parentNew.textContent = "New link";
    parentUrl.value = "Loading...";
    await fillParent(false);
  }
  parentNew.onclick = async () => {
    if (parentNew.textContent === "New link") {
      parentNew.textContent = "Sure? The old link stops working";
      return;
    }
    await fillParent(true);
    parentNew.textContent = "New link";
  };
  document.getElementById("add-open").onclick = () => openAdd();
  document.getElementById("pw-open").onclick = () => openPw();
  document.getElementById("refresh").onclick = refresh;

  api.get("/api/me").then(async (me) => {
    if (me.role !== "teacher") throw new Error();
    document.getElementById("panel").hidden = false;
    await loadStudents();
    let last = null;
    try { last = Number(localStorage.getItem("tp-student")); } catch {}
    const pick = students.find((s) => s.id === last) || students[0];
    if (pick) await openStudent(pick.id, true);
    setInterval(() => { if (!document.hidden) refresh(); }, 30000);
  }).catch(() => { document.getElementById("gate").hidden = false; });
})();
