// Game Zone: one save for all games, sound, diamonds, the mode buttons and the Garage.
// builder.js and racer.js use save, keep, beep, tune, addGems, confetti and CARS from here.

const save = (() => {
  let old = {};
  try { old = JSON.parse(store.get("game")) || {}; } catch {}
  return { gems: 0, stars: {}, best: 0, cars: ["red"], car: "red", sound: true, upto: 0, ...old };
})();
const keep = () => store.set("game", JSON.stringify(save));

const CARS = [
  { id: "red", name: "Red Racer", color: "#e53935", price: 0 },
  { id: "blue", name: "Blue Bolt", color: "#1e88e5", price: 10 },
  { id: "green", name: "Green Gecko", color: "#43a047", price: 20 },
  { id: "gold", name: "Gold Rush", color: "#f4b400", price: 40 },
  { id: "night", name: "Night Rider", color: "#37474f", price: 60 },
  { id: "pink", name: "Pink Flash", color: "#ec407a", price: 80 },
  { id: "diamond", name: "Diamond Car", color: "#26c6da", price: 120 },
];
const carColor = () => (CARS.find((c) => c.id === save.car) || CARS[0]).color;

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

function hud() {
  document.getElementById("gems").textContent = save.gems;
  document.getElementById("star-total").textContent = Object.values(save.stars).reduce((a, b) => a + b, 0);
  const sound = document.getElementById("sound");
  sound.textContent = "Sound: " + (save.sound ? "on" : "off");
  sound.setAttribute("aria-pressed", save.sound);
}

function addGems(n) {
  save.gems += n;
  keep();
  hud();
}

function confetti() {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const box = document.querySelector(".confetti");
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

// A small pixel car, the same one he drives in Tag Racer.
function carSVG(color) {
  return `<svg viewBox="0 0 12 16" width="48" height="64" shape-rendering="crispEdges" aria-hidden="true">
<rect x="2" y="1" width="8" height="14" fill="${color}"/><rect x="3" y="3" width="6" height="3" fill="#bfe9ff"/>
<rect x="3" y="11" width="6" height="2" fill="#bfe9ff"/><rect x="0" y="2" width="2" height="4" fill="#222"/>
<rect x="10" y="2" width="2" height="4" fill="#222"/><rect x="0" y="10" width="2" height="4" fill="#222"/>
<rect x="10" y="10" width="2" height="4" fill="#222"/><rect x="5" y="7" width="2" height="3" fill="#fff"/></svg>`;
}

function garage() {
  const cards = CARS.map((car) => {
    const owned = save.cars.includes(car.id);
    const card = document.createElement("div");
    card.className = "car-card" + (save.car === car.id ? " on" : "");
    card.innerHTML = carSVG(car.color) + "<strong></strong><span></span><button type=\"button\"></button>";
    card.querySelector("strong").textContent = car.name;
    card.querySelector("span").textContent = owned ? "Yours!" : `${car.price} diamonds`;
    const btn = card.querySelector("button");
    if (save.car === car.id) {
      btn.textContent = "Driving now";
      btn.disabled = true;
    } else if (owned) {
      btn.textContent = "Drive it";
      btn.onclick = () => { save.car = car.id; keep(); beep(660); garage(); };
    } else {
      btn.textContent = save.gems >= car.price ? "Buy it" : `Need ${car.price - save.gems} more`;
      btn.disabled = save.gems < car.price;
      btn.onclick = () => {
        save.gems -= car.price;
        save.cars.push(car.id);
        save.car = car.id;
        keep();
        hud();
        tune([523, 659, 784, 1047]);
        confetti();
        garage();
      };
    }
    return card;
  });
  document.getElementById("cars").replaceChildren(...cards);
}

function showMode(name) {
  document.querySelectorAll(".modes button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.mode === name));
  document.querySelectorAll(".mode").forEach((s) => { s.hidden = s.id !== name; });
  store.set("game-mode", name);
  if (name === "garage") garage();
  document.dispatchEvent(new CustomEvent("game-mode", { detail: name }));
}

document.querySelectorAll(".modes button").forEach((b) => b.addEventListener("click", () => showMode(b.dataset.mode)));
document.getElementById("sound").addEventListener("click", () => {
  save.sound = !save.sound;
  keep();
  hud();
  beep(880);
});
hud();
addEventListener("load", () => showMode(store.get("game-mode") || "builder"));
