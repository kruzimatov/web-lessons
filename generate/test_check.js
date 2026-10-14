// Run: node generate/test_check.js
const assert = require("node:assert");
const { checkHTML } = require("../assets/check.js");

const msgs = (src) => checkHTML(src).map((p) => `${p.line}: ${p.msg}`);
const ok = (src) => assert.deepStrictEqual(msgs(src), [], src);
const finds = (src, line, text) =>
  assert.ok(checkHTML(src).some((p) => p.line === line && p.msg.includes(text)), `${src}\n${msgs(src).join("\n")}`);

ok("<!DOCTYPE html>\n<html>\n<head>\n  <title>Hi</title>\n</head>\n<body>\n  <h1>Hi</h1>\n</body>\n</html>");
ok('<p>5 &lt; 10<br>ok</p>\n<!-- note -->\n<img src="a.jpg" alt="A dog">');
ok('<input type="checkbox" id="x"> <label for="x">X</label>\n<textarea rows="3"><p>not a tag</textarea>');

finds("<h1>My Games<h1>", 1, "never closed");
finds("<p>I play</p\n<h2>Pets</h2>", 1, "missing its >");
finds("<h1>Hello</h2>", 1, "Did you mean </h1>");
finds("<p><strong><em>Wow</strong></em></p>", 1, "Close the inside tag first");
finds("<p>Hello</br>world</p>", 1, "Delete </br>");
finds("<h7>Big</h7>", 1, "not an HTML tag");
finds('<a href=wikipedia.org target="blank">W</a>', 1, "quotes");
finds('<a href="https://x.org" target="blank">W</a>', 1, "_blank");
finds('<img scr="dog.jpg">', 1, "needs src");
finds('<img src="dog.jpg">', 1, "needs alt");
finds('<video src="f.mp4"></video>', 1, "controls");
finds("<!-- oops\n<p>Hi</p>", 1, "comment never ends");
finds("<ul>\n  <li>Cats</li>\n  <li>Fish</ul>\n</li>", 3, "Close the inside tag first");
ok("<p><strong><em>Wow</em></strong></p>");
assert.strictEqual(checkHTML("<p><strong><em>Wow</strong></em></p>").length, 1);
ok('<iframe src="https://www.google.com/maps?q=Paris&output=embed" title="Map"></iframe>');

console.log("check.js: all tests pass");
