VSCODE_SKELETON = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>

</body>
</html>"""

INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Home</title>
</head>
<body>
  <a href="index.html">Home</a> | <a href="hobbies.html">Hobbies</a>
  <h1>Ali's website</h1>
  <p>Welcome to my website!</p>
</body>
</html>"""

HOBBIES = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Hobbies</title>
</head>
<body>
  <a href="index.html">Home</a> | <a href="hobbies.html">Hobbies</a>
  <h1>My hobbies</h1>
  <ul>
    <li>Football</li>
    <li>Chess</li>
  </ul>
</body>
</html>"""

LESSON = {
    "n": 6,
    "week": 1,
    "folder": "week1/lesson06_my_real_website",
    "title": "My real website: VS Code and many pages",
    "goal": "Today you make your REAL website on your computer, with two pages that link to each other.",
    "cheats": [
        ("index.html", "The home page file"),
        ("! then Tab", "VS Code writes the skeleton"),
        ("<a href=\"hobbies.html\">Hobbies</a>", "A link to your own page"),
        ("<meta charset=\"UTF-8\">", "Show every letter correctly"),
        ("Cmd + S, then Refresh", "Save and see the change"),
    ],
    "review": [
        ("quiz", "Which tag makes a link?", ["`<link>`", "`<a>`", "`<l>`"], 1),
        ("quiz", "Which part says where a link goes?", ["`href`", "`target`", "`title`"], 0),
        ("quiz", "How do you open a link in a new tab?", ["`target=\"_blank\"`", "`href=\"new\"`", "`tab=\"new\"`"], 0),
    ],
    "blocks": [
        ("h", "Part 1: Your website folder"),
        ("say", "Until now we wrote code in the browser. Real websites are **files in a folder**. We use **VS Code**, a free program for writing code."),
        ("anim", "folder_tree", "Your website is a folder. Every page is one `.html` file."),
        ("steps", [
            "Ask a parent to install VS Code: `code.visualstudio.com`",
            "On the Desktop, make a new folder: `my-website`",
            "Open VS Code. Click **File**, then **Open Folder**, choose `my-website`",
            "Click the **New File** icon and name it `index.html`",
        ]),
        ("uz", "Sayt bu papka. Har bir sahifa alohida .html fayl."),
        ("say", "`index.html` is special: it is always the **home page** of a website."),
        ("try", "Practise here first: write the name of your website in an `<h1>` and a welcome `<p>`.", "<h1></h1>\n<p></p>"),
        ("quiz", "What is the name of the home page file?", ["`home.html`", "`index.html`", "`main.txt`"], 1),

        ("h", "Part 2: The magic shortcut"),
        ("say", "In `index.html`, type `!` and press **Tab**. VS Code writes the whole skeleton for you!"),
        ("code", VSCODE_SKELETON, "What VS Code writes for you"),
        ("table", ["New line", "What it means"], [
            ["`lang=\"en\"`", "This page is in English"],
            ["`<meta charset=\"UTF-8\">`", "Show all letters correctly: ö, ğ, ü, emoji"],
            ["`<meta name=\"viewport\" ...>`", "Look good on phones and iPads"],
        ]),
        ("steps", [
            "Change `Document` to your page title",
            "Write your `<h1>` and `<p>` in the body",
            "Save: **Cmd + S** (Windows: **Ctrl + S**)",
            "Open the `my-website` folder and double-click `index.html`. It opens in Chrome!",
            "Change something, save, then press **Refresh** in Chrome",
        ]),
        ("uz", "Har safar: o'zgartirish, Save, Chrome da Refresh."),
        ("try", "This is your page with the extra lines. Change the title and the h1.", INDEX.replace("  <a href=\"index.html\">Home</a> | <a href=\"hobbies.html\">Hobbies</a>\n", "")),
        ("quiz", "You changed your code, but Chrome shows the old page. What did you forget?", ["To save and refresh", "To close VS Code", "Nothing"], 0),

        ("h", "Part 3: Two pages, joined by links"),
        ("say", "Make a second file: `hobbies.html`. To link to YOUR OWN page, write only the file name. No `https://`."),
        ("code", "<a href=\"hobbies.html\">My hobbies</a>", "A link to your own page"),
        ("code", INDEX, "index.html with a menu at the top"),
        ("code", HOBBIES, "hobbies.html with the same menu"),
        ("say", "Put the same menu on every page. Then you can always go back home."),
        ("try", "Write the menu for a site with 3 pages: Home, Hobbies and Pets (`pets.html`).", "<a href=\"index.html\">Home</a> | "),
        ("quiz", "How do you link to your page `pets.html`?", ["`href=\"https://pets.html\"`", "`href=\"pets.html\"`", "`href=\"pets\"`"], 1),
    ],
    "mistakes": [
        "File saved as `index.txt`. The name must end with `.html`",
        "Forgot to save before refreshing Chrome",
        "Spaces or capitals in file names. Use `my-pets.html`, not `My Pets.html`",
        "The link name and the file name are different: `hobby.html` vs `hobbies.html`",
    ],
    "practice": [
        {
            "task": "Write the code for your `index.html`: skeleton, title \"Home\", an h1 and a p. Then copy it into VS Code, save and open it in Chrome.",
            "hints": ["Type `!` and press Tab in VS Code.", "Change Document to Home."],
            "start": "",
            "answer": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Home</title>\n</head>\n<body>\n  <h1>Ali's website</h1>\n  <p>Welcome to my website!</p>\n</body>\n</html>",
        },
        {
            "task": "Write `hobbies.html`: skeleton, title \"Hobbies\", an h1 and a list of 3 hobbies. Make it in VS Code too.",
            "hints": ["Same skeleton, new title.", "A list is `<ul>` with 3 `<li>`."],
            "start": "",
            "answer": HOBBIES.replace("  <a href=\"index.html\">Home</a> | <a href=\"hobbies.html\">Hobbies</a>\n", "").replace("    <li>Chess</li>\n", "    <li>Chess</li>\n    <li>Lego</li>\n"),
        },
        {
            "task": "These links do not work. There are 3 mistakes. Fix them. (The files are `index.html`, `hobbies.html`, `pets.html`.)",
            "hints": ["Your own pages: no https, and the name must be exact.", "`index.html`, `hobbies.html`, `pets.html`."],
            "start": "<a href=\"https://index.html\">Home</a> |\n<a href=\"hobby.html\">Hobbies</a> |\n<a href=\"pets\">Pets</a>",
            "answer": "<a href=\"index.html\">Home</a> |\n<a href=\"hobbies.html\">Hobbies</a> |\n<a href=\"pets.html\">Pets</a>",
        },
        {
            "task": "Add the menu (Home | Hobbies) at the top of BOTH pages in VS Code. Click the links in Chrome: can you go back and forth?",
            "hints": ["The menu is 2 links with ` | ` between them.", "Put it as the first line in the body."],
            "start": HOBBIES.replace("  <a href=\"index.html\">Home</a> | <a href=\"hobbies.html\">Hobbies</a>\n", ""),
            "answer": HOBBIES,
        },
        {
            "task": "Make a third page `pets.html` (or any topic you like). Put a 3-link menu on ALL three pages.",
            "hints": ["The menu now has 3 links.", "Change the menu on ALL three pages."],
            "start": "",
            "answer": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Pets</title>\n</head>\n<body>\n  <a href=\"index.html\">Home</a> | <a href=\"hobbies.html\">Hobbies</a> | <a href=\"pets.html\">Pets</a>\n  <h1>My pets</h1>\n  <p>I have a cat called Momo.</p>\n</body>\n</html>",
        },
    ],
    "homework": [
        {
            "task": "Copy your `index.html` from VS Code here. It must have the 3-link menu.",
            "answer": INDEX.replace("<a href=\"hobbies.html\">Hobbies</a>", "<a href=\"hobbies.html\">Hobbies</a> | <a href=\"pets.html\">Pets</a>"),
        },
        {
            "task": "On `hobbies.html`, add a numbers list of your top 3 hobbies, and one link to a website about your favorite hobby. Copy it here.",
            "answer": "<h1>My hobbies</h1>\n<ol>\n  <li>Football</li>\n  <li>Chess</li>\n  <li>Lego</li>\n</ol>\n<p>Read about <a href=\"https://en.wikipedia.org/wiki/Football\" target=\"_blank\">football</a>.</p>",
        },
    ],
}
