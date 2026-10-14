FORMS_SANDBOX = "allow-forms allow-scripts allow-popups allow-popups-to-escape-sandbox"
MENU = '<a href="index.html">Home</a> | <a href="hobbies.html">Hobbies</a> | <a href="contact.html">Write to me</a>'

FORM = """<form>
  <p>
    <label for="name">Your name</label>
    <input type="text" id="name" required>
  </p>
  <p>
    <label for="email">Your email</label>
    <input type="email" id="email" placeholder="you@example.com">
  </p>
  <p>How did you find my site?
    <input type="radio" name="found" id="friend"> <label for="friend">A friend</label>
    <input type="radio" name="found" id="google"> <label for="google">Google</label>
  </p>
  <p>
    <label for="fav">Best page</label>
    <select id="fav">
      <option>Home</option>
      <option>Hobbies</option>
    </select>
  </p>
  <p>
    <input type="checkbox" id="news"> <label for="news">Tell me about new pages</label>
  </p>
  <p>
    <label for="msg">Message</label><br>
    <textarea id="msg" rows="4"></textarea>
  </p>
  <button>Send</button>
</form>"""

CONTACT = f"""<header>
  <h1>Write to me</h1>
</header>
<nav>
  {MENU}
</nav>
<main>
  <p>Do you like my website? Tell me!</p>
{chr(10).join("  " + line for line in FORM.splitlines())}
</main>
<footer>
  <p><small>&copy; 2026 Ali</small></p>
</footer>"""

LESSON = {
    "n": 14,
    "week": 3,
    "folder": "week3/lesson14_practice_contact_page",
    "title": "Practice day: my \"Write to me\" page",
    "goal": "No new tags today! You build a contact page with every kind of form box.",
    "sandbox": FORMS_SANDBOX,
    "cheats": [
        ("contact.html", "Your \"Write to me\" page"),
        ("Labels match ids", "for=\"email\" and id=\"email\""),
    ],
    "review": [
        ("quiz", "Pick only ONE answer. Which type?", ["`radio`", "`checkbox`", "`select`"], 0),
        ("quiz", "Radio buttons in one group need the same...", ["`id`", "`name`", "`label`"], 1),
        ("quiz", "A long message box is...", ["`<textarea>`", "`<input>`", "`<message>`"], 0),
    ],
    "blocks": [
        ("h", "Part 1: Plan the page"),
        ("table", ["Part", "Tags"], [
            ["Top", "`<header>` with `<h1>`"],
            ["Menu", "`<nav>` with 3 links, the new one is `contact.html`"],
            ["Content", "`<main>` with a p and the form"],
            ["Form", "text, email, radio, select, checkbox, textarea, button"],
            ["Bottom", "`<footer>` with copyright"],
        ]),
        ("uz", "Yangi sahifa: contact.html. Menyuga ham qo'shamiz."),
        ("try", "Write the new menu with the third link \"Write to me\".", '<a href="index.html">Home</a> | <a href="hobbies.html">Hobbies</a> | '),
        ("quiz", "The new page file is `contact.html`. What is the link?", ["`href=\"contact.html\"`", "`href=\"https://contact\"`", "`src=\"contact.html\"`"], 0),

        ("h", "Part 2: The form"),
        ("code", FORM, "A form with every kind of box"),
        ("try", "Fill it in and press Send. Then change the questions to your own.", FORM),
        ("quiz", "Which box lets you tick \"Tell me about new pages\"?", ["`checkbox`", "`radio`", "`textarea`"], 0),

        ("h", "Part 3: The full page"),
        ("code", CONTACT, "contact.html, body part"),
        ("try", "This page has 4 mistakes. Find them!",
         CONTACT.replace('name="found" id="google"', 'name="find" id="google"').replace("</textarea>", "").replace('<label for="email">', '<label for="mail">').replace("</main>", "")),
        ("quiz", "Where does the form go?", ["In `<main>`", "In `<footer>`", "In `<head>`"], 0),
    ],
    "mistakes": [
        "Forgetting to add the new page to the menu on ALL pages",
        "Radio buttons with different names",
        "Forgetting `</textarea>`",
        "A label `for` that does not match the input `id`",
    ],
    "practice": [
        {
            "task": "Write the menu with 3 links: Home, Hobbies, Write to me (`contact.html`).",
            "hints": ["3 links with ` | ` between.", "The new one: `<a href=\"contact.html\">Write to me</a>`."],
            "start": "",
            "answer": MENU,
        },
        {
            "task": "A form with your name (required) and email, each with a label, and a Send button.",
            "hints": ["Two labels, two inputs, one button.", "Name has `required`. Email has `type=\"email\"`."],
            "start": "<form>\n\n</form>",
            "answer": "<form>\n  <label for=\"name\">Your name</label>\n  <input type=\"text\" id=\"name\" required>\n  <label for=\"email\">Your email</label>\n  <input type=\"email\" id=\"email\">\n  <button>Send</button>\n</form>",
        },
        {
            "task": "This page has 4 mistakes. Fix them.",
            "hints": ["4 mistakes: radio names, a closing tag, a label, a box.", "Both radios `name=\"found\"`. Add `</textarea>`. `for=\"mail\"` should be `email`. Add `</main>`."],
            "start": CONTACT.replace('name="found" id="google"', 'name="find" id="google"').replace("</textarea>", "").replace('<label for="email">', '<label for="mail">').replace("</main>", ""),
            "answer": CONTACT,
        },
        {
            "task": "Add to your form: a radio question with 2 answers, a select with 3 choices, and a checkbox.",
            "hints": ["Radio: 2 buttons, same name. Select: 3 options.", "Checkbox: `<input type=\"checkbox\" id=\"news\">` with a label."],
            "start": FORM.split("  <p>How did")[0] + "  <button>Send</button>\n</form>",
            "answer": FORM,
        },
        {
            "task": "The full `contact.html`: header, nav, main with the form (every kind of box), footer. Make it in VS Code and add the link to the menu on all your pages.",
            "hints": ["Start with the 4 boxes: header, nav, main, footer.", "Copy your form into main."],
            "start": "",
            "answer": CONTACT,
        },
    ],
    "homework": [
        {
            "task": "Copy your `contact.html` from VS Code here.",
            "answer": CONTACT,
        },
        {
            "task": "Add a question to your form: \"How many stars for my site?\" with a number box from 1 to 5.",
            "answer": "<p>\n  <label for=\"stars\">How many stars for my site?</label>\n  <input type=\"number\" id=\"stars\" min=\"1\" max=\"5\">\n</p>",
        },
    ],
}
