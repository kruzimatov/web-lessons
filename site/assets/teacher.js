// Teacher panel: every student's progress and saved code. All data comes from /api/teacher/*.
(() => {
  const panel = document.getElementById("panel");
  const gate = document.getElementById("gate");
  const list = document.getElementById("students");
  const work = document.getElementById("work");
  const json = (res) => res.json().then((data) => { if (!res.ok) throw new Error(data.error); return data; });
  const get = (url) => fetch(url).then(json);
  const post = (url, body) => fetch(url, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  }).then(json);
  const el = (tag, text, cls) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (cls) node.className = cls;
    return node;
  };

  function ago(seconds) {
    if (!seconds) return "never";
    const mins = Math.round((Date.now() / 1000 - seconds) / 60);
    if (mins < 2) return "just now";
    if (mins < 60) return `${mins} min ago`;
    if (mins < 48 * 60) return `${Math.round(mins / 60)} h ago`;
    return `${Math.round(mins / 1440)} days ago`;
  }

  function label(key) {
    let m;
    if ((m = /^code:h(\d+)-(\d+)$/.exec(key))) return [`Homework ${m[1]}`, `Lesson ${m[1]} homework, task ${m[2]}`];
    if ((m = /^code:p(\d+)-(\d+)$/.exec(key))) return [`Practice ${m[1]}`, `Lesson ${m[1]} practice, task ${m[2]}`];
    if ((m = /^code:game-(.+)$/.exec(key))) return ["Game levels", `Level: ${m[1]}`];
    if (key === "code:free-1") return ["Playground", "Playground"];
    return null;
  }

  async function showStudents() {
    const { students } = await get("/api/teacher/students");
    const rows = students.map((s) => {
      const tr = el("tr");
      const cells = [s.username, ago(s.updated), s.levels ?? 0, s.stars ?? 0, s.gems ?? 0, s.best ?? 0,
        s.homework && s.homework.length ? s.homework.join(", ") : "none"];
      cells.forEach((c) => tr.append(el("td", String(c))));
      const actions = el("td", undefined, "actions");
      const view = el("button", "See work");
      view.onclick = () => showWork(s.id, s.username);
      const pass = el("button", "New password");
      pass.onclick = async () => {
        const pw = prompt(`New password for ${s.username} (at least 8 characters):`);
        if (!pw) return;
        try { await post("/api/teacher/password", { id: s.id, password: pw }); alert("Password changed. Give it to the student."); }
        catch (e) { alert(e.message); }
      };
      const del = el("button", "Delete", "danger");
      del.onclick = async () => {
        if (!confirm(`Delete ${s.username} and ALL their saved work? This cannot be undone.`)) return;
        await post("/api/teacher/delete", { id: s.id });
        work.replaceChildren();
        showStudents();
      };
      actions.append(view, pass, del);
      tr.append(actions);
      return tr;
    });
    list.replaceChildren(...(rows.length ? rows : [Object.assign(el("tr"), { innerHTML: '<td colspan="8">No students yet. Add one below.</td>' })]));
  }

  async function showWork(id, name) {
    const { items } = await get(`/api/teacher/student?id=${id}`);
    const groups = {};
    Object.entries(items)
      .filter(([key, item]) => label(key) && item.v && item.v.trim())
      .sort((a, b) => b[1].t - a[1].t)
      .forEach(([key, item]) => {
        const [group, title] = label(key);
        (groups[group] = groups[group] || []).push({ title, code: item.v, t: item.t });
      });
    const parts = [el("h2", `${name}'s work`)];
    if (!Object.keys(groups).length) parts.push(el("p", "Nothing saved yet."));
    for (const [group, entries] of Object.entries(groups)) {
      parts.push(el("h3", group));
      for (const entry of entries) {
        const box = el("details", undefined, "work-item");
        box.append(el("summary", `${entry.title} · ${ago(entry.t / 1000)}`));
        box.addEventListener("toggle", () => {
          if (!box.open || box.querySelector(".panes")) return;
          const panes = el("div", undefined, "panes");
          const view = el("iframe");
          view.title = entry.title;
          view.sandbox = ""; // his page shows, but no scripts run
          view.srcdoc = entry.code;
          const pre = el("pre");
          pre.append(el("code", entry.code));
          panes.append(pre, view);
          box.append(panes);
        });
        parts.push(box);
      }
    }
    work.replaceChildren(...parts);
    work.scrollIntoView({ behavior: "smooth" });
  }

  function form(id, send, done) {
    const f = document.getElementById(id);
    const note = f.querySelector(".checked");
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        await send(f);
        note.className = "checked good";
        note.textContent = done(f);
        f.reset();
        showStudents();
      } catch (err) {
        note.className = "checked bad";
        note.textContent = err.message;
      }
    });
  }

  document.querySelectorAll(".show-pw").forEach((btn) => btn.addEventListener("click", () => {
    const input = btn.previousElementSibling;
    input.type = input.type === "password" ? "text" : "password";
    btn.textContent = input.type === "password" ? "Show" : "Hide";
  }));

  form("add-form", (f) => post("/api/teacher/students", { username: f.username.value.trim(), password: f.password.value }),
    (f) => `Added ${f.username.value.trim()}. Give them the username and password to log in once on each device.`);
  form("pw-form", (f) => post("/api/teacher/password", { password: f.password.value }),
    () => "Your password is changed. Other devices are logged out.");

  get("/api/me").then((me) => {
    if (me.role !== "teacher") throw new Error();
    gate.hidden = true;
    panel.hidden = false;
    showStudents();
    setInterval(() => { if (!document.hidden) showStudents(); }, 30000);
  }).catch(() => { gate.hidden = false; });
})();
