HOME = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Ali's World</title>
</head>
<body>
  <header>
    <h1>Ali's World</h1>
  </header>
  <nav>
    <a href="index.html">Home</a> | <a href="hobbies.html">Hobbies</a> | <a href="pets.html">Pets</a> | <a href="contact.html">Write to me</a>
  </nav>
  <main>
    <section>
      <h2>About me</h2>
      <img src="https://picsum.photos/id/237/400/300" alt="A black puppy" width="250">
      <p>Hi! I am <strong>Ali</strong>, I am 8 and I make websites.</p>
    </section>
    <section>
      <h2>My top 3</h2>
      <ol>
        <li>Football</li>
        <li>Minecraft</li>
        <li>Pizza</li>
      </ol>
    </section>
  </main>
  <footer>
    <p><small>&copy; 2026 Ali</small></p>
  </footer>
</body>
</html>"""

LESSON = {
    "n": 16,
    "week": 3,
    "folder": "week3/lesson16_final_project",
    "title": "Final project: my website",
    "goal": "Today you finish your website and show it to your family. You are a web builder now!",
    "cheats": [
        ("Checklist", "Skeleton, title, menu, header, main, footer on every page"),
    ],
    "review": [
        ("quiz", "Which tag holds the main content?", ["`<main>`", "`<header>`", "`<nav>`"], 0),
        ("quiz", "Every picture needs...", ["`alt`", "`border`", "`colspan`"], 0),
        ("quiz", "Every page of your site has the same...", ["menu", "picture", "table"], 0),
    ],
    "blocks": [
        ("h", "Part 1: The checklist"),
        ("say", "A finished website has all of these. Tick them one by one."),
        ("table", ["Page", "Must have"], [
            ["Every page", "Skeleton, a good `<title>`, header, nav (menu), main, footer"],
            ["Home `index.html`", "Your name, a picture, a welcome, a list"],
            ["Hobbies", "A table and a video"],
            ["Pets or your topic", "Pictures with alt, facts, links"],
            ["Write to me `contact.html`", "A form with every kind of box"],
        ]),
        ("uz", "Har bir sahifada: skelet, title, menyu, header, main, footer."),
        ("code", HOME, "A finished home page"),
        ("try", "Make it yours: change every word, the picture and the top 3.", HOME),
        ("quiz", "Which file is your home page?", ["`index.html`", "`home.html`", "`first.html`"], 0),

        ("h", "Part 2: Check everything"),
        ("steps", [
            "Click every menu link on every page",
            "Every picture shows, and has an alt",
            "Every video and map plays",
            "Fill in your form and press Send",
            "Read every page: no spelling mistakes",
        ]),
        ("try", "Last bug hunt! This home page has 5 mistakes.",
         HOME.replace("</header>", "").replace(' alt="A black puppy"', "").replace('href="pets.html"', 'href="pet.html"').replace("</strong>", "").replace("        <li>Pizza</li>\n", "        Pizza\n")),
        ("quiz", "You click a menu link and see \"File not found\". What do you check?", ["The href and the file name", "The picture", "The footer"], 0),

        ("h", "Part 3: Show time, and what comes next"),
        ("say", "Open your website in Chrome and show it to your family. Tell them which tags you used!"),
        ("say", "Next month: **CSS**. It paints your website: colors, fonts, boxes, layouts. Here is a sneak peek."),
        ("try", "Sneak peek of CSS: change the colors and see what happens.",
         "<h1 style=\"color: white; background-color: royalblue; padding: 20px\">Ali's World</h1>\n<p style=\"font-size: 24px; color: darkgreen\">CSS paints my website!</p>"),
        ("uz", "Keyingi oy CSS: saytingizni ranglar, shriftlar va bloklar bilan chiroyli qilamiz."),
        ("quiz", "What will CSS do to your website?", ["Paint it: colors, fonts, layout", "Delete it", "Make it a video"], 0),
    ],
    "mistakes": [
        "One page without the menu",
        "Pictures that do not show because the file name is wrong",
        "A `<title>` still saying \"Document\"",
        "Not saving before you check",
    ],
    "practice": [
        {
            "task": "Write your final `index.html` with header, nav (4 links), main with 2 sections, and footer.",
            "hints": ["Start from your home page in VS Code.", "4 boxes, 4 menu links, 2 sections."],
            "start": "",
            "answer": HOME,
        },
        {
            "task": "Check your hobbies page: menu, a table with title cells, a video. Copy it here and fix anything missing.",
            "hints": ["Open hobbies.html in VS Code.", "Menu at the top? Table with th? Video?"],
            "start": "",
            "answer": "(his hobbies page with menu, table with th, and an iframe video)",
        },
        {
            "task": "Fix the 5 mistakes in this home page.",
            "hints": ["5 mistakes: a box, a picture, a link, a bold word, a list item.", "Close header. Add alt. pet.html should be pets.html. Close strong. Pizza needs li."],
            "start": HOME.replace("</header>", "").replace(' alt="A black puppy"', "").replace('href="pets.html"', 'href="pet.html"').replace("</strong>", "").replace("        <li>Pizza</li>\n", "        Pizza\n"),
            "answer": HOME,
        },
        {
            "task": "Check your contact page: every input has a label with the right `for`, radio buttons share a name, and the form has a button.",
            "hints": ["Look at each label and its input.", "for and id must be the same word."],
            "start": "",
            "answer": "(his contact.html, all labels match, radio names match, button present)",
        },
        {
            "task": "Show your site! Open every page in Chrome while your teacher watches on the shared screen. Then write here which page you like most and why.",
            "hints": ["Open index.html in Chrome and click through.", "Write one sentence: which page and why."],
            "start": "<p>My favorite page is </p>",
            "answer": "(any honest answer)",
        },
    ],
    "homework": [
        {
            "task": "Show your website to your family. Copy your final `index.html` here.",
            "answer": HOME,
        },
        {
            "task": "Write 3 things you learned in HTML, in a numbers list.",
            "answer": "<ol>\n  <li>Tags open and close</li>\n  <li>Links join pages</li>\n  <li>Forms collect information</li>\n</ol>",
        },
    ],
}
