SKELETON = """<!DOCTYPE html>
<html>
<head>
  <title>My Page</title>
</head>
<body>
  <h1>Hello!</h1>
  <p>This is my first page.</p>
</body>
</html>"""

LESSON = {
    "n": 1,
    "week": 1,
    "folder": "week1/lesson01_what_is_html",
    "title": "What is HTML? Your first web page",
    "goal": "Today you learn what HTML is, write titles and text, and build a full web page.",
    "cheats": [
        ("<h1>Title</h1>", "Big title. h1 to h6, h1 is the biggest"),
        ("<p>Text</p>", "A paragraph of normal text"),
        ("<!-- note -->", "A comment: a note the browser does not show"),
        ("<!DOCTYPE html>", "First line of every page"),
        ("<head> ... </head>", "Hidden info, like the title"),
        ("<title>My Page</title>", "The name on the browser tab"),
        ("<body> ... </body>", "Everything you see"),
    ],
    "review": [],
    "blocks": [
        ("h", "Part 1: Websites and tags"),
        ("say", "Which websites do you know? YouTube, Google, Roblox, Wikipedia... Every one of them is made with **HTML**."),
        ("big", "A website is a file. The browser (Chrome) reads the file and shows it on the screen."),
        ("anim", "file_to_browser", "Your file goes into Chrome. Chrome turns it into a page."),
        ("say", "HTML is made of **tags**. A tag tells the browser what something is: a title, some text, a picture."),
        ("big", "A tag is like a box: open it, put something inside, close it."),
        ("uz", "Tag bu quti: ochamiz, ichiga yozamiz, yopamiz."),
        ("anim", "tag_box", "Open the tag, put something inside, close the tag."),
        ("table", ["Part", "Code", "Meaning"], [
            ["Opening tag", "`<h1>`", "Open the box"],
            ["Content", "`Hello!`", "What is inside"],
            ["Closing tag", "`</h1>`", "Close the box. It has a `/`"],
        ]),
        ("try", "Change Hello! to your name. Watch the right side change.", "<h1>Hello!</h1>"),
        ("quiz", "Which one is a closing tag?", ["`<h1>`", "`</h1>`", "`<1h>`"], 1),

        ("h", "Part 2: Headings h1 to h6"),
        ("say", "Headings are titles. There are 6 of them. `h1` is the biggest, `h6` is the smallest."),
        ("anim", "heading_stairs", "Like stairs: every step down is a smaller title."),
        ("code", "<h1>Heading 1</h1>\n<h2>Heading 2</h2>\n<h3>Heading 3</h3>\n<h4>Heading 4</h4>\n<h5>Heading 5</h5>\n<h6>Heading 6</h6>", "All 6 headings"),
        ("table", ["Heading", "Use it for", "Example"], [
            ["`h1`", "The page title. Only ONE on a page", "My Website"],
            ["`h2`", "Big parts of the page", "My Family, My Games"],
            ["`h3`", "Small parts inside a big part", "My Cat, My Dog"],
            ["`h4` to `h6`", "Very small titles. Not used much", "Notes"],
        ]),
        ("uz", "h1 bu kitobning nomi, h2 bu boblar, h3 bu bob ichidagi kichik qismlar."),
        ("try", "Change the words. Then try to make an h7. What happens?",
         "<h1>Heading 1</h1>\n<h2>Heading 2</h2>\n<h3>Heading 3</h3>\n<h4>Heading 4</h4>\n<h5>Heading 5</h5>\n<h6>Heading 6</h6>"),
        ("quiz", "Which heading is the biggest?", ["`<h6>`", "`<h1>`", "`<h3>`"], 1),

        ("h", "Part 3: Paragraphs"),
        ("say", "Headings are for titles. For normal text we use `<p>`, a **paragraph**. Every `<p>` starts on a new line."),
        ("code", "<h1>My Cat</h1>\n<p>My cat is called Momo.</p>\n<p>She likes to sleep on my bed.</p>", "Title, then text"),
        ("try", "Write about your pet, your toy or your best friend: one h1 and two p.",
         "<h1>My Cat</h1>\n<p>My cat is called Momo.</p>\n<p>She likes to sleep on my bed.</p>"),
        ("quiz", "Which tag is for normal text?", ["`<h1>`", "`<t>`", "`<p>`"], 2),

        ("h", "Part 4: The page skeleton and comments"),
        ("say", "A real page needs a **skeleton**. It is always the same. Every HTML page in the world starts like this."),
        ("anim", "skeleton", "html holds everything. head is hidden info. body is what you see."),
        ("code", SKELETON, "The full page skeleton"),
        ("table", ["Part", "What it does"], [
            ["`<!DOCTYPE html>`", "First line. Says: this is an HTML page"],
            ["`<html>`", "The big box around everything"],
            ["`<head>`", "Hidden info about the page"],
            ["`<title>`", "The name on the browser tab. Goes inside head"],
            ["`<body>`", "Everything you SEE: headings, text, pictures"],
        ]),
        ("uz", "head bu odamning boshi: ichida fikr bor, lekin ko'rinmaydi. body bu tana: hammasi ko'rinadi."),
        ("try", "Change the h1 and the p. The title shows on the browser tab, so you cannot see it here.", SKELETON),
        ("say", "A **comment** is a note for people. The browser does not show it. It starts with `<!--` and ends with `-->`."),
        ("try", "Write your own comment. Does it show on the right side?",
         "<!-- My first page -->\n<h1>Hello!</h1>\n<!-- Text about me -->\n<p>I am 8 years old.</p>"),
        ("quiz", "Where do headings and text go?", ["`<head>`", "`<body>`", "`<title>`"], 1),
    ],
    "mistakes": [
        "Forgot the closing tag: `<h1>Hello` must be `<h1>Hello</h1>`",
        "Wrong slash: `<\\h1>` is wrong, `</h1>` is right",
        "Different tags: `<h1>Hello</h2>` is wrong. Open and close the same tag",
        "Text in the head. Everything you want to SEE goes in the body",
    ],
    "practice": [
        {
            "task": "Make a big title with your name, and a paragraph with your age.",
            "hints": ["Which tag makes the biggest title?", "`<h1>Your name</h1>`, then `<p>I am ... years old.</p>`"],
            "start": "",
            "answer": "<h1>Hi, I am Ali!</h1>\n<p>I am 8 years old.</p>",
        },
        {
            "task": "Stairs: write all 6 headings, from h1 down to h6, with your own words.",
            "hints": ["Start with `<h1>` and go down one number each line.", "The last one is `<h6>`."],
            "start": "",
            "answer": "<h1>Big</h1>\n<h2>Smaller</h2>\n<h3>Smaller</h3>\n<h4>Smaller</h4>\n<h5>Smaller</h5>\n<h6>Smallest</h6>",
        },
        {
            "task": "There are 3 mistakes. Fix them.",
            "hints": ["Look at every closing tag. Does it have a `/`? Does it end with `>`?", "Line 1 needs `</h1>`, line 2 needs `</p>`, line 3 opens h2 but closes h3."],
            "start": "<h1>My Games<h1>\n<p>I play football.</p\n<h2>My Pets</h3>",
            "answer": "<h1>My Games</h1>\n<p>I play football.</p>\n<h2>My Pets</h2>",
        },
        {
            "task": "Build a full page from zero: the skeleton, a title \"About Me\", an h1 and a p.",
            "hints": ["Start with `<!DOCTYPE html>`, then `<html>`.", "Inside html: `<head>` with `<title>`, then `<body>` with your h1 and p."],
            "start": "",
            "answer": "<!DOCTYPE html>\n<html>\n<head>\n  <title>About Me</title>\n</head>\n<body>\n  <h1>About Me</h1>\n  <p>My name is Ali.</p>\n</body>\n</html>",
        },
        {
            "task": "\"My Favorite Animal\" page: one h1, two h2 parts (\"What it eats\", \"Where it lives\"), a p under each h2, and a comment above each part.",
            "hints": ["You need 1 h1, 2 h2, 2 p and 3 comments.", "A comment looks like `<!-- Food -->`. Put one above each part."],
            "start": "",
            "answer": "<!-- Title -->\n<h1>My Favorite Animal: the Lion</h1>\n<!-- Food -->\n<h2>What it eats</h2>\n<p>Lions eat meat.</p>\n<!-- Home -->\n<h2>Where it lives</h2>\n<p>Lions live in Africa.</p>",
        },
    ],
    "homework": [
        {
            "task": "\"My Family\": an h1, then a p about 3 people in your family.",
            "answer": "<h1>My Family</h1>\n<p>My mom likes cooking.</p>\n<p>My dad likes football.</p>\n<p>My sister likes drawing.</p>",
        },
        {
            "task": "Upside-down stairs: write the headings from h6 up to h1.",
            "answer": "<h6>Smallest</h6>\n<h5>Small</h5>\n<h4>Medium</h4>\n<h3>Bigger</h3>\n<h2>Big</h2>\n<h1>Biggest</h1>",
        },
    ],
}
