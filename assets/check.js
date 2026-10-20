// Checks a kid's HTML and explains problems in plain words, with line numbers.
// The browser quietly fixes broken HTML, so without this he never sees his mistakes.

const VOID_TAGS = new Set(["br", "hr", "img", "input", "meta", "link", "source"]);
const RAW_TAGS = new Set(["script", "style", "textarea"]);
const KNOWN_TAGS = new Set([
  "html", "head", "title", "body", "meta", "link", "style", "script",
  "h1", "h2", "h3", "h4", "h5", "h6", "p", "br", "hr",
  "strong", "b", "em", "i", "u", "mark", "small", "del", "ins", "sub", "sup",
  "ul", "ol", "li", "a", "img", "table", "thead", "tbody", "tfoot", "tr", "td", "th", "caption",
  "iframe", "video", "audio", "source", "div", "span", "header", "nav", "main", "section",
  "article", "aside", "footer", "form", "label", "input", "button", "select", "option",
  "textarea", "figure", "figcaption", "blockquote", "code", "pre", "q", "details", "summary",
]);

function checkHTML(src) {
  const problems = [];
  const lineOf = (pos) => src.slice(0, pos).split("\n").length;
  const add = (pos, msg) => problems.push({ line: lineOf(pos), msg });
  const stack = [];
  const forced = []; // inner tags closed for him after a mixed-up order; their own closing tag is expected later
  let i = 0;

  while ((i = src.indexOf("<", i)) !== -1) {
    if (src.startsWith("<!--", i)) {
      const end = src.indexOf("-->", i + 4);
      if (end === -1) { add(i, "This comment never ends. Finish it with -->"); break; }
      i = end + 3;
      continue;
    }
    if (src[i + 1] === "!") {
      const end = src.indexOf(">", i);
      i = end === -1 ? src.length : end + 1;
      continue;
    }
    const m = /^<(\/?)([a-zA-Z][a-zA-Z0-9]*)([^<>]*)(>?)/.exec(src.slice(i));
    if (!m) {
      add(i, "A lonely < sign. To show < on the page, write &lt;");
      i += 1;
      continue;
    }
    const [whole, slash, rawName, attrs, close] = m;
    const name = rawName.toLowerCase();
    const pos = i;
    i += whole.length;

    if (!close) add(pos, `The tag <${slash}${rawName} is missing its > at the end`);
    if (!KNOWN_TAGS.has(name)) { add(pos, `<${rawName}> is not an HTML tag. Check the spelling`); continue; }

    if (slash) {
      if (VOID_TAGS.has(name)) { add(pos, `<${name}> has no closing tag. Delete </${name}>`); continue; }
      const at = stack.map((t) => t.name).lastIndexOf(name);
      if (at === -1) {
        const late = forced.indexOf(name);
        if (late !== -1) { forced.splice(late, 1); continue; } // already reported above
        const top = stack.pop();
        add(pos, top
          ? `</${name}> does not match <${top.name}> from line ${lineOf(top.pos)}. Did you mean </${top.name}>?`
          : `</${name}> closes a tag that was never opened`);
        continue;
      }
      while (stack.length - 1 > at) {
        const inner = stack.pop();
        forced.push(inner.name);
        add(inner.pos, `<${inner.name}> must close before </${name}>. Close the inside tag first`);
      }
      stack.pop();
      continue;
    }

    checkAttributes(name, attrs, pos, add);
    if (VOID_TAGS.has(name) || attrs.trim().endsWith("/")) continue;
    if (RAW_TAGS.has(name)) {
      const end = src.toLowerCase().indexOf(`</${name}>`, i);
      if (end === -1) { add(pos, `<${name}> is never closed. Add </${name}>`); break; }
      i = end + name.length + 3;
      continue;
    }
    stack.push({ name, pos });
  }

  for (const open of stack) add(open.pos, `<${open.name}> is never closed. Add </${open.name}>`);
  const seen = new Set();
  return problems
    .filter((p) => !seen.has(p.line + p.msg) && seen.add(p.line + p.msg))
    .sort((a, b) => a.line - b.line)
    .slice(0, 6);
}

function checkAttributes(name, attrs, pos, add) {
  const outside = attrs.replace(/"[^"]*"|'[^']*'/g, '""'); // only look outside quoted values
  if (/=\s*[^"'\s>]/.test(outside)) add(pos, `Put quotes around the value: name="value"`);
  if (/target\s*=\s*["']?blank/.test(attrs)) add(pos, `Write target="_blank" with a _ at the start`);
  const has = (attr) => new RegExp(`(^|\\s)${attr}(\\s|=|$)`).test(attrs);
  if (name === "img" && !has("src")) add(pos, "<img> needs src: where the picture is");
  if (name === "img" && !has("alt")) add(pos, "<img> needs alt: words that describe the picture");
  if (name === "a" && !has("href")) add(pos, "<a> needs href: where the link goes");
  if ((name === "video" || name === "audio") && !has("controls")) add(pos, `<${name}> needs controls to show the play button`);
}

// One goal from answer_checks.py or game_data.py, on <li data-sel|data-re|data-any data-n>.
// sel: that many elements; re: that many matches in his code; any: that many of these selectors found.
// n = 0 means it must not be there.
function meetsRule(li, src, doc) {
  const n = Number(li.dataset.n);
  const count = (sel) => { try { return doc.querySelectorAll(sel).length; } catch { return -1; } };
  let got;
  if (li.dataset.re) {
    const [, body, flags] = /^\/(.*)\/(\w*)$/s.exec(li.dataset.re);
    got = (src.match(new RegExp(body, flags + "g")) || []).length;
  } else if (li.dataset.any) {
    got = li.dataset.any.split(",").filter((sel) => count(sel) > 0).length;
  } else {
    got = count(li.dataset.sel);
  }
  return n === 0 ? got === 0 : got >= n;
}

if (typeof module === "object") module.exports = { checkHTML };
