LESSON = {
    "n": 15,
    "week": 3,
    "folder": "week3/lesson15_review_game",
    "title": "Review game and test",
    "goal": "Today is a game! 4 rounds of questions about everything you learned. Count your green answers.",
    "quizzes_per_part": 4,
    "cheats": [
        ("Void tags", "br, hr, img, input, meta: no closing tag"),
    ],
    "review": [
        ("quiz", "What is the first line of every page?", ["`<html>`", "`<!DOCTYPE html>`", "`<body>`"], 1),
        ("quiz", "Which part of the page do you SEE?", ["`<head>`", "`<body>`", "`<title>`"], 1),
        ("quiz", "How many headings are there?", ["6", "3", "10"], 0),
    ],
    "blocks": [
        ("h", "Round 1: Text and lists"),
        ("say", "Answer the 4 questions, then fix the bugs. Every green answer is one point!"),
        ("quiz", "Which tag says \"this is IMPORTANT\"?", ["`<b>`", "`<strong>`", "`<u>`"], 1),
        ("quiz", "How do you write x²?", ["`x<sub>2</sub>`", "`x<sup>2</sup>`", "`x<small>2</small>`"], 1),
        ("quiz", "Steps of a recipe go in a...", ["`<ul>`", "`<ol>`", "`<table>`"], 1),
        ("quiz", "How do you show `<` on the page?", ["`&lt;`", "`&gt;`", "`<<`"], 0),
        ("try", "Bug hunt: 4 mistakes.", "<h1>My Page</h2>\n<p>Hello</br>world</p>\n<ul>\n  <li>Milk\n  <li>Bread</li>\n</ol>"),

        ("h", "Round 2: Links and images"),
        ("quiz", "Which part of a link says where it goes?", ["`href`", "`src`", "`alt`"], 0),
        ("quiz", "How do you open a link in a new tab?", ["`target=\"_blank\"`", "`new=\"tab\"`", "`href=\"_blank\"`"], 0),
        ("quiz", "Which part of an image says what is in the picture?", ["`src`", "`alt`", "`width`"], 1),
        ("quiz", "Your picture `cat.jpg` is in the `images` folder. The src is...", ["`images/cat.jpg`", "`cat.jpg/images`", "`images`"], 0),
        ("try", "Bug hunt: 3 mistakes.", "<a href=\"wikipedia.org\">Wikipedia\n<img scr=\"https://picsum.photos/id/237/400/300\" alt=\"A puppy\">"),

        ("h", "Round 3: Tables and media"),
        ("quiz", "Which tag makes a row?", ["`<tr>`", "`<td>`", "`<th>`"], 0),
        ("quiz", "One cell 2 columns wide:", ["`rowspan=\"2\"`", "`colspan=\"2\"`", "`span=\"2\"`"], 1),
        ("quiz", "Which tag shows a YouTube video?", ["`<video>`", "`<iframe>`", "`<youtube>`"], 1),
        ("quiz", "What gives a video a play button?", ["`controls`", "`play`", "`button`"], 0),
        ("try", "Bug hunt: 3 mistakes.", "<table border=\"1\">\n  <tr>\n    <td>Name</td>\n    <td>Age</td>\n  <tr>\n    <td>Ali</td>\n    <tr>8</tr>\n  </tr>\n</table>"),

        ("h", "Round 4: Page boxes and forms"),
        ("quiz", "Where does the menu go?", ["`<nav>`", "`<footer>`", "`<main>`"], 0),
        ("quiz", "Which tag is a box to type in?", ["`<input>`", "`<label>`", "`<type>`"], 0),
        ("quiz", "You can pick only ONE answer. Which type?", ["`checkbox`", "`radio`", "`text`"], 1),
        ("quiz", "A drop-down list is...", ["`<select>`", "`<input type=\"list\">`", "`<dropdown>`"], 0),
        ("try", "Bug hunt: 3 mistakes.", "<form>\n  <label for=\"name\">Name</label>\n  <input type=\"text\" id=\"nam\"></input>\n  <input type=\"radio\" name=\"a\" id=\"yes\"> Yes\n  <input type=\"radio\" name=\"b\" id=\"no\"> No\n  <button>Send</button>\n</form>"),
    ],
    "mistakes": [
        "Opening and closing different tags",
        "Writing closing tags for `<br>`, `<hr>`, `<img>`, `<input>`",
        "Forgetting quotes around values",
        "Different names for one radio group",
    ],
    "practice": [
        {
            "task": "Test 1: a full page skeleton with the title \"Test\", an h1 and a p with one strong word.",
            "hints": ["DOCTYPE, html, head, title, body.", "`<strong>` goes inside the p."],
            "start": "",
            "answer": "<!DOCTYPE html>\n<html>\n<head>\n  <title>Test</title>\n</head>\n<body>\n  <h1>My test</h1>\n  <p>I am <strong>ready</strong>!</p>\n</body>\n</html>",
        },
        {
            "task": "Test 2: a numbers list of 3 planets. Each planet is a link to its Wikipedia page, opening in a new tab.",
            "hints": ["`<ol>` with 3 `<li>`, each with an `<a>`.", "`target=\"_blank\"` in every link."],
            "start": "",
            "answer": "<ol>\n  <li><a href=\"https://en.wikipedia.org/wiki/Mars\" target=\"_blank\">Mars</a></li>\n  <li><a href=\"https://en.wikipedia.org/wiki/Venus\" target=\"_blank\">Venus</a></li>\n  <li><a href=\"https://en.wikipedia.org/wiki/Earth\" target=\"_blank\">Earth</a></li>\n</ol>",
        },
        {
            "task": "Test 3: there are 5 mistakes. Fix them all.",
            "hints": ["5 mistakes: check every box, picture, number and table.", "Close header. Add alt. sup should be sub. Add border. Footer needs an opening tag."],
            "start": "<header>\n  <h1>Quiz</h1>\n<main>\n  <img src=\"https://picsum.photos/id/1025/400/300\">\n  <p>Water is H<sup>2</sup>O</p>\n  <table>\n    <tr><td>Name</td></tr>\n  </table>\n</main>\n</footer>",
            "answer": "<header>\n  <h1>Quiz</h1>\n</header>\n<main>\n  <img src=\"https://picsum.photos/id/1025/400/300\" alt=\"A pug\">\n  <p>Water is H<sub>2</sub>O</p>\n  <table border=\"1\">\n    <tr><td>Name</td></tr>\n  </table>\n</main>\n<footer></footer>",
        },
        {
            "task": "Test 4: a table with title cells Animal and Legs, and 3 animals.",
            "hints": ["Title row with `<th>`.", "Cat 4, Bird 2, Spider 8."],
            "start": "",
            "answer": "<table border=\"1\">\n  <tr><th>Animal</th><th>Legs</th></tr>\n  <tr><td>Cat</td><td>4</td></tr>\n  <tr><td>Bird</td><td>2</td></tr>\n  <tr><td>Spider</td><td>8</td></tr>\n</table>",
        },
        {
            "task": "Test 5: a form with a name box (required), a radio question with 2 answers, a select with 3 choices, and a button.",
            "hints": ["text input, 2 radio, select, button.", "Radios share a name. Name box is required."],
            "start": "",
            "answer": "<form>\n  <label for=\"name\">Name</label>\n  <input type=\"text\" id=\"name\" required>\n  <p>Do you like HTML?\n    <input type=\"radio\" name=\"like\" id=\"y\"> <label for=\"y\">Yes</label>\n    <input type=\"radio\" name=\"like\" id=\"n\"> <label for=\"n\">No</label>\n  </p>\n  <select>\n    <option>Red</option>\n    <option>Green</option>\n    <option>Blue</option>\n  </select>\n  <button>Send</button>\n</form>",
        },
    ],
    "homework": [
        {
            "task": "Write the names of 10 tags you know and what each one does, in a dots list.",
            "answer": "<ul>\n  <li>h1: big title</li>\n  <li>p: text</li>\n  <li>a: link</li>\n  <li>img: picture</li>\n  <li>ul: dots list</li>\n  <li>ol: numbers list</li>\n  <li>table: table</li>\n  <li>form: form</li>\n  <li>input: box to type in</li>\n  <li>nav: menu</li>\n</ul>",
        },
        {
            "task": "Make a table of 4 tags with no closing tag (`br`, `hr`, `img`, `input`) and what they do.",
            "answer": "<table border=\"1\">\n  <tr><th>Tag</th><th>Does</th></tr>\n  <tr><td>&lt;br&gt;</td><td>New line</td></tr>\n  <tr><td>&lt;hr&gt;</td><td>Line across</td></tr>\n  <tr><td>&lt;img&gt;</td><td>Picture</td></tr>\n  <tr><td>&lt;input&gt;</td><td>Box to type in</td></tr>\n</table>",
        },
    ],
}
