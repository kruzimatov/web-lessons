FORMS_SANDBOX = "allow-forms allow-scripts allow-popups allow-popups-to-escape-sandbox"

TICKS = """<form>
  <p>What do you like?</p>
  <input type="checkbox" id="foot">
  <label for="foot">Football</label>
  <input type="checkbox" id="chess">
  <label for="chess">Chess</label>

  <p>Pizza size:</p>
  <input type="radio" name="size" id="small">
  <label for="small">Small</label>
  <input type="radio" name="size" id="big">
  <label for="big">Big</label>
</form>"""

SELECT = """<form>
  <label for="pet">Favorite pet</label>
  <select id="pet">
    <option>Dog</option>
    <option>Cat</option>
    <option>Fish</option>
  </select>
</form>"""

LESSON = {
    "n": 13,
    "week": 3,
    "folder": "week3/lesson13_forms_2",
    "title": "Forms 2: ticks, choices and messages",
    "goal": "Today you add tick boxes, \"pick one\" buttons, drop-down lists and big message boxes to forms.",
    "sandbox": FORMS_SANDBOX,
    "cheats": [
        ("<input type=\"checkbox\">", "Tick many"),
        ("<input type=\"radio\" name=\"size\">", "Pick one. Same name in a group"),
        ("<select><option>Cat</option></select>", "A drop-down list"),
        ("<option selected>", "Chosen at the start"),
        ("<textarea rows=\"4\"></textarea>", "A big message box"),
    ],
    "review": [
        ("quiz", "Which tag is a box to type in?", ["`<input>`", "`<label>`", "`<box>`"], 0),
        ("quiz", "Which type shows dots?", ["`type=\"password\"`", "`type=\"dots\"`", "`type=\"text\"`"], 0),
        ("quiz", "What does `required` do?", ["You must fill the box before sending", "Makes the box red", "Deletes the box"], 0),
    ],
    "blocks": [
        ("h", "Part 1: Tick boxes and \"pick one\" buttons"),
        ("anim", "choices", "checkbox: tick many. radio: only one. select: pick from a list."),
        ("code", TICKS, "checkbox and radio"),
        ("table", ["type", "You can choose", "Example"], [
            ["`checkbox`", "Many, or none", "What do you like?"],
            ["`radio`", "Only ONE", "Small or big pizza"],
        ]),
        ("say", "Radio buttons in one group need the **same** `name`. That is how the browser knows only one can be picked."),
        ("uz", "radio guruhida name bir xil bo'lsa, faqat bittasini tanlash mumkin."),
        ("try", "Click everything. Then change `name=\"size\"` on one radio to `name=\"x\"`. What breaks?", TICKS),
        ("quiz", "You can pick only ONE answer. Which type?", ["`checkbox`", "`radio`", "`text`"], 1),

        ("h", "Part 2: Drop-down lists"),
        ("say", "`<select>` makes a drop-down list. Every choice is an `<option>`."),
        ("code", SELECT, "A drop-down with 3 choices"),
        ("try", "Add 2 more pets. Then add `selected` to the Cat option: `<option selected>Cat</option>`.", SELECT),
        ("quiz", "Every choice in a select is a...", ["`<li>`", "`<option>`", "`<choice>`"], 1),

        ("h", "Part 3: Big message boxes"),
        ("say", "`<input>` is for one line. For a long message use `<textarea>`. It DOES have a closing tag."),
        ("code", "<form>\n  <label for=\"msg\">Your message</label><br>\n  <textarea id=\"msg\" rows=\"4\" placeholder=\"Write here...\"></textarea><br>\n  <button>Send</button>\n</form>", "`rows=\"4\"`: 4 lines tall"),
        ("try", "Make the box 6 rows tall and write a message to a friend.",
         "<form>\n  <label for=\"msg\">Your message</label><br>\n  <textarea id=\"msg\" rows=\"4\" placeholder=\"Write here...\"></textarea><br>\n  <button>Send</button>\n</form>"),
        ("quiz", "For a long message you use...", ["`<input type=\"text\">`", "`<textarea>`", "`<p>`"], 1),
    ],
    "mistakes": [
        "Radio buttons with different `name`: then you can pick all of them",
        "Writing `<input type=\"select\">`. A drop-down is `<select>` with `<option>`s",
        "Forgetting `</textarea>`: the rest of the page goes into the box!",
        "Labels without `for`: clicking the words does nothing",
    ],
    "practice": [
        {
            "task": "3 checkboxes with labels: \"I like cats\", \"I like dogs\", \"I like fish\".",
            "hints": ["`<input type=\"checkbox\" id=\"cats\">` then a label.", "Do it 3 times with different ids."],
            "start": "",
            "answer": "<input type=\"checkbox\" id=\"cats\"> <label for=\"cats\">I like cats</label>\n<input type=\"checkbox\" id=\"dogs\"> <label for=\"dogs\">I like dogs</label>\n<input type=\"checkbox\" id=\"fish\"> <label for=\"fish\">I like fish</label>",
        },
        {
            "task": "\"Cats or dogs?\" with 2 radio buttons. Only one can be picked.",
            "hints": ["Both radio buttons need the SAME name.", "`name=\"pet\"` on both."],
            "start": "<p>Cats or dogs?</p>\n",
            "answer": "<p>Cats or dogs?</p>\n<input type=\"radio\" name=\"pet\" id=\"cats\"> <label for=\"cats\">Cats</label>\n<input type=\"radio\" name=\"pet\" id=\"dogs\"> <label for=\"dogs\">Dogs</label>",
        },
        {
            "task": "There are 3 mistakes. Fix them.",
            "hints": ["Radio names, a drop-down, a message box.", "Both radios: `name=\"drink\"`. Use `<select>` and `</select>`. Close the textarea."],
            "start": "<p>Drink:</p>\n<input type=\"radio\" name=\"drink\" id=\"tea\"> <label for=\"tea\">Tea</label>\n<input type=\"radio\" name=\"drinks\" id=\"milk\"> <label for=\"milk\">Milk</label>\n<input type=\"select\">\n  <option>Red</option>\n<textarea rows=\"3\">",
            "answer": "<p>Drink:</p>\n<input type=\"radio\" name=\"drink\" id=\"tea\"> <label for=\"tea\">Tea</label>\n<input type=\"radio\" name=\"drink\" id=\"milk\"> <label for=\"milk\">Milk</label>\n<select>\n  <option>Red</option>\n</select>\n<textarea rows=\"3\"></textarea>",
        },
        {
            "task": "A drop-down \"Favorite color\" with 5 colors. Blue is chosen at the start.",
            "hints": ["`<select>` with 5 `<option>`.", "`<option selected>Blue</option>`."],
            "start": "",
            "answer": "<label for=\"color\">Favorite color</label>\n<select id=\"color\">\n  <option>Red</option>\n  <option selected>Blue</option>\n  <option>Green</option>\n  <option>Yellow</option>\n  <option>Pink</option>\n</select>",
        },
        {
            "task": "A \"Pizza order\" form: name, size (radio: small, medium, big), toppings (checkboxes: cheese, mushrooms, olives), drink (select), a message box, and an \"Order\" button.",
            "hints": ["Do it in parts: name, size, toppings, drink, message, button.", "Radios share `name=\"size\"`. Checkboxes do not need a name."],
            "start": "<h2>Pizza order</h2>\n",
            "answer": "<h2>Pizza order</h2>\n<form>\n  <p><label for=\"name\">Name</label> <input type=\"text\" id=\"name\" required></p>\n  <p>Size:\n    <input type=\"radio\" name=\"size\" id=\"s\"> <label for=\"s\">Small</label>\n    <input type=\"radio\" name=\"size\" id=\"m\"> <label for=\"m\">Medium</label>\n    <input type=\"radio\" name=\"size\" id=\"b\"> <label for=\"b\">Big</label>\n  </p>\n  <p>Toppings:\n    <input type=\"checkbox\" id=\"cheese\"> <label for=\"cheese\">Cheese</label>\n    <input type=\"checkbox\" id=\"mush\"> <label for=\"mush\">Mushrooms</label>\n    <input type=\"checkbox\" id=\"olive\"> <label for=\"olive\">Olives</label>\n  </p>\n  <p><label for=\"drink\">Drink</label>\n    <select id=\"drink\">\n      <option>Water</option>\n      <option>Juice</option>\n    </select>\n  </p>\n  <p><label for=\"note\">Message</label><br>\n    <textarea id=\"note\" rows=\"3\"></textarea>\n  </p>\n  <button>Order</button>\n</form>",
        },
    ],
    "homework": [
        {
            "task": "A quiz form: \"What is 2 + 2?\" with 3 radio answers (3, 4, 5) and a Check button.",
            "answer": "<form>\n  <p>What is 2 + 2?</p>\n  <input type=\"radio\" name=\"q1\" id=\"a3\"> <label for=\"a3\">3</label>\n  <input type=\"radio\" name=\"q1\" id=\"a4\"> <label for=\"a4\">4</label>\n  <input type=\"radio\" name=\"q1\" id=\"a5\"> <label for=\"a5\">5</label>\n  <button>Check</button>\n</form>",
        },
        {
            "task": "\"My holiday\": a drop-down of 4 countries, checkboxes for what to pack (3 things), and a textarea \"Why?\".",
            "answer": "<form>\n  <label for=\"land\">Country</label>\n  <select id=\"land\">\n    <option>Japan</option>\n    <option>Italy</option>\n    <option>Egypt</option>\n    <option>Brazil</option>\n  </select>\n  <p>Pack:\n    <input type=\"checkbox\" id=\"hat\"> <label for=\"hat\">Hat</label>\n    <input type=\"checkbox\" id=\"ball\"> <label for=\"ball\">Ball</label>\n    <input type=\"checkbox\" id=\"book\"> <label for=\"book\">Book</label>\n  </p>\n  <label for=\"why\">Why?</label><br>\n  <textarea id=\"why\" rows=\"3\"></textarea>\n  <button>Send</button>\n</form>",
        },
    ],
}
