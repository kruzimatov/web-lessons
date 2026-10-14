// Plays one animation in headless Chrome and saves frames as PNGs.
// Usage: node gif.mjs <page.html> <out_dir> <seconds>
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const [page, outDir, seconds] = process.argv.slice(2);
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const port = 9200 + Math.floor(Math.random() * 500);
const chrome = spawn(CHROME, [
  "--headless=new", "--hide-scrollbars", `--remote-debugging-port=${port}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "gif-"))}`, "about:blank",
]);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

try {
  let list;
  for (let i = 0; i < 40 && !list; i++) {
    await sleep(250);
    list = await fetch(`http://127.0.0.1:${port}/json`).then((r) => r.json()).catch(() => null);
  }
  const tab = list.find((t) => t.type === "page");
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r));
  let id = 0;
  const send = (method, params = {}) => new Promise((resolve) => {
    const my = ++id;
    const on = (e) => {
      const m = JSON.parse(e.data);
      if (m.id === my) { ws.removeEventListener("message", on); resolve(m.result); }
    };
    ws.addEventListener("message", on);
    ws.send(JSON.stringify({ id: my, method, params }));
  });

  await send("Emulation.setDeviceMetricsOverride", { width: 720, height: 260, deviceScaleFactor: 1.5, mobile: false });
  await send("Page.navigate", { url: pathToFileURL(page).href });
  await sleep(600);
  await send("Runtime.evaluate", { expression: "document.querySelector('.anim').classList.add('on')" });
  const start = Date.now();
  const times = [];
  for (let n = 0; Date.now() - start < Number(seconds) * 1000 + 300; n++) {
    const shot = await send("Page.captureScreenshot", { format: "png" });
    times.push(Date.now() - start);
    writeFileSync(join(outDir, `f${String(n).padStart(4, "0")}.png`), Buffer.from(shot.data, "base64"));
    await sleep(60);
  }
  writeFileSync(join(outDir, "times.json"), JSON.stringify(times));
  ws.close();
} finally {
  chrome.kill();
}
