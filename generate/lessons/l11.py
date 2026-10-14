STRUCTURED = """<header>
  <h1>Ali's World</h1>
</header>
<nav>
  <a href="index.html">Home</a> | <a href="hobbies.html">Hobbies</a>
</nav>
<main>
  <section>
    <h2>About me</h2>
    <p>I am 8 and I love football.</p>
  </section>
  <section>
    <h2>My pets</h2>
    <p>I have a cat called Momo.</p>
  </section>
</main>
<footer>
  <p><small>&copy; 2026 Ali</small></p>
</footer>"""

LESSON = {
    "n": 11,
    "week": 2,
    "folder": "week2/lesson11_page_structure",
    "title": "Page structure: boxes with names",
    "goal": "Today you organize your page into parts: top, menu, content and bottom.",
    "cheats": [
        ("<div> ... </div>", "A box for a group"),
        ("<span>words</span>", "A box for a few words"),
        ("<header>", "The top of the page"),
        ("<nav>", "The menu"),
        ("<main>", "The main content, only one"),
        ("<section>", "One part of the content"),
        ("<footer>", "The bottom of the page"),
        ("style=\"background-color: pink\"", "Sneak peek of CSS: paint a box"),
    ],
    "review": [
        ("quiz", "What is on every page of your website?", ["The same menu", "The same picture", "Nothing"], 0),
        ("quiz", "A link to your page `hobbies.html`:", ["`href=\"hobbies.html\"`", "`href=\"https://hobbies\"`", "`src=\"hobbies.html\"`"], 0),
        ("quiz", "Which tag shows a picture?", ["`<img>`", "`<iframe>`", "`<picture-box>`"], 0),
    ],
    "blocks": [
        ("h", "Part 1: div and span"),
        ("say", "`<div>` is a plain **box** for a group of things. `<span>` is a box for a few **words** inside a line."),
        ("say", "Boxes are invisible! To see them, here is a sneak peek of CSS (next month): `style=\"background-color: ...\"` paints a box."),
        ("code", "<div style=\"background-color: lightblue\">\n  <h2>My box</h2>\n  <p>Everything in here is one group.</p>\n</div>\n<p>My cat is <span style=\"background-color: yellow\">very fluffy</span>.</p>", "div: a box on its own lines. span: a piece of a line"),
        ("table", ["Tag", "What it is", "Starts a new line?"], [
            ["`<div>`", "A box for a group", "Yes"],
            ["`<span>`", "A box for some words", "No, stays in the line"],
        ]),
        ("uz", "div bu katta quti, yangi qatordan boshlanadi. span bu qator ichidagi kichik quti."),
        ("try", "Change the colors: try `pink`, `lightgreen`, `orange`. Put another p inside the div.",
         "<div style=\"background-color: lightblue\">\n  <h2>My box</h2>\n  <p>Everything in here is one group.</p>\n</div>\n<p>My cat is <span style=\"background-color: yellow\">very fluffy</span>.</p>"),
        ("quiz", "You want to color 2 words in a sentence. Which tag?", ["`<div>`", "`<span>`", "`<p>`"], 1),

        ("h", "Part 2: Boxes with names"),
        ("say", "Some boxes have **names** that say what they are. Every big website uses them."),
        ("anim", "page_layout", "header on top, nav for the menu, main for the content, footer at the bottom."),
        ("table", ["Tag", "Part of the page"], [
            ["`<header>`", "The top: the name of the site"],
            ["`<nav>`", "The menu (navigation)"],
            ["`<main>`", "The main content. Only one"],
            ["`<section>`", "One part of the content"],
            ["`<footer>`", "The bottom: copyright, contact"],
        ]),
        ("uz", "Bu teglar sahifani bo'laklarga ajratadi: tepasi, menyu, asosiy qism, pasti."),
        ("try", "Look at the page. Then change the header and add a third section.", STRUCTURED),
        ("quiz", "Where does the menu go?", ["`<footer>`", "`<nav>`", "`<main>`"], 1),

        ("h", "Part 3: Why boxes with names?"),
        ("steps", [
            "You can find things in your code faster",
            "Programs that read pages aloud know where the menu is",
            "Google understands your page better",
            "Next month, CSS will paint each box",
        ]),
        ("try", "Sneak peek: paint the header, the nav and the footer with colors.",
         STRUCTURED.replace("<header>", "<header style=\"background-color: lightblue\">").replace("<footer>", "<footer style=\"background-color: lightgray\">")),
        ("quiz", "How many `<main>` should a page have?", ["One", "Two", "One for each section"], 0),
    ],
    "mistakes": [
        "More than one `<main>` on a page",
        "Putting the menu links outside `<nav>`",
        "A `<div>` for every tiny thing. Use the named boxes when they fit",
        "Forgetting a closing tag: `</section>`, `</main>`",
    ],
    "practice": [
        {
            "task": "A `<div>` painted `lightgreen` with an h2 and a p inside.",
            "hints": ["`<div style=\"background-color: lightgreen\">`", "Put the h2 and p inside, then `</div>`."],
            "start": "",
            "answer": "<div style=\"background-color: lightgreen\">\n  <h2>My garden</h2>\n  <p>We grow tomatoes.</p>\n</div>",
        },
        {
            "task": "Write a sentence and paint 2 words yellow with `<span>`.",
            "hints": ["`<span style=\"background-color: yellow\">`", "Only the 2 words go inside the span."],
            "start": "<p></p>",
            "answer": "<p>I love <span style=\"background-color: yellow\">chocolate cake</span> very much.</p>",
        },
        {
            "task": "There are 3 mistakes. Fix them.",
            "hints": ["Does header close? How many main? Check the spelling.", "Add `</header>`. One main only. `</foter>` should be `</footer>`."],
            "start": "<header>\n  <h1>My site</h1>\n<nav>\n  <a href=\"index.html\">Home</a>\n</nav>\n<main>\n  <p>Hello!</p>\n</main>\n<main>\n  <p>More</p>\n</main>\n<footer>\n  <p>&copy; 2026</p>\n</foter>",
            "answer": "<header>\n  <h1>My site</h1>\n</header>\n<nav>\n  <a href=\"index.html\">Home</a>\n</nav>\n<main>\n  <p>Hello!</p>\n  <p>More</p>\n</main>\n<footer>\n  <p>&copy; 2026</p>\n</footer>",
        },
        {
            "task": "Put the parts in the right boxes: header (h1), nav (2 links), main with 2 sections, footer (copyright).",
            "hints": ["Top: header. Menu: nav. Content: main. Bottom: footer.", "Each h2 + p goes inside its own `<section>`."],
            "start": "<h1>Sara's page</h1>\n<a href=\"index.html\">Home</a> | <a href=\"art.html\">Art</a>\n<h2>About me</h2>\n<p>I like drawing.</p>\n<h2>My art</h2>\n<p>I draw cats.</p>\n<p>&copy; 2026 Sara</p>",
            "answer": "<header>\n  <h1>Sara's page</h1>\n</header>\n<nav>\n  <a href=\"index.html\">Home</a> | <a href=\"art.html\">Art</a>\n</nav>\n<main>\n  <section>\n    <h2>About me</h2>\n    <p>I like drawing.</p>\n  </section>\n  <section>\n    <h2>My art</h2>\n    <p>I draw cats.</p>\n  </section>\n</main>\n<footer>\n  <p>&copy; 2026 Sara</p>\n</footer>",
        },
        {
            "task": "A full page \"My school\": header, nav, main with 3 sections (teachers, subjects as a list, timetable as a table), and footer. Paint the header with a color.",
            "hints": ["Start with the 4 boxes, then fill main.", "Section 2 has a ul, section 3 has a table."],
            "start": "",
            "answer": "<header style=\"background-color: lightblue\">\n  <h1>My school</h1>\n</header>\n<nav>\n  <a href=\"index.html\">Home</a>\n</nav>\n<main>\n  <section>\n    <h2>Teachers</h2>\n    <p>My teacher is Mrs Brown.</p>\n  </section>\n  <section>\n    <h2>Subjects</h2>\n    <ul>\n      <li>Maths</li>\n      <li>English</li>\n    </ul>\n  </section>\n  <section>\n    <h2>Timetable</h2>\n    <table border=\"1\">\n      <tr><th>Day</th><th>First lesson</th></tr>\n      <tr><td>Monday</td><td>Maths</td></tr>\n    </table>\n  </section>\n</main>\n<footer>\n  <p><small>&copy; 2026 Ali</small></p>\n</footer>",
        },
    ],
    "homework": [
        {
            "task": "In VS Code, put your `index.html` in boxes: header, nav, main, footer. Copy the body here.",
            "answer": STRUCTURED,
        },
        {
            "task": "Do the same on `hobbies.html`. Each hobby gets its own `<section>`.",
            "answer": "<main>\n  <section>\n    <h2>Football</h2>\n    <p>I play on Saturday.</p>\n  </section>\n  <section>\n    <h2>Chess</h2>\n    <p>I play with my dad.</p>\n  </section>\n</main>",
        },
    ],
}
