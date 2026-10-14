ABOUT_START = """<!DOCTYPE html>
<html>
<head>
  <title>About Me</title>
</head>
<body>
  <!-- 1. Your name -->

  <!-- 2. About you -->

  <!-- 3. Favorite things -->

  <!-- 4. Top 3 -->

</body>
</html>"""

ABOUT_DONE = """<!DOCTYPE html>
<html>
<head>
  <title>About Me</title>
</head>
<body>
  <h1>Hi, I am Ali!</h1>
  <p>I am <strong>8 years old</strong>. I live in London.</p>
  <p>I <em>really</em> love football.</p>
  <hr>
  <h2>My favorite things</h2>
  <ul>
    <li>Pizza</li>
    <li>Lego</li>
    <li>My cat Momo</li>
  </ul>
  <h2>My top 3 games</h2>
  <ol>
    <li>Minecraft</li>
    <li>Football</li>
    <li>Chess</li>
  </ol>
</body>
</html>"""

LESSON = {
    "n": 4,
    "week": 1,
    "folder": "week1/lesson04_practice_about_me",
    "title": "Practice day: my \"About me\" page",
    "goal": "No new tags today! You build a full \"About me\" page with everything you know.",
    "cheats": [
        ("Plan first", "Write a comment where each part goes"),
        ("One <h1>", "Only one big title per page"),
    ],
    "review": [
        ("quiz", "Which list has numbers?", ["`<ul>`", "`<ol>`", "`<li>`"], 1),
        ("quiz", "Every item in a list goes in...", ["`<li>`", "`<p>`", "`<item>`"], 0),
        ("quiz", "Where does a small list inside a list go?", ["After `</ul>`", "Inside the `<li>`", "In the head"], 1),
    ],
    "blocks": [
        ("h", "Part 1: Plan your page"),
        ("say", "Good builders plan first. Here is what your page will have."),
        ("table", ["Part", "Tags you use"], [
            ["Skeleton", "`<!DOCTYPE html>`, `html`, `head`, `title`, `body`"],
            ["Your name", "`<h1>`"],
            ["About you", "`<p>`, `<strong>`, `<em>`"],
            ["A line", "`<hr>`"],
            ["Favorite things", "`<h2>`, `<ul>`, `<li>`"],
            ["Top 3", "`<h2>`, `<ol>`, `<li>`"],
        ]),
        ("uz", "Avval reja, keyin qurilish. Har bir qism uchun qaysi tag kerakligini bilamiz."),
        ("say", "The comments show where each part goes. Write your code under each comment."),
        ("try", "Fill in part 1: your name in an `<h1>` under the first comment.", ABOUT_START),
        ("quiz", "Your top 3 games: which list?", ["`<ul>`", "`<ol>`", "`<hr>`"], 1),

        ("h", "Part 2: A finished example"),
        ("say", "This is how a finished page can look. Yours will have YOUR words."),
        ("code", ABOUT_DONE, "Ali's \"About me\" page"),
        ("try", "Change everything to be about YOU: name, age, city, things you love.", ABOUT_DONE),
        ("quiz", "Which tag makes the line between the parts?", ["`<br>`", "`<hr>`", "`<line>`"], 1),

        ("h", "Part 3: Check your page"),
        ("say", "Before you finish, check these 4 things:"),
        ("steps", [
            "Every tag that opens also closes (except `<br>` and `<hr>`)",
            "Only ONE `<h1>` on the page",
            "Everything you want to see is inside `<body>`",
            "Every list item is inside `<li>`",
        ]),
        ("try", "This page has 4 mistakes. Find them all!",
         "<!DOCTYPE html>\n<html>\n<head>\n  <title>About Me</title>\n</head>\n<body>\n  <h1>Hi, I am Sara!</h1>\n  <h1>I am 9</h1>\n  <p>I like <strong>cats</p></strong>\n  <ul>\n    <li>Cats</li>\n    Dogs\n  </ul>\n</html>"),
        ("quiz", "How many `<h1>` should a page have?", ["One", "Two", "As many as you want"], 0),
    ],
    "mistakes": [
        "Two `<h1>` on one page. Use `<h2>` for the parts",
        "Forgetting `</body>` at the end",
        "Closing tags in the wrong order: `<p><strong>Hi</p></strong>`",
        "Items in a list without `<li>`",
    ],
    "practice": [
        {
            "task": "Start the page: the skeleton with the title \"About Me\" and an `<h1>` with your name.",
            "hints": ["Look at the skeleton in the lesson.", "The title goes in head, the h1 goes in body."],
            "start": "",
            "answer": "<!DOCTYPE html>\n<html>\n<head>\n  <title>About Me</title>\n</head>\n<body>\n  <h1>Hi, I am Ali!</h1>\n</body>\n</html>",
        },
        {
            "task": "Add two paragraphs about you. Make your age strong and one word em. Then an `<hr>`.",
            "hints": ["Age in `<strong>`, one word in `<em>`.", "The `<hr>` comes after the second `</p>`."],
            "start": "<!DOCTYPE html>\n<html>\n<head>\n  <title>About Me</title>\n</head>\n<body>\n  <h1>Hi, I am Ali!</h1>\n</body>\n</html>",
            "answer": "  <h1>Hi, I am Ali!</h1>\n  <p>I am <strong>8 years old</strong>. I live in London.</p>\n  <p>I <em>really</em> love football.</p>\n  <hr>",
        },
        {
            "task": "Fix the 4 mistakes in this page.",
            "hints": ["There are 4: count the h1s, check the order, check the list, check the end.", "Second h1 becomes p. Close strong before p. Dogs needs li. Add `</body>`."],
            "start": "<!DOCTYPE html>\n<html>\n<head>\n  <title>About Me</title>\n</head>\n<body>\n  <h1>Hi, I am Sara!</h1>\n  <h1>I am 9</h1>\n  <p>I like <strong>cats</p></strong>\n  <ul>\n    <li>Cats</li>\n    Dogs\n  </ul>\n</html>",
            "answer": "<!DOCTYPE html>\n<html>\n<head>\n  <title>About Me</title>\n</head>\n<body>\n  <h1>Hi, I am Sara!</h1>\n  <p>I am 9</p>\n  <p>I like <strong>cats</strong></p>\n  <ul>\n    <li>Cats</li>\n    <li>Dogs</li>\n  </ul>\n</body>\n</html>",
        },
        {
            "task": "Add \"My favorite things\" (h2 + dots list of 3) and \"My top 3\" (h2 + numbers list).",
            "hints": ["Favorite things: `<ul>`. Top 3: `<ol>`.", "Each part starts with an `<h2>`."],
            "start": ABOUT_START,
            "answer": "  <h2>My favorite things</h2>\n  <ul>\n    <li>Pizza</li>\n    <li>Lego</li>\n    <li>My cat Momo</li>\n  </ul>\n  <h2>My top 3 games</h2>\n  <ol>\n    <li>Minecraft</li>\n    <li>Football</li>\n    <li>Chess</li>\n  </ol>",
        },
        {
            "task": "The full \"About me\" page: all 4 parts, an `<hr>` between parts, and a fun fact with `<sub>` or `<sup>` at the end.",
            "hints": ["Do it part by part, under each comment.", "Fun fact: `H<sub>2</sub>O`."],
            "start": ABOUT_START,
            "answer": ABOUT_DONE.replace("  </ol>\n</body>", "  </ol>\n  <hr>\n  <p>Fun fact: I drink a lot of H<sub>2</sub>O!</p>\n</body>"),
        },
    ],
    "homework": [
        {
            "task": "Finish your \"About me\" page from today. Copy it here.",
            "answer": ABOUT_DONE,
        },
        {
            "task": "Add a part \"My family\" with an h2 and a list of people. Each person has a small list of what they like.",
            "answer": "<h2>My family</h2>\n<ul>\n  <li>Mom\n    <ul>\n      <li>Cooking</li>\n    </ul>\n  </li>\n  <li>Dad\n    <ul>\n      <li>Football</li>\n    </ul>\n  </li>\n</ul>",
        },
    ],
}
