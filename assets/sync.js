// Saves a logged-in student's work on the server, so it is safe on every device.
// It wraps store.set/store.drop from kit.js, so every save on every page is sent.
// Not logged in (or offline): the site works exactly as before, in this browser only.
(() => {
  const SYNCED = /^(code:[\w-]{1,40}|game|last)$/;
  const raw = { set: store.set, drop: store.drop };
  let times = {};
  try { times = JSON.parse(store.get("sync-times")) || {}; } catch {}
  let pending = new Set();
  let on = false;
  let wait = 0;

  const remember = () => raw.set("sync-times", JSON.stringify(times));
  const later = (ms) => { clearTimeout(wait); wait = setTimeout(push, ms); };
  const mark = (key) => {
    if (!SYNCED.test(key)) return;
    times[key] = Date.now();
    remember();
    pending.add(key);
    if (on) later(1500);
  };
  store.set = (key, value) => { raw.set(key, value); mark(key); };
  store.drop = (key) => { raw.drop(key); mark(key); };

  const payload = (keys) => JSON.stringify({
    items: Object.fromEntries(keys.map((k) => [k, { v: store.get(k), t: times[k] || Date.now() }])),
  });
  const post = (url, body) => fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body });

  async function push() {
    if (!on || !pending.size) return;
    const keys = [...pending];
    pending = new Set();
    try {
      const res = await post("/api/sync", payload(keys));
      if (!res.ok) throw new Error(res.status);
      status("Saved");
    } catch {
      keys.forEach((k) => pending.add(k));
      status("Not saved yet. Check the internet");
      later(10000);
    }
  }
  addEventListener("pagehide", () => {
    if (on && pending.size) navigator.sendBeacon("/api/sync", new Blob([payload([...pending])], { type: "application/json" }));
  });

  let badge = null;
  function status(text) { if (badge) badge.querySelector("span").textContent = text; }

  function account(me) {
    const nav = document.querySelector("nav.top");
    if (!nav) return;
    badge = document.createElement("span");
    badge.className = "account";
    if (!me) {
      badge.innerHTML = '<a href="/login.html">Log in</a>';
    } else {
      badge.innerHTML = "<strong></strong> <span></span> <button type=\"button\">Log out</button>";
      badge.querySelector("strong").textContent = me.username;
      status(me.role === "teacher" ? "Teacher" : "Saved");
      if (me.role === "teacher") badge.querySelector("span").innerHTML = '<a href="/teacher.html">Teacher panel</a>';
      badge.querySelector("button").addEventListener("click", async () => {
        await push();
        await post("/api/logout", "{}").catch(() => {});
        location.href = "/login.html";
      });
    }
    nav.append(badge);
  }

  const localKeys = () => {
    try { return Object.keys(localStorage).filter((k) => SYNCED.test(k)); } catch { return []; }
  };

  async function start() {
    let me;
    try {
      const res = await fetch("/api/me");
      if (res.status === 401) return account(null);
      if (!res.ok) return;
      me = await res.json();
    } catch { return; } // opened as a file, or offline
    account(me);
    if (me.role !== "student") return;
    on = true;
    const firstTime = store.get("sync-who") !== String(me.id); // new device: the server copy wins
    let changed = false;
    for (const [key, item] of Object.entries(me.items)) {
      if (!SYNCED.test(key) || !(firstTime || item.t > (times[key] || 0))) continue;
      if (store.get(key) !== item.v) {
        if (item.v === null) raw.drop(key); else raw.set(key, item.v);
        changed = true;
      }
      times[key] = item.t;
    }
    for (const key of localKeys()) {
      const server = me.items[key];
      if (!server || (times[key] || 0) > server.t) { times[key] = times[key] || Date.now(); pending.add(key); }
    }
    remember();
    raw.set("sync-who", String(me.id));
    await push();
    if (changed) location.reload(); // his newer work from another device: show it
  }

  // The login page.
  const form = document.getElementById("login-form");
  if (form) {
    const note = document.getElementById("login-note");
    const pw = form.querySelector("#password");
    form.querySelector(".show-pw").addEventListener("click", (e) => {
      pw.type = pw.type === "password" ? "text" : "password";
      e.target.textContent = pw.type === "password" ? "Show" : "Hide";
    });
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      note.className = "checked";
      note.textContent = "Logging in...";
      try {
        const res = await post("/api/login", JSON.stringify({ username: form.username.value.trim(), password: pw.value }));
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);
        location.href = data.role === "teacher" ? "/teacher.html" : "/index.html";
      } catch (err) {
        note.className = "checked bad";
        note.textContent = err.message === "Failed to fetch" ? "No internet. Try again." : err.message;
      }
    });
  }

  start();
})();
