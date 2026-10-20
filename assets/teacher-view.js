// Teacher panel windows: the work viewer (task, code, mistakes, his page) and the small forms.
// teacher.js uses api, el, ago, openViewer and formDialog from here.

const api = {
  json: (res) => res.json().catch(() => ({})).then((data) => {
    if (!res.ok) throw new Error(data.error || "Server error. Try again.");
    return data;
  }),
  get: (url) => fetch(url).then(api.json),
  post: (url, body) => fetch(url, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  }).then(api.json),
};

function el(tag, text, cls) {
  const node = document.createElement(tag);
  if (text !== undefined && text !== null) node.textContent = text;
  if (cls) node.className = cls;
  return node;
}

function ago(ms) {
  if (!ms) return "never";
  const mins = Math.round((Date.now() - ms) / 60000);
  if (mins < 2) return "just now";
  if (mins < 60) return `${mins} min ago`;
  if (mins < 48 * 60) return `${Math.round(mins / 60)} h ago`;
  return `${Math.round(mins / 1440)} days ago`;
}

const STATUS = {
  done: "Done", mistakes: "Has mistakes", started: "Not changed yet", empty: "Empty",
};

document.addEventListener("click", (e) => {
  const close = e.target.closest("[data-close]");
  if (close) close.closest("dialog").close();
  const show = e.target.closest(".show-pw");
  if (show) {
    const input = show.previousElementSibling;
    input.type = input.type === "password" ? "text" : "password";
    show.textContent = input.type === "password" ? "Show" : "Hide";
  }
});

// The work viewer. Previous / Next walk through the list it was opened with.
const viewer = document.getElementById("viewer");
let viewList = [];
let viewAt = 0;

function openViewer(list, index) {
  viewList = list;
  viewAt = index;
  drawViewer();
  if (!viewer.open) viewer.showModal();
}

function drawViewer() {
  const w = viewList[viewAt];
  document.getElementById("v-kicker").textContent =
    `${viewAt + 1} of ${viewList.length} · ${STATUS[w.status]} · saved ${ago(w.t)}`;
  document.getElementById("v-title").textContent = w.title;
  document.getElementById("v-task").textContent = w.task || "";
  document.getElementById("v-code").textContent = w.code || "(empty)";
  document.getElementById("v-view").srcdoc = w.code || "";
  const checks = document.getElementById("v-checks");
  const problems = window.checkHTML ? checkHTML(w.code || "") : [];
  if (problems.length) {
    const list = el("ul");
    problems.forEach((p) => list.append(el("li", `Line ${p.line}: ${p.msg}`)));
    checks.className = "checked bad";
    checks.replaceChildren(list);
  } else {
    checks.className = "checked good";
    checks.textContent = w.code && w.code.trim() ? "No mistakes found by the checker." : "Nothing written yet.";
  }
  document.getElementById("v-prev").disabled = viewAt === 0;
  document.getElementById("v-next").disabled = viewAt === viewList.length - 1;
}

const step = (by) => {
  const next = viewAt + by;
  if (next >= 0 && next < viewList.length) { viewAt = next; drawViewer(); }
};
document.getElementById("v-prev").addEventListener("click", () => step(-1));
document.getElementById("v-next").addEventListener("click", () => step(1));
viewer.addEventListener("keydown", (e) => {
  if (e.key === "ArrowLeft") step(-1);
  if (e.key === "ArrowRight") step(1);
});

// A form inside a <dialog>. Returns open(name): the name fills every [data-name] in the title.
function formDialog(name, submit) {
  const dialog = document.getElementById(`${name}-dialog`);
  const form = dialog.querySelector("form");
  const note = form.querySelector(".checked");
  const button = form.querySelector("[type=submit]");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    button.disabled = true;
    note.className = "checked";
    note.textContent = "";
    try {
      await submit(form);
      dialog.close();
    } catch (err) {
      note.className = "checked bad";
      note.textContent = err.message;
    } finally {
      button.disabled = false;
    }
  });
  return (who = "") => {
    form.reset();
    note.textContent = "";
    note.className = "checked";
    form.querySelectorAll("input[type=text]").forEach((i) => { if (i.closest(".pw-row")) i.type = "password"; });
    form.querySelectorAll(".show-pw").forEach((b) => { b.textContent = "Show"; });
    dialog.querySelectorAll("[data-name]").forEach((s) => { s.textContent = who; });
    dialog.showModal();
  };
}
