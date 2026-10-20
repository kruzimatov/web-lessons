// Block Builder: every task he finishes adds rows to a pixel building, live while he types.
// "Build it!" checks the code: all tasks done and no mistakes wins 1 to 3 stars.
(() => {
  const BLOCK = {
    G: "#5dbb3f", D: "#8b5a2b", S: "#9e9e9e", W: "#7a4a22", P: "#d7a85a", L: "#3f8f2f",
    R: "#d84a3a", B: "#8fd8ff", Y: "#f4c430", K: "#2b2b2b", O: "#ff8a1f", C: "#26c6da",
  };
  const ARTS = {
    sign: ["............", ".PPPPPPPPPP.", ".PKKPKPKKKP.", ".PPPPPPPPPP.", ".PKPKKKPKKP.",
      ".PPPPPPPPPP.", ".....WW.....", ".....WW.....", ".....WW.....", "GGGGGGGGGGGG"],
    house: [".....RR.....", "....RRRR....", "...RRRRRR...", "..RRRRRRRR..", ".PPPPPPPPPP.",
      ".PBBPPPPBBP.", ".PBBPWWPBBP.", ".PPPPWWPPPP.", ".SSSSWWSSSS.", "GGGGGGGGGGGG"],
    tree: ["....LLLL....", "...LLLLLL...", "..LLLRLLLL..", "..LLLLLLRL..", "...LLLLLL...",
      ".....WW.....", ".....WW.....", ".....WW.....", "....WWWW....", "GGGGGGGGGGGG"],
    car: ["............", "............", "............", "...RRRRR....", "..RBBRBBR...",
      ".RRRRRRRRRR.", ".RRRRRRRRRRY", ".RKKRRRRKKR.", "..KK....KK..", "SSSSSSSSSSSS"],
    rocket: [".....RR.....", "....RBBR....", "....SBBS....", "....SSSS....", "....SRRS....",
      "....SSSS....", "...RSSSSR...", "..RRSSSSRR..", "....OYYO....", ".....OO....."],
    castle: [".S.S....S.S.", ".SSS....SSS.", ".SSS.CC.SSS.", ".SSSSSSSSSS.", ".SSBSSSSBSS.",
      ".SSSSSSSSSS.", ".SSBSSSSBSS.", ".SSSSKKSSSS.", ".SSSSKKSSSS.", "GGGGGGGGGGGG"],
  };
  const map = document.querySelector("#builder .map");
  const intro = document.querySelector("#builder > .goal");
  const missions = [...document.querySelectorAll(".mission")];

  function drawArt(box, name) {
    const rows = ARTS[name];
    box.style.setProperty("--cols", rows[0].length);
    box.replaceChildren(...rows.flatMap((row, y) => [...row].map((ch, x) => {
      const cell = document.createElement("i");
      cell.dataset.row = rows.length - 1 - y; // 0 is the ground row
      cell.style.transitionDelay = x * 25 + "ms";
      if (ch !== ".") cell.style.background = BLOCK[ch];
      else cell.className = "air";
      return cell;
    })));
  }

  function drawMap() {
    let open = true;
    map.querySelectorAll(".level").forEach((btn) => {
      const got = save.stars[btn.dataset.go] || 0;
      btn.disabled = !open;
      btn.classList.toggle("locked", !open);
      btn.classList.toggle("done", got > 0);
      btn.querySelector(".stars").textContent = open ? starText(got) : "Locked";
      open = got > 0;
    });
  }

  function showMap() {
    missions.forEach((m) => { m.hidden = true; });
    map.hidden = false;
    intro.hidden = false;
    drawMap();
  }

  missions.forEach((m, k) => {
    const id = m.dataset.id;
    const code = m.querySelector("textarea.src");
    const art = m.querySelector(".art");
    const needs = [...m.querySelectorAll(".needs li")];
    const built = m.querySelector(".built");
    const note = m.querySelector(".note");
    const finish = m.querySelector(".finish");
    const next = document.createElement("button");
    let fails = 0;
    let lastDone = 0;
    next.type = "button";
    next.className = "build-btn next";
    next.textContent = k + 1 < missions.length ? "Next level" : "Back to the map";
    next.hidden = true;
    finish.append(next);
    drawArt(art, m.dataset.art);

    const update = () => {
      const src = code.value;
      const doc = new DOMParser().parseFromString(src, "text/html");
      const done = needs.filter((li) => {
        const ok = meetsRule(li, src, doc);
        li.classList.toggle("done", ok);
        return ok;
      }).length;
      const rows = ARTS[m.dataset.art].length;
      const shown = Math.round((rows * done) / needs.length);
      art.querySelectorAll("i").forEach((c) => c.classList.toggle("on", Number(c.dataset.row) < shown));
      built.textContent = `${done} of ${needs.length} built`;
      if (done > lastDone) beep(440 + done * 110);
      lastDone = done;
    };

    let wait = 0;
    const later = () => { clearTimeout(wait); wait = setTimeout(update, 250); };
    let cm = null;
    const start = () => {
      const box = m.querySelector(".play");
      if (box.dataset.ready) return;
      setupPlay(box);
      cm = m.querySelector(".CodeMirror");
      if (cm) cm.CodeMirror.on("change", later); else code.addEventListener("input", later);
    };

    m.open = () => {
      missions.forEach((x) => { x.hidden = x !== m; });
      map.hidden = true;
      intro.hidden = true;
      fails = 0;
      note.textContent = "";
      next.hidden = true;
      start();
      if (cm) cm.CodeMirror.refresh();
      lastDone = needs.length; // no beeps for work he did last time
      update();
      m.scrollIntoView({ block: "start" });
    };

    m.querySelector(".back").addEventListener("click", showMap);
    next.addEventListener("click", () => (missions[k + 1] ? missions[k + 1].open() : showMap()));

    m.querySelector(".build-btn").addEventListener("click", () => {
      update();
      const missing = needs.filter((li) => !li.classList.contains("done"));
      const problems = window.checkHTML ? checkHTML(code.value) : [];
      if (missing.length || problems.length) {
        fails += 1;
        beep(150, 300);
        art.parentElement.classList.remove("shake");
        void art.offsetWidth;
        art.parentElement.classList.add("shake");
        if (problems.length) {
          note.textContent = "There is a bug in your code. Look at the list under the editor!";
          m.querySelector(".check-btn").click();
        } else {
          note.textContent = `Not finished yet: ${missing.length} more to build. Look for the empty boxes.`;
        }
        return;
      }
      const stars = fails === 0 ? 3 : fails <= 2 ? 2 : 1;
      const before = save.stars[id] || 0;
      const gems = Math.max(0, stars - before) * 5;
      save.stars[id] = Math.max(stars, before);
      keep();
      if (gems) addGems(gems); else hud();
      note.textContent = `You built it! ${starText(stars)}` + (gems ? ` +${gems} diamonds!` : "");
      next.hidden = false;
      tune([523, 659, 784, 1047, 1319]);
      confetti();
    });
  });

  map.querySelectorAll(".level").forEach((btn) => {
    btn.addEventListener("click", () => document.getElementById("m-" + btn.dataset.go).open());
  });
  document.addEventListener("game-mode", (e) => { if (e.detail === "builder") showMap(); });
  drawMap();
})();
