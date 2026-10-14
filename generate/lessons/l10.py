MENU = '<a href="index.html">Home</a> | <a href="hobbies.html">Hobbies</a> | <a href="pets.html">Pets</a>'
PUPPY = "https://picsum.photos/id/237/400/300"

HOME = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Home</title>
</head>
<body>
  {MENU}
  <h1>Ali's World</h1>
  <img src="{PUPPY}" alt="A black puppy" width="300">
  <p>Hi! I am <strong>Ali</strong>. Welcome to my website.</p>
  <h2>On this website</h2>
  <ul>
    <li>My hobbies</li>
    <li>My pets</li>
  </ul>
  <hr>
  <p><small>&copy; 2026 Ali</small></p>
</body>
</html>"""

HOBBIES = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Hobbies</title>
</head>
<body>
  {MENU}
  <h1>My hobbies</h1>
  <table border="1">
    <tr><th>Hobby</th><th>When</th></tr>
    <tr><td>Football</td><td>Saturday</td></tr>
    <tr><td>Chess</td><td>Every evening</td></tr>
  </table>
  <h2>Watch this</h2>
  <iframe width="400" height="225" src="https://www.youtube.com/embed/jNQXAC9IVRw" title="A video" allowfullscreen></iframe>
</body>
</html>"""

LESSON = {
    "n": 10,
    "week": 2,
    "folder": "week2/lesson10_practice_my_website",
    "title": "Practice day: my website grows",
    "goal": "No new tags today! Your website gets 3 pages with pictures, a table and a video.",
    "sandbox": "allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox allow-presentation",
    "cheats": [
        ("Same menu on every page", "Home | Hobbies | Pets"),
        ("Check every link", "Click them all in Chrome"),
    ],
    "review": [
        ("quiz", "Which tag shows a YouTube video?", ["`<iframe>`", "`<video>`", "`<a>`"], 0),
        ("quiz", "What gives a video a play button?", ["`controls`", "`play`", "`start`"], 0),
        ("quiz", "How do you link to your own page `pets.html`?", ["`href=\"pets.html\"`", "`src=\"pets.html\"`", "`href=\"https://pets\"`"], 0),
    ],
    "blocks": [
        ("h", "Part 1: Plan your website"),
        ("say", "Your website will have 3 pages. Every page has the same menu at the top."),
        ("table", ["Page", "File", "What is on it"], [
            ["Home", "`index.html`", "Your name, a picture, a short welcome, a list"],
            ["Hobbies", "`hobbies.html`", "A table of hobbies and a video"],
            ["Pets (or any topic)", "`pets.html`", "Pictures and facts"],
        ]),
        ("uz", "Har bir sahifada bir xil menyu bo'ladi: istalgan sahifadan uyga qaytish mumkin."),
        ("code", MENU, "The menu: put it on all 3 pages"),
        ("try", "Write your menu. Change Pets to your own topic if you like.", MENU),
        ("quiz", "Why is the menu on EVERY page?", ["So you can go to any page from any page", "Because HTML needs it", "To make it pretty"], 0),

        ("h", "Part 2: The home page"),
        ("code", HOME, "A finished home page"),
        ("try", "Make it YOURS: your name, your picture number, your words.", HOME),
        ("quiz", "The picture does not show. What do you check first?", ["The `src` address", "The `<title>`", "The menu"], 0),

        ("h", "Part 3: The hobbies page"),
        ("code", HOBBIES, "A table and a video on one page"),
        ("try", "Add one more hobby row and change the video.", HOBBIES),
        ("steps", [
            "Click every link in the menu, on every page",
            "Every picture has an `alt`",
            "Every table has `border=\"1\"` and title cells `<th>`",
            "Save every file before you check in Chrome",
        ]),
        ("quiz", "You click \"Pets\" and see \"File not found\". What is wrong?", ["The file name and the href are different", "The picture is too big", "The table has no border"], 0),
    ],
    "mistakes": [
        "Different menus on different pages",
        "A link to `pet.html` when the file is `pets.html`",
        "Forgetting to save one of the files",
        "Pictures without `alt`",
    ],
    "practice": [
        {
            "task": "Write the menu for your 3 pages.",
            "hints": ["3 links with ` | ` between.", "`index.html`, `hobbies.html`, `pets.html`."],
            "start": "",
            "answer": MENU,
        },
        {
            "task": "Build your home page: the menu, h1, a picture with alt and width, a welcome p, and a list. Then copy it into `index.html` in VS Code.",
            "hints": ["Menu, h1, img, p, ul.", "The picture needs alt and width."],
            "start": "",
            "answer": HOME,
        },
        {
            "task": "This home page has 4 mistakes. Fix them.",
            "hints": ["4 mistakes: a picture, a bold word, a link, a list.", "Add alt. Close strong. hobby.html should be hobbies.html. Add `</ul>`."],
            "start": HOME.replace(' alt="A black puppy"', "").replace("</strong>", "").replace('href="hobbies.html"', 'href="hobby.html"').replace("  </ul>\n", ""),
            "answer": HOME,
        },
        {
            "task": "Build the hobbies page: menu, h1, a table of 3 hobbies with title cells, and a YouTube video.",
            "hints": ["Menu, h1, table, h2, iframe.", "The table needs a `<th>` row."],
            "start": "",
            "answer": HOBBIES,
        },
        {
            "task": "Build your third page: menu, h1, 2 pictures with alt, and a numbers list of 3 facts. Then check every link in Chrome.",
            "hints": ["Menu, h1, 2 img, ol.", "Click every link in Chrome when you finish."],
            "start": "",
            "answer": f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Pets</title>\n</head>\n<body>\n  {MENU}\n  <h1>My pets</h1>\n  <img src=\"{PUPPY}\" alt=\"A black puppy\" width=\"250\">\n  <img src=\"https://picsum.photos/id/1025/400/300\" alt=\"A pug in a blanket\" width=\"250\">\n  <ol>\n    <li>Dogs can smell very well.</li>\n    <li>Pugs come from China.</li>\n    <li>Puppies sleep a lot.</li>\n  </ol>\n</body>\n</html>",
        },
    ],
    "homework": [
        {
            "task": "Finish all 3 pages in VS Code. Copy your `index.html` here.",
            "answer": HOME,
        },
        {
            "task": "Copy your `hobbies.html` here.",
            "answer": HOBBIES,
        },
    ],
}
