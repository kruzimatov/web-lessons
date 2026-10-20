// Tag Racer: a question at the top, 3 road signs come down, he drives into the right one.
// Right: +1 diamond and the car speeds up. Wrong: lose a heart and see the right answer.
(() => {
  const canvas = document.getElementById("road");
  const ctx = canvas.getContext("2d");
  const W = 420, H = 560, LANES = [100, 210, 320], CAR_Y = 460, SIGN_W = 104, SIGN_H = 50;
  const ROAD_L = 44, ROAD_R = 376;
  const ALL = JSON.parse(document.getElementById("questions").textContent);
  const question = document.getElementById("question");
  const overlay = document.getElementById("overlay");
  const overText = document.getElementById("over-text");
  const goBtn = document.getElementById("go");
  const upto = document.getElementById("upto");
  const scoreEl = document.getElementById("score");
  const bestEl = document.getElementById("best");
  const heartsEl = document.getElementById("hearts");
  const ratio = window.devicePixelRatio || 1;
  canvas.width = W * ratio;
  canvas.height = H * ratio;
  ctx.scale(ratio, ratio);

  let game = null;
  let bag = [];
  let last = 0;

  if (save.upto && [...upto.options].some((o) => o.value === String(save.upto))) upto.value = save.upto;
  upto.addEventListener("change", () => { save.upto = Number(upto.value); keep(); bag = []; });

  const shuffle = (list) => {
    for (let i = list.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [list[i], list[j]] = [list[j], list[i]];
    }
    return list;
  };

  // Every question once before any repeats.
  function nextQuestion() {
    if (!bag.length) bag = shuffle(ALL.filter((q) => q[0] <= Number(upto.value)));
    const [, text, right, ...wrong] = bag.pop();
    game.q = { text, right, signs: shuffle([right, ...wrong]), y: -SIGN_H, hit: -1 };
    question.textContent = text;
    question.className = "question";
  }

  function stats() {
    scoreEl.textContent = game ? game.score : 0;
    bestEl.textContent = save.best;
    heartsEl.textContent = "♥".repeat(game ? game.hearts : 3);
  }

  function start() {
    game = { lane: 1, x: LANES[1], speed: 70, score: 0, hearts: 3, scroll: 0, pause: 0, shake: 0, flash: null };
    overlay.hidden = true;
    nextQuestion();
    stats();
    last = performance.now();
    requestAnimationFrame(frame);
  }

  function stop(text, paused = false) {
    overlay.hidden = false;
    overText.textContent = text;
    goBtn.textContent = paused ? "Keep driving" : "Drive again";
    if (game) Object.assign(game, { over: true, paused });
  }

  function resume() {
    Object.assign(game, { over: false, paused: false });
    overlay.hidden = true;
    last = performance.now();
    requestAnimationFrame(frame);
  }

  function judge() {
    const q = game.q;
    q.hit = game.lane;
    if (q.signs[game.lane] === q.right) {
      game.score += 1;
      game.speed = Math.min(180, game.speed + 6);
      game.flash = "rgba(93,187,63,0.35)";
      game.pause = 0.7;
      addGems(1);
      tune([660, 990]);
      question.textContent = "Yes! +1 diamond";
      question.className = "question good";
    } else {
      game.hearts -= 1;
      game.shake = 0.4;
      game.flash = "rgba(216,74,58,0.4)";
      game.pause = 2;
      beep(120, 400);
      question.textContent = `Oops! The right answer is ${q.right}`;
      question.className = "question bad";
    }
    if (game.score > save.best) { save.best = game.score; keep(); }
    stats();
  }

  function frame(now) {
    if (!game || game.over) return;
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    game.scroll += game.speed * dt;
    game.x += (LANES[game.lane] - game.x) * Math.min(1, dt * 14);
    game.shake = Math.max(0, game.shake - dt);
    game.q.y += game.speed * dt;
    if (game.q.hit < 0 && game.q.y + SIGN_H >= CAR_Y - 34) judge();
    if (game.q.hit >= 0) {
      game.pause -= dt;
      if (game.pause <= 0) {
        game.flash = null;
        if (game.hearts <= 0) {
          draw();
          stop(`Game over! You got ${game.score} right. Best: ${save.best}.`);
          question.textContent = "Press Drive again to play!";
          return;
        }
        nextQuestion();
      }
    }
    draw();
    requestAnimationFrame(frame);
  }

  function block(x, y, w, h, color) {
    ctx.fillStyle = color;
    ctx.fillRect(Math.round(x), Math.round(y), w, h);
  }

  function tree(x, y) {
    block(x + 12, y + 30, 12, 20, "#7a4a22");
    block(x, y, 36, 32, "#3f8f2f");
    block(x + 6, y + 6, 10, 10, "#4fa83b");
  }

  function car(x, y, color) {
    block(x - 24, y - 26, 10, 18, "#222");
    block(x + 14, y - 26, 10, 18, "#222");
    block(x - 24, y + 10, 10, 18, "#222");
    block(x + 14, y + 10, 10, 18, "#222");
    block(x - 18, y - 32, 36, 64, color);
    block(x - 12, y - 22, 24, 12, "#bfe9ff");
    block(x - 12, y + 14, 24, 8, "#bfe9ff");
    block(x - 3, y - 6, 6, 14, "#fff");
  }

  function sign(x, y, text, fill) {
    block(x - SIGN_W / 2 - 4, y - 4, SIGN_W + 8, SIGN_H + 8, "#2b2b2b");
    block(x - SIGN_W / 2, y, SIGN_W, SIGN_H, fill);
    let size = 20;
    do ctx.font = `bold ${size}px Menlo, Consolas, monospace`;
    while (ctx.measureText(text).width > SIGN_W - 10 && --size > 9);
    ctx.fillStyle = "#1f2a37";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(text, x, y + SIGN_H / 2 + 1);
  }

  function draw() {
    const g = game || { x: LANES[1], scroll: 0, shake: 0 };
    ctx.save();
    if (g.shake) ctx.translate((Math.random() - 0.5) * 12, (Math.random() - 0.5) * 6);
    block(-10, -10, W + 20, H + 20, "#5dbb3f");
    const step = 40, off = g.scroll % step;
    for (let y = -step; y < H + step; y += step) {
      block(0, y + off, ROAD_L, step / 2, "#4fa83b");
      block(ROAD_R, y + off + step / 2, W - ROAD_R, step / 2, "#4fa83b");
    }
    block(ROAD_L, -10, ROAD_R - ROAD_L, H + 20, "#55595e");
    block(ROAD_L, -10, 6, H + 20, "#f4f4f4");
    block(ROAD_R - 6, -10, 6, H + 20, "#f4f4f4");
    for (const lx of [152, 262]) {
      for (let y = -60; y < H + 60; y += 60) block(lx, y + (g.scroll % 60), 6, 30, "#f4f4f4");
    }
    const treeOff = g.scroll % 140;
    for (let y = -140; y < H + 140; y += 140) {
      tree(2, y + treeOff);
      tree(W - 38, y + treeOff + 70);
    }
    if (g.q) {
      g.q.signs.forEach((text, i) => {
        let fill = "#fffdf7";
        if (g.q.hit >= 0 && text === g.q.right) fill = "#9be37e";
        else if (g.q.hit === i) fill = "#ff9b8f";
        sign(LANES[i], g.q.y, text, fill);
      });
    }
    car(g.x, CAR_Y, carColor());
    if (g.flash) block(-10, -10, W + 20, H + 20, g.flash);
    ctx.restore();
  }

  function steer(dir) {
    if (!game || game.over) return;
    const lane = Math.max(0, Math.min(2, game.lane + dir));
    if (lane !== game.lane && game.q.hit < 0) { game.lane = lane; beep(330, 40); }
  }

  goBtn.addEventListener("click", () => (game && game.paused ? resume() : start()));
  document.getElementById("left").addEventListener("pointerdown", () => steer(-1));
  document.getElementById("right").addEventListener("pointerdown", () => steer(1));
  canvas.addEventListener("pointerdown", (e) => {
    const box = canvas.getBoundingClientRect();
    steer((e.clientX - box.left) / box.width * W < game?.x ? -1 : 1);
  });
  addEventListener("keydown", (e) => {
    if (document.getElementById("racer").hidden || !game || game.over) return;
    const dir = { ArrowLeft: -1, a: -1, A: -1, ArrowRight: 1, d: 1, D: 1 }[e.key];
    if (dir) { e.preventDefault(); steer(dir); }
  });
  document.addEventListener("game-mode", (e) => {
    if (e.detail !== "racer" && game && !game.over) stop("Paused. Ready to drive?", true);
    if (e.detail === "racer") draw();
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden && game && !game.over) stop("Paused. Ready to drive?", true);
  });
  stats();
  draw();
})();
