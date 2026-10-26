// Parent page: one student's progress from the secret link (?k=...), in English and Uzbek. Read only, no login.
(() => {
  const COURSE = JSON.parse(document.getElementById("course").textContent);
  const PASS = COURSE.pass;
  const ALL = COURSE.lessons.length;
  const TASKS = [
    ["p", 1, "Easy", "Oson"], ["p", 2, "Medium", "O'rtacha"], ["p", 3, "Find the bug", "Xatoni top"],
    ["p", 4, "Medium", "O'rtacha"], ["p", 5, "Mini project", "Kichik loyiha"],
    ["h", 1, "Task 1", "1-vazifa"], ["h", 2, "Task 2", "2-vazifa"], ["h", 3, "Your idea", "O'z g'oyasi"],
  ];
  const GIFT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20 7h-2.2A3 3 0 0 0 12 3.8 3 3 0 0 0 6.2 7H4a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h1v8a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-8h1a1 1 0 0 0 1-1V8a1 1 0 0 0-1-1Zm-6-2a1 1 0 1 1 0 2h-1V6a1 1 0 0 1 1-1ZM9 6a1 1 0 0 1 2 0v1h-1a1 1 0 0 1-1-1ZM5 9h6v1H5Zm2 3h4v7H7Zm10 7h-4v-7h4Zm2-9h-6V9h6Z"/></svg>';
  const root = document.getElementById("pp");
  const key = new URLSearchParams(location.search).get("k") || "";

  function el(tag, cls, ...kids) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    node.append(...kids.filter((k) => k !== null && k !== undefined)); // strings become text, never HTML
    return node;
  }
  function two(en, uz, cls = "") {
    const u = el("span", "uz", uz);
    u.lang = "uz";
    return el("span", `two ${cls}`, el("span", "en", en), u);
  }
  function gift(cls) {
    const box = el("span", cls);
    box.innerHTML = GIFT; // fixed markup, no student data
    return box;
  }
  function bar(part, whole, mark) {
    const box = el("div", "pp-bar", el("i"));
    box.firstChild.style.width = `${Math.min(100, Math.round((100 * part) / whole))}%`;
    if (mark) {
      const line = el("b");
      line.style.left = `${(100 * mark) / whole}%`;
      box.append(line);
    }
    box.setAttribute("role", "progressbar");
    box.setAttribute("aria-valuemin", "0");
    box.setAttribute("aria-valuemax", String(whole));
    box.setAttribute("aria-valuenow", String(part));
    return box;
  }
  const starText = (n) => "★".repeat(n) + "☆".repeat(3 - n);

  function lessonsOf(tasks, items) {
    return COURSE.lessons.map((L) => {
      const list = TASKS.map(([kind, n, en, uz]) => {
        const id = `${kind}${L.n}-${n}`;
        return { id, kind, en, uz, n, stars: tasks[id] || 0, code: (items[`code:${id}`] || {}).v || "" };
      });
      const done = list.filter((t) => t.stars).length;
      const stars = list.reduce((a, t) => a + t.stars, 0);
      const passed = done >= PASS.tasks && stars >= PASS.stars;
      const state = passed ? "passed" : done || list.some((t) => t.code.trim()) ? "doing" : "todo";
      return { ...L, list, done, stars, state };
    });
  }

  const STATE = { passed: ["Passed", "O'tdi"], doing: ["In progress", "Jarayonda"], todo: ["Not started", "Boshlanmagan"] };

  function hero(data, game) {
    const name = data.username.charAt(0).toUpperCase() + data.username.slice(1);
    const seen = data.updated ? data.updated * 1000 : 0;
    const online = seen && Date.now() - seen < 5 * 60000;
    const when = seen ? new Date(seen).toLocaleString([], { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }) : "-";
    return el("header", "pp-hero",
      el("span", "pp-avatar", name.charAt(0)),
      el("div", "pp-who",
        two("Web course progress", "Veb kurs natijalari", "pp-kicker"),
        el("h1", null, name),
        online ? two("Online now", "Hozir saytda", "pp-online")
          : el("p", "pp-seen", two(`Last active ${when}`, `Oxirgi faollik ${when}`))),
      el("div", "pp-level", el("strong", null, String(game.level || 1)), two("Level", "Daraja")));
  }

  function stat(value, of, en, uz, cls, note) {
    return el("div", `pp-stat ${cls}`, el("strong", null, String(value), of ? el("small", null, ` / ${of}`) : null), two(en, uz),
      note ? two(...note, "pp-stat-note") : null);
  }

  function giftCard(passed, stars) {
    const won = passed === ALL && stars >= PASS.gift;
    const left = [];
    if (stars < PASS.gift) left.push([`${PASS.gift - stars} more stars`, `yana ${PASS.gift - stars} ta yulduz`]);
    if (passed < ALL) left.push([`${ALL - passed} more lessons`, `yana ${ALL - passed} ta dars`]);
    return el("section", `pp-gift${won ? " won" : ""}`,
      gift("pp-gift-icon"),
      el("div", "pp-gift-text",
        el("h2", null, two(won ? "Gift unlocked!" : "Gift goal", won ? "Sovg'a ochildi!" : "Sovg'a maqsadi")),
        el("p", null, two(`Pass all ${ALL} lessons and collect ${PASS.gift} stars (tasks and game).`,
          `${ALL} ta darsning hammasidan o'tib, ${PASS.gift} ta yulduz (vazifa va o'yin) to'plasa, sovg'a ochiladi.`)),
        el("div", "pp-meter", el("span", "pp-meter-label", two("Stars: tasks + game", "Yulduzlar: vazifa + o'yin"), el("b", null, `★ ${stars} / ${PASS.gift}`)), bar(stars, PASS.gift)),
        el("div", "pp-meter", el("span", "pp-meter-label", two("Lessons passed", "O'tilgan darslar"), el("b", null, `${passed} / ${ALL}`)), bar(passed, ALL)),
        won ? null : el("p", "pp-left", two(`Still to go: ${left.map((l) => l[0]).join(" and ")}.`, `Qoldi: ${left.map((l) => l[1]).join(" va ")}.`))));
  }

  function road(lessons, now) {
    const list = el("ol", "pp-road");
    list.setAttribute("aria-label", "Lessons");
    lessons.forEach((L) => {
      const a = el("a", `pp-stop ${L.state}${L.n === now ? " now" : ""}`, L.state === "passed" ? "✓" : String(L.n));
      a.href = `#lesson-${L.n}`;
      a.title = `Lesson ${L.n}: ${L.title} (${STATE[L.state][0]})`;
      a.onclick = () => { document.getElementById(`lesson-${L.n}`).open = true; };
      list.append(el("li", null, a));
    });
    list.append(el("li", null, gift(`pp-stop gift${lessons.every((L) => L.state === "passed") ? " passed" : ""}`)));
    return list;
  }

  // Every task of every lesson in one table, like the teacher's grid. A cell opens his page.
  function grid(lessons, now) {
    const head = el("tr", null, el("th", "pp-grid-lesson", two("Lesson", "Dars")),
      ...TASKS.map(([kind, n]) => el("th", kind === "h" ? "hw" : null, `${kind === "p" ? "P" : "H"}${n}`)),
      el("th", "pp-grid-sum", "★"));
    const rows = lessons.map((L) => el("tr", `${L.state}${L.n === now ? " now" : ""}`,
      el("th", "pp-grid-lesson", el("span", "pp-grid-num", L.state === "passed" ? "✓" : String(L.n)), el("span", "pp-grid-title", `${L.n}. ${L.title}`)),
      ...L.list.map((t) => {
        const label = t.stars ? String(t.stars) : "·";
        const cell = t.code.trim() ? el("button", `pp-cell s${t.stars}`, label) : el("span", `pp-cell s${t.stars}`, label);
        cell.title = `Lesson ${L.n} · ${t.en}: ${t.stars ? `${t.stars} stars` : "not done yet"}`;
        if (cell.tagName === "BUTTON") {
          cell.type = "button";
          cell.onclick = () => show(`Lesson ${L.n} · ${t.kind === "p" ? "Practice" : "Homework"} ${t.n}: ${t.en}`, t.code);
        }
        return el("td", t.kind === "h" ? "hw" : null, cell);
      }),
      el("td", "pp-grid-sum", el("b", null, String(L.stars)))));
    const legend = el("p", "pp-legend",
      el("span", "pp-cell s3", "3"), two("stars, within 3 misses", "yulduz, 3 xatogacha"),
      el("span", "pp-cell s2", "2"), two("stars, more misses", "yulduz, ko'proq xato"),
      el("span", "pp-cell s0", "·"), two("not done", "bajarilmagan"));
    return el("div", null, legend, el("div", "pp-grid-scroll",
      el("table", "pp-grid", el("thead", null, head), el("tbody", null, ...rows))));
  }

  function taskRow(t, L) {
    const row = el("li", `pp-task${t.stars ? " done" : ""}`,
      el("span", "pp-tick", t.stars ? "✓" : ""),
      two(t.en, t.uz, "pp-task-name"),
      t.stars ? el("span", "pp-stars", starText(t.stars)) : two("Not done yet", "Hali bajarilmagan", "pp-muted"));
    if (t.code.trim()) {
      const b = el("button", "pp-btn small", two("See his page", "Sahifasini ko'rish"));
      b.type = "button";
      b.onclick = () => show(`Lesson ${L.n} · ${t.kind === "p" ? "Practice" : "Homework"} ${t.n}: ${t.en}`, t.code);
      row.append(b);
    }
    return row;
  }

  function lessonCard(L, now, open) {
    const card = el("details", `pp-lesson ${L.state}${L.n === now ? " now" : ""}`);
    card.id = `lesson-${L.n}`;
    card.open = open.has(card.id) || (!open.size && L.n === now);
    const group = (kind, en, uz) => el("div", "pp-group", el("h3", null, two(en, uz)),
      el("ul", null, ...L.list.filter((t) => t.kind === kind).map((t) => taskRow(t, L))));
    card.append(
      el("summary", null,
        el("span", "pp-num", L.state === "passed" ? "✓" : String(L.n)),
        el("span", "pp-lesson-text", el("strong", null, `${L.n}. ${L.title}`),
          L.n === now ? two("Now", "Hozir", "pp-now") : two(...STATE[L.state], `pp-state ${L.state}`)),
        el("span", "pp-lesson-score", el("b", null, `★ ${L.stars} / 24`), bar(L.stars, 24, PASS.stars))),
      el("div", "pp-lesson-body",
        el("p", "pp-rule", two(`To pass: ${PASS.tasks} of 8 tasks and ${PASS.stars} stars. Now: ${L.done} tasks, ${L.stars} stars.`,
          `O'tish uchun: 8 tadan ${PASS.tasks} ta vazifa va ${PASS.stars} ta yulduz. Hozir: ${L.done} ta vazifa, ${L.stars} ta yulduz.`)),
        group("p", "Practice in class", "Darsdagi mashq"), group("h", "Homework", "Uy vazifasi")));
    return card;
  }

  function draw(data) {
    let game = {};
    try { game = JSON.parse((data.items.game || {}).v || "{}") || {}; } catch {}
    const lessons = lessonsOf(game.tasks || {}, data.items);
    const passed = lessons.filter((L) => L.state === "passed").length;
    const taskStars = lessons.reduce((a, L) => a + L.stars, 0);
    const gameStars = Object.values(game.stars || {}).reduce((a, b) => a + b, 0);
    const stars = taskStars + gameStars; // the same total as the star chip on his own pages
    const now = (lessons.find((L) => L.state !== "passed") || {}).n;
    const open = new Set([...root.querySelectorAll("details[open]")].map((d) => d.id));
    const badges = game.badges || [];
    document.title = `${data.username}: Progress`;
    root.replaceChildren(
      hero(data, game),
      el("div", "pp-stats",
        stat(passed, ALL, "Lessons passed", "O'tilgan darslar", "green"),
        stat(stars, lessons.length * 24 + COURSE.levels * 3, "Stars", "Yulduzlar", "gold",
          [`${taskStars} from tasks · ${gameStars} from game`, `${taskStars} vazifadan · ${gameStars} o'yindan`]),
        stat(game.gems || 0, null, "Diamonds", "Olmoslar", "blue"),
        stat(Object.keys(game.stars || {}).length, COURSE.levels, "Game levels", "O'yin bosqichlari", "orange")),
      giftCard(passed, stars),
      el("h2", "pp-h", two("The road to the gift", "Sovg'a sari yo'l")),
      road(lessons, now),
      el("h2", "pp-h", two("At a glance", "Bir qarashda")),
      el("p", "pp-hint", two("P = practice in class, H = homework. Numbers are stars.", "P = darsdagi mashq, H = uy vazifasi. Raqamlar yulduzlar soni.")),
      grid(lessons, now),
      el("h2", "pp-h", two("Lessons", "Darslar")),
      el("p", "pp-hint", two("Tap a lesson to see every task.", "Har bir vazifani ko'rish uchun darsni bosing.")),
      el("div", "pp-lessons", ...lessons.map((L) => lessonCard(L, now, open))),
      el("section", "pp-info",
        el("h2", null, two("How stars work", "Yulduzlar qanday beriladi")),
        el("ul", null,
          el("li", null, el("b", null, "★★★ "), two("Done with 3 or fewer wrong checks.", "3 tagacha xato tekshiruv bilan bajarildi.")),
          el("li", null, el("b", null, "★★☆ "), two("Done after more wrong checks.", "Ko'proq xato tekshiruvdan keyin bajarildi.")),
          el("li", null, el("b", null, "★☆☆ "), two("Older tasks from the first rules. Check again to get more.", "Eski qoida bo'yicha. Qayta tekshirsa, ko'proq oladi.")))),
      badges.length ? el("section", "pp-info",
        el("h2", null, two(`Badges: ${badges.length}`, `Nishonlar: ${badges.length}`)),
        el("ul", "pp-badges", ...badges.map((b) => el("li", null, b)))) : null,
      el("p", "pp-foot", two("This page updates by itself every minute.", "Bu sahifa har daqiqada o'zi yangilanadi.")));
  }

  const view = document.getElementById("pp-view");
  function show(title, code) {
    document.getElementById("pp-view-title").textContent = title;
    view.showModal();
    const frame = document.getElementById("pp-frame");
    const fresh = frame.cloneNode(false); // a new frame each time, filled once the window is open
    fresh.srcdoc = code; // sandbox="" : his page runs no scripts
    frame.replaceWith(fresh);
  }
  document.getElementById("pp-close").onclick = () => view.close();

  async function load() {
    const res = await fetch(`/api/parent?k=${encodeURIComponent(key)}`);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || "Server error");
    draw(data);
  }
  function fail() {
    root.replaceChildren(el("div", "pp-error", el("h1", null, two("This link does not work", "Bu havola ishlamayapti")),
      el("p", null, two("Ask the teacher for a new link.", "O'qituvchidan yangi havola so'rang."))));
  }
  load().then(() => {
    setInterval(() => { if (!document.hidden && !view.open) load().catch(() => {}); }, 60000);
  }).catch(fail);
})();
