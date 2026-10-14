FORMS_SANDBOX = "allow-forms allow-scripts allow-popups allow-popups-to-escape-sandbox"

FIRST = """<form>
  <label for="name">Your name</label>
  <input type="text" id="name">
  <button>Send</button>
</form>"""

TYPES = """<form>
  <p>
    <label for="email">Email</label>
    <input type="email" id="email">
  </p>
  <p>
    <label for="pass">Password</label>
    <input type="password" id="pass">
  </p>
  <p>
    <label for="age">Age</label>
    <input type="number" id="age">
  </p>
  <p>
    <label for="bday">Birthday</label>
    <input type="date" id="bday">
  </p>
  <button>Sign up</button>
</form>"""

LESSON = {
    "n": 12,
    "week": 2,
    "folder": "week2/lesson12_forms_1",
    "title": "Forms 1: boxes to type in",
    "goal": "Today you make forms: boxes where people type their name, email, password and age.",
    "sandbox": FORMS_SANDBOX,
    "cheats": [
        ("<form> ... </form>", "Holds a form"),
        ("<label for=\"name\">Name</label>", "Words next to a box"),
        ("<input type=\"text\" id=\"name\">", "A box to type in. No closing tag"),
        ("type=\"email\" / \"password\" / \"number\" / \"date\"", "Other kinds of boxes"),
        ("<button>Send</button>", "Sends the form"),
        ("placeholder=\"...\"", "Grey hint text"),
        ("required", "Must be filled in"),
        ("min=\"1\" max=\"10\"", "Smallest and biggest number"),
    ],
    "review": [
        ("quiz", "Which box holds the menu?", ["`<nav>`", "`<footer>`", "`<header>`"], 0),
        ("quiz", "How many `<main>` on a page?", ["One", "Two", "Many"], 0),
        ("quiz", "Which tag colors a few words inside a line?", ["`<div>`", "`<span>`", "`<section>`"], 1),
    ],
    "blocks": [
        ("h", "Part 1: Your first form"),
        ("say", "A **form** lets people send you information: sign up, write a message, answer a quiz."),
        ("anim", "form_fill", "label says what to type, input is the box, button sends it."),
        ("code", FIRST, "A form with one box and a button"),
        ("table", ["Tag", "What it does"], [
            ["`<form>`", "Holds the whole form"],
            ["`<label>`", "The words next to a box"],
            ["`<input>`", "A box to type in. No closing tag"],
            ["`<button>`", "The button that sends the form"],
        ]),
        ("say", "`for=\"name\"` on the label and `id=\"name\"` on the input join them. Click the label: the box gets ready for typing!"),
        ("uz", "label ning for= qiymati input ning id= qiymati bilan bir xil bo'lsin."),
        ("try", "Type your name and press Send. Then click the label \"Your name\".", FIRST),
        ("quiz", "Which tag is the box you type in?", ["`<label>`", "`<input>`", "`<form>`"], 1),

        ("h", "Part 2: Different kinds of boxes"),
        ("say", "Change `type` and you get a different box."),
        ("code", TYPES, "4 types of input"),
        ("table", ["type", "What you get"], [
            ["`text`", "Any words"],
            ["`email`", "An email address. It checks the `@`"],
            ["`password`", "Dots instead of letters"],
            ["`number`", "Only numbers, with up and down arrows"],
            ["`date`", "A calendar to pick a day"],
        ]),
        ("try", "Try every box. Type letters in the Age box: what happens?", TYPES),
        ("quiz", "Which type shows dots instead of letters?", ["`text`", "`password`", "`secret`"], 1),

        ("h", "Part 3: Helpful extras"),
        ("code", "<form>\n  <label for=\"user\">Username</label>\n  <input type=\"text\" id=\"user\" placeholder=\"for example: ali2018\" required>\n  <label for=\"age\">Age</label>\n  <input type=\"number\" id=\"age\" min=\"5\" max=\"15\">\n  <button>Send</button>\n</form>", "placeholder, required, min and max"),
        ("table", ["Extra", "What it does"], [
            ["`placeholder=\"...\"`", "Grey hint text inside the box"],
            ["`required`", "You must fill it before sending"],
            ["`min=\"5\" max=\"15\"`", "The smallest and biggest number allowed"],
        ]),
        ("uz", "required bo'lsa, bo'sh qoldirib yuborib bo'lmaydi."),
        ("try", "Press Send with an empty Username. Then type age 20 and press Send. What does the browser say?",
         "<form>\n  <label for=\"user\">Username</label>\n  <input type=\"text\" id=\"user\" placeholder=\"for example: ali2018\" required>\n  <label for=\"age\">Age</label>\n  <input type=\"number\" id=\"age\" min=\"5\" max=\"15\">\n  <button>Send</button>\n</form>"),
        ("quiz", "Which extra makes a box \"must fill\"?", ["`placeholder`", "`required`", "`max`"], 1),
    ],
    "mistakes": [
        "Writing `</input>`. `<input>` has no closing tag",
        "The label `for` and the input `id` are different",
        "Using `type=\"text\"` for a password: everyone can read it",
        "Forgetting the `<button>`: there is no way to send",
    ],
    "practice": [
        {
            "task": "A form with a label \"Favorite food\", a text box and a button \"Send\".",
            "hints": ["form, label, input, button.", "label `for=\"food\"` and input `id=\"food\"`."],
            "start": "",
            "answer": "<form>\n  <label for=\"food\">Favorite food</label>\n  <input type=\"text\" id=\"food\">\n  <button>Send</button>\n</form>",
        },
        {
            "task": "A login form: Email and Password boxes, each with a label, and a \"Log in\" button.",
            "hints": ["Email box: `type=\"email\"`. Password box: `type=\"password\"`.", "Each box has its own label with matching for and id."],
            "start": "<h2>Log in</h2>\n",
            "answer": "<h2>Log in</h2>\n<form>\n  <p>\n    <label for=\"email\">Email</label>\n    <input type=\"email\" id=\"email\">\n  </p>\n  <p>\n    <label for=\"pass\">Password</label>\n    <input type=\"password\" id=\"pass\">\n  </p>\n  <button>Log in</button>\n</form>",
        },
        {
            "task": "There are 3 mistakes. Fix them.",
            "hints": ["Check the ids, the closing tags, the password type.", "`id=\"nam\"` should be `name`. Delete `</input>`. Password needs `type=\"password\"`."],
            "start": "<form>\n  <label for=\"name\">Name</label>\n  <input type=\"text\" id=\"nam\"></input>\n  <label for=\"pw\">Password</label>\n  <input type=\"text\" id=\"pw\">\n  <button>Send</button>\n</form>",
            "answer": "<form>\n  <label for=\"name\">Name</label>\n  <input type=\"text\" id=\"name\">\n  <label for=\"pw\">Password</label>\n  <input type=\"password\" id=\"pw\">\n  <button>Send</button>\n</form>",
        },
        {
            "task": "\"How old are you?\" with a number box from 1 to 100, a placeholder \"Your age\", and required.",
            "hints": ["`type=\"number\"` with min and max.", "Add `placeholder=\"Your age\"` and `required`."],
            "start": "",
            "answer": "<form>\n  <label for=\"age\">How old are you?</label>\n  <input type=\"number\" id=\"age\" min=\"1\" max=\"100\" placeholder=\"Your age\" required>\n  <button>Send</button>\n</form>",
        },
        {
            "task": "\"Join my club\" sign-up form: name (required), email, password, birthday (date), and a \"Join\" button. Each box has a label and a placeholder where it fits.",
            "hints": ["4 boxes: text, email, password, date.", "Put each label and box in its own `<p>`."],
            "start": "<h2>Join my club</h2>\n",
            "answer": "<h2>Join my club</h2>\n<form>\n  <p>\n    <label for=\"name\">Name</label>\n    <input type=\"text\" id=\"name\" placeholder=\"Your name\" required>\n  </p>\n  <p>\n    <label for=\"email\">Email</label>\n    <input type=\"email\" id=\"email\" placeholder=\"you@example.com\">\n  </p>\n  <p>\n    <label for=\"pass\">Password</label>\n    <input type=\"password\" id=\"pass\">\n  </p>\n  <p>\n    <label for=\"bday\">Birthday</label>\n    <input type=\"date\" id=\"bday\">\n  </p>\n  <button>Join</button>\n</form>",
        },
    ],
    "homework": [
        {
            "task": "A form \"Order a pizza\": your name, a number box \"How many?\" (1 to 5) and an \"Order\" button.",
            "answer": "<h2>Order a pizza</h2>\n<form>\n  <label for=\"name\">Your name</label>\n  <input type=\"text\" id=\"name\" required>\n  <label for=\"count\">How many?</label>\n  <input type=\"number\" id=\"count\" min=\"1\" max=\"5\">\n  <button>Order</button>\n</form>",
        },
        {
            "task": "A form \"My birthday party\": name, email and the party date, all required.",
            "answer": "<form>\n  <label for=\"name\">Name</label>\n  <input type=\"text\" id=\"name\" required>\n  <label for=\"email\">Email</label>\n  <input type=\"email\" id=\"email\" required>\n  <label for=\"day\">Party date</label>\n  <input type=\"date\" id=\"day\" required>\n  <button>Send</button>\n</form>",
        },
    ],
}
