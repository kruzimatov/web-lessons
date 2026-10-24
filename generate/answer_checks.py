"""What "Check my answer" looks for in each practice (pN-k) and homework (hN-k) task.

A rule is (what to do, test, how many):
- a CSS selector: at least that many elements on the page the browser builds,
- /regex/flags on his code: at least that many matches,
- "any:sel1,sel2,...": at least that many of these selectors find something.
How many = 0 means "must not be there". Kids write their own words, so rules check the
structure the task asks for, never the exact text of the model answer.
test_answers.py checks that every model answer passes its rules and the start code does not.
"""

SKELETON = [
    ("Start with `<!DOCTYPE html>`", r"/<!doctype html>/i", 1),
    ("`<html>` opens and closes", r"/<html[\s\S]*<\/html>/i", 1),
    ("A `<body>` that opens and closes", r"/<body[\s\S]*<\/body>/i", 1),
]
BOXES = ("Page boxes: `header`, `nav`, `main`, `footer`", "any:header,nav,main,footer", 4)
NO_EMPTY_ALT = 'img[alt]:not([alt=""])'


def title(text):
    return (f"The title is `{text}`", rf"/<title>\s*{text}\s*<\/title>/i", 1)


def button(text):
    return (f"A `{text}` button", rf"/<button[^>]*>\s*{text}/i", 1)


def labels_match(n):
    return ("Every label's `for` is the same as its box's `id`", r'/for="([^"]+)"[\s\S]*?id="\1"|id="([^"]+)"[\s\S]*?for="\2"/', n)


def menu(n):
    return (f"A menu with {n} links to your `.html` pages", 'a[href$=".html"]', n)


SAME_NAME = ("Radio buttons share one `name`, so only one is picked", r'/name="([^"]+)"[\s\S]*?name="\1"/', 1)
HOME = ("Home goes to `index.html`", 'a[href="index.html"]', 1)

CHECKS = {
    # 1. What is HTML?
    "p1-1": [("A big `h1` title with your name", r"/<h1[^>]*>[^<]*\w/i", 1),
             ("A `p` paragraph", "p", 1),
             ("Your age as a number, like 8", r"/\d/", 1)],
    "p1-2": [("All 6 headings: `h1` to `h6`", "any:h1,h2,h3,h4,h5,h6", 6),
             ("Stairs: `h1` first, `h6` last", r"/<h1[\s\S]*<h2[\s\S]*<h3[\s\S]*<h4[\s\S]*<h5[\s\S]*<h6/i", 1)],
    "p1-3": [("The `h1` closes with `</h1>`", r"/<h1>[^<]*<\/h1>/i", 1),
             ("`</p>` ends with `>`", r"/<\/p>/i", 1),
             ("The `h2` closes with `</h2>`", r"/<h2>[^<]*<\/h2>/i", 1)],
    "p1-4": SKELETON + [title("About Me"), ("An `h1` in the body", "body h1", 1), ("A `p` in the body", "body p", 1)],
    "p1-5": [("One `h1`", "h1", 1),
             ("Two `h2` parts: \"What it eats\" and \"Where it lives\"", r"/<h2[^>]*>\s*What it eats[\s\S]*<h2[^>]*>\s*Where it lives/i", 1),
             ("A `p` under each `h2`", "h2 + p", 2),
             ("A comment `<!-- -->` above each part", r"/<!--[\s\S]*?-->\s*<h2/", 2)],
    "h1-1": [("An `h1` title", "h1", 1), ("A `p` about your family", "p", 1),
             ("3 people: 3 sentences that end with a dot", r"/[.!?]/", 3)],
    "h1-2": [("All 6 headings: `h1` to `h6`", "any:h1,h2,h3,h4,h5,h6", 6),
             ("Upside down: `h6` first, `h1` last", r"/<h6[\s\S]*<h5[\s\S]*<h4[\s\S]*<h3[\s\S]*<h2[\s\S]*<h1/i", 1)],

    # 2. Formatting text
    "p2-1": [("The poem is in a `p`", "p", 1), ("3 `<br>` for 4 lines", "br", 3)],
    "p2-2": [("Important words in `strong`", "strong", 2), ("A feeling word in `em`", "em", 1)],
    "p2-3": [("A `<br>` new line, not `</br>`", r"/<\/br>/i", 0),
             ("`em` closes before `strong`", "strong > em", 1),
             ("The 2 in H2O goes down: `sub`, not `sup`", "sup", 0),
             ("H<sub>2</sub>O uses `sub`", "sub", 1)],
    "p2-4": [("The old price is crossed out: `<del>20$</del>`", r"/<del[^>]*>[^<]*20/i", 1),
             ("The new price is highlighted: `<mark>15$</mark>`", r"/<mark[^>]*>[^<]*15/i", 1),
             ("5² written as `5<sup>2</sup>`", r"/5\s*<sup>\s*2\s*<\/sup>/i", 1)],
    "p2-5": [("An `h1`", "h1", 1), ("4 facts", "p, li", 4),
             ("5 different tags from today", "any:strong,em,b,i,u,mark,del,ins,sub,sup,small,br,hr", 5),
             ("A line across: `<hr>`", "hr", 1),
             ("A copyright line: `&copy;`", r"/&copy;|©/", 1)],
    "h2-1": [("The poem is in a `p`", "p", 1), ("`<br>` at the end of each line", "br", 3)],
    "h2-2": [("3 sentences", r"/[.!?]/", 3), ("2 important words in `strong`", "strong", 2),
             ("1 word in `em`", "em", 1), ("An `<hr>` at the end", r"/<hr[^>]*>\s*$/i", 1)],

    # 3. Lists
    "p3-1": [("A dots list: `ul`", "ul", 1), ("4 things: 4 `li`", "ul > li", 4)],
    "p3-2": [("A numbers list: `ol`", "ol", 1), ("5 items: 5 `li`", "ol > li", 5),
             ("Number 1 is `strong`", "ol > li:first-child strong", 1)],
    "p3-3": [("Every animal is in its own `<li>`", "ul > li", 3), ("`</ul>` ends with `>`", r"/<\/ul>/i", 1)],
    "p3-4": [("Pets and Wild animals each get a small list", "ul > li > ul", 2),
             ("4 animals in the small lists", "li > ul > li", 4)],
    "p3-5": [("An `h1` with a food name", "h1", 1),
             ("An `h2` \"You need\", then an `h2` \"Steps\"", r"/<h2[^>]*>\s*You need[\s\S]*<h2[^>]*>\s*Steps/i", 1),
             ("A dots list of things you need", "ul > li", 2), ("A numbers list of 4 steps", "ol > li", 4)],
    "h3-1": [("A numbers list: `ol`", "ol", 1), ("5 things: 5 `li`", "ol > li", 5)],
    "h3-2": [("A dots list of people", "ul", 1), ("A small list under each person", "ul > li > ul", 2),
             ("2 things each person likes", "li > ul > li", 4)],

    # 4. Practice day: About me
    "p4-1": SKELETON + [title("About Me"), ("An `h1` with your name", "body h1", 1)],
    "p4-2": [("2 paragraphs about you", "p", 2), ("Your age in `strong`", r"/<strong[^>]*>[^<]*\d/i", 1),
             ("One word in `em`", "em", 1), ("Then an `<hr>`", "p ~ hr", 1)],
    "p4-3": [("Only one `h1`", "h1 ~ h1", 0), ("\"I am 9\" is a `p`", r"/<p>\s*I am 9/i", 1),
             ("Dogs is in an `<li>`", "li", 2), ("The body closes: `</body>`", r"/<\/body>/i", 1)],
    "p4-4": [("2 `h2` parts", "h2", 2), ("A dots list of 3 favorite things", "ul > li", 3),
             ("A numbers list for your top 3", "ol > li", 3)],
    "p4-5": SKELETON + [("An `h1` with your name", "h1", 1), ("About you: a `p` with `strong`", "p strong", 1),
                        ("...and `em`", "p em", 1), ("Favorite things: a dots list", "ul > li", 3),
                        ("Top 3: a numbers list", "ol > li", 3), ("An `<hr>` between parts", "hr", 2),
                        ("A fun fact with `sub` or `sup`", "sub, sup", 1)],
    "h4-1": SKELETON + [("A `<title>`", "title", 1), ("An `h1` with your name", "h1", 1),
                        ("Favorite things: a dots list", "ul > li", 3), ("Top 3: a numbers list", "ol > li", 3)],
    "h4-2": [("An `h2` \"My family\"", r"/<h2[^>]*>\s*My family/i", 1), ("A list of people", "ul > li, ol > li", 2),
             ("Each person has a small list", "li > ul, li > ol", 2)],

    # 5. Links
    "p5-1": [("A link to Wikipedia", 'a[href*="wikipedia.org"]', 1), ("The address starts with `https://`", 'a[href^="https://"]', 1),
             ("The link says \"Learn everything\"", r"/>\s*Learn everything\s*<\/a>/i", 1),
             ("Opens in a new tab: `target=\"_blank\"`", 'a[target="_blank"]', 1)],
    "p5-2": [("The sentence is in a `p`", r"/<p[^>]*>\s*I like space pictures from/i", 1),
             ("Only \"NASA\" is the link", r"/<a[^>]*>\s*NASA\s*<\/a>/i", 1),
             ("It goes to nasa.gov", 'p a[href*="nasa.gov"]', 1)],
    "p5-3": [("The Wikipedia link closes with `</a>`", r"/Wikipedia\s*<\/a>/i", 1),
             ("Quotes and `https://` in the Wikipedia address", 'a[href^="https://"][href*="wikipedia.org"]', 1),
             ("`_blank` starts with `_`", 'a[target="blank"]', 0), ("Both links open in a new tab", 'a[target="_blank"]', 2)],
    "p5-4": [("A dots list", "ul > li", 3), ("A link in every item", "li > a[href]", 3),
             ("Wikipedia, NASA and YouTube", 'any:a[href*="wikipedia"],a[href*="nasa"],a[href*="youtube"]', 3),
             ("Every link has a `title`", "a[title]", 3)],
    "p5-5": [("An `h1`", "h1", 1), ("A `p`", "p", 1), ("A numbers list of 3 animals", "ol > li", 3),
             ("Each animal links to its Wikipedia page", 'ol > li > a[href*="wikipedia.org/wiki/"]', 3)],
    "h5-1": [("3 links", "a[href]", 3), ("Real addresses that start with `https://`", 'a[href^="http"]', 3),
             ("Each one opens in a new tab", 'a[target="_blank"]', 3)],
    "h5-2": [("2 sentences in `p`", "p", 2), ("One link inside each sentence", "p a[href]", 2)],

    # 6. VS Code and many pages
    "p6-1": SKELETON + [title("Home"), ("An `h1` in the body", "body h1", 1), ("A `p` in the body", "body p", 1)],
    "p6-2": SKELETON + [title("Hobbies"), ("An `h1`", "h1", 1), ("A list of 3 hobbies", "li", 3)],
    "p6-3": [HOME, ("Hobbies goes to `hobbies.html`", 'a[href="hobbies.html"]', 1),
             ("Pets goes to `pets.html`", 'a[href="pets.html"]', 1)],
    "p6-4": [HOME, ("Hobbies goes to `hobbies.html`", 'a[href="hobbies.html"]', 1),
             ("The menu is at the top, before the `h1`", "a[href] ~ h1", 1)],
    "p6-5": SKELETON + [menu(3), HOME, ("An `h1`", "h1", 1)],
    "h6-1": SKELETON + [title("Home"), menu(3), HOME, ("An `h1`", "h1", 1)],
    "h6-2": [("A numbers list of 3 hobbies", "ol > li", 3), ("A link to a website", 'a[href^="http"]', 1)],

    # 7. Images
    "p7-1": [("The puppy picture: id 237", 'img[src*="picsum.photos/id/237"]', 1),
             ("`alt` words that describe it", NO_EMPTY_ALT, 1)],
    "p7-2": [("An `h2` \"Wild animals\"", r"/<h2[^>]*>\s*Wild animals/i", 1),
             ("Lioness 1074, leopard 219, walruses 1084", 'any:img[src*="/id/1074/"],img[src*="/id/219/"],img[src*="/id/1084/"]', 3),
             ("All 3 with `width=\"200\"`", 'img[width="200"]', 3), ("Every picture has `alt`", NO_EMPTY_ALT, 3)],
    "p7-3": [("`src`, not `scr`", "img[scr]", 0), ("No `</img>`: img never closes", r"/<\/img>/i", 0),
             ("Both pictures have `alt`", NO_EMPTY_ALT, 2)],
    "p7-4": [("A link to the leopard page", 'a[href*="wikipedia.org/wiki/Leopard"]', 1),
             ("The picture is inside the link", "a > img", 1), ("Opens in a new tab", 'a[target="_blank"]', 1)],
    "p7-5": [("3 `h2` names", "h2", 3), ("3 pictures with `width=\"200\"`", 'img[width="200"]', 3),
             ("Every picture has `alt`", NO_EMPTY_ALT, 3),
             ("Each picture is a link to Wikipedia", 'a[href*="wikipedia.org"] > img', 3), ("A `p` fact for each", "p", 3)],
    "h7-1": [("A picture from your `images` folder", 'img[src^="images/"]', 1), ("With `alt`", NO_EMPTY_ALT, 1),
             ("With `width`", "img[width]", 1)],
    "h7-2": [("2 pictures from picsum.photos", 'img[src*="picsum.photos"]', 2), ("Good `alt` words", NO_EMPTY_ALT, 2)],

    # 8. Tables
    "p8-1": [("A table with `border=\"1\"`", 'table[border="1"]', 1), ("2 rows", "tr", 2),
             ("A name and an age in each row", "tr > td:nth-child(2)", 2)],
    "p8-2": [("Title cells: Animal, Name, Age", r"/<th[^>]*>\s*Animal[\s\S]*<th[^>]*>\s*Name[\s\S]*<th[^>]*>\s*Age/i", 1),
             ("3 rows of pets", "tr:has(td)", 3), ("`border=\"1\"`", "table[border]", 1)],
    "p8-3": [("Name and Goals are title cells: `th`", "th", 2), ("The first row closes: `</tr>`", "tr:nth-of-type(3)", 0),
             ("3 is in a `td`, not a `tr`", r"/<td[^>]*>\s*3\s*<\/td>/i", 1)],
    "p8-4": [("Title cells: x, 1, 2, 3", "tr:first-child > th", 4),
             ("Row of 2: 2, 4, 6", r"/<td[^>]*>\s*2\s*<\/td>\s*<td[^>]*>\s*4\s*<\/td>\s*<td[^>]*>\s*6\s*<\/td>/i", 1),
             ("Row of 3: 3, 6, 9", r"/<td[^>]*>\s*3\s*<\/td>\s*<td[^>]*>\s*6\s*<\/td>\s*<td[^>]*>\s*9\s*<\/td>/i", 1)],
    "p8-5": [("Title cells: Day, Morning, Evening", "th", 3),
             ("Monday to Saturday", r"/Monday[\s\S]*Tuesday[\s\S]*Wednesday[\s\S]*Thursday[\s\S]*Friday[\s\S]*Saturday/i", 1),
             ("6 rows of days", "tr:has(td)", 6), ("\"Fun day!\" with `colspan=\"2\"`", 'td[colspan="2"]', 1)],
    "h8-1": [("Title cells: Food, Taste, Score", r"/<th[^>]*>\s*Food[\s\S]*<th[^>]*>\s*Taste[\s\S]*<th[^>]*>\s*Score/i", 1),
             ("4 foods", "tr:has(td)", 4)],
    "h8-2": [("`thead` and `tbody`", r"/<thead[\s\S]*<\/thead>\s*<tbody/i", 1),
             ("Title cells: Team, Played, Won", "thead th", 3), ("3 teams", "tbody tr", 3)],

    # 9. YouTube, maps, video and sound
    "p9-1": [("The YouTube video jNQXAC9IVRw", 'iframe[src*="youtube.com/embed/jNQXAC9IVRw"]', 1),
             ("`width=\"400\"`", 'iframe[width="400"]', 1), ("`height=\"225\"`", 'iframe[height="225"]', 1)],
    "p9-2": [("An `h2`", "h2", 1), ("A Google map of your city", 'iframe[src*="google.com/maps"]', 1)],
    "p9-3": [("The video closes: `</video>`", r"/<\/video>/i", 1), ("The video has `controls`", "video[controls]", 1),
             ("The sound has `controls`, not control", "audio[controls]", 1)],
    "p9-4": [("An `h1`", "h1", 1), ("A `p` with a fact", "p", 1),
             ("The T-Rex roar", 'audio[src*="t-rex-roar"]', 1), ("With `controls`", "audio[controls]", 1)],
    "p9-5": [("3 `h2` parts", "h2", 3), ("A `p` under each part", "p", 3),
             ("A YouTube video", 'iframe[src*="youtube.com/embed/"]', 1), ("A map", 'iframe[src*="google.com/maps"]', 1),
             ("The flower video with `controls`", 'video[src*="flower"][controls]', 1)],
    "h9-1": [("A YouTube video", 'iframe[src*="youtube.com/embed/"]', 1), ("With a `title`", "iframe[title]", 1)],
    "h9-2": [("An `h2` that says why", "h2", 1), ("A map under it", 'h2 ~ iframe[src*="google.com/maps"]', 1)],

    # 10. Practice day: my website grows
    "p10-1": [menu(3), HOME],
    "p10-2": [menu(3), ("An `h1`", "h1", 1), ("A picture with `alt` and `width`", 'img[alt]:not([alt=""])[width]', 1),
              ("A welcome `p`", "p", 1), ("A list", "li", 2)],
    "p10-3": [("Hobbies goes to `hobbies.html`", 'a[href="hobbies.html"]', 1), ("The picture has `alt`", NO_EMPTY_ALT, 1),
              ("`strong` closes", r"/<\/strong>/i", 1), ("The list closes: `</ul>`", r"/<\/ul>/i", 1)],
    "p10-4": [menu(3), ("An `h1`", "h1", 1), ("A table with title cells", "table th", 1),
              ("3 hobbies in the table", "tr:has(td)", 3), ("A YouTube video", 'iframe[src*="youtube.com/embed/"]', 1)],
    "p10-5": [menu(3), ("An `h1`", "h1", 1), ("2 pictures with `alt`", NO_EMPTY_ALT, 2),
              ("A numbers list of 3 facts", "ol > li", 3)],
    "h10-1": [menu(3), ("An `h1`", "h1", 1), ("A picture with `alt` and `width`", 'img[alt]:not([alt=""])[width]', 1),
              ("A welcome `p`", "p", 1), ("A list", "li", 2)],
    "h10-2": [menu(3), ("An `h1`", "h1", 1), ("A table with title cells", "table th", 1),
              ("3 hobbies in the table", "tr:has(td)", 3), ("A YouTube video", 'iframe[src*="youtube.com/embed/"]', 1)],

    # 11. Page structure
    "p11-1": [("A `div` painted `lightgreen`", 'div[style*="lightgreen"]', 1), ("An `h2` inside", "div h2", 1),
              ("A `p` inside", "div p", 1)],
    "p11-2": [("A sentence in a `p`", "p", 1), ("A `span` painted yellow", 'p span[style*="yellow"]', 1),
              ("2 words in the `span`", r"/<span[^>]*>\s*\S+\s+\S+/i", 1)],
    "p11-3": [("The header closes: `</header>`", r"/<\/header>/i", 1), ("Only one `main`", "main ~ main", 0),
              ("`</footer>` is spelled right", r"/<\/footer>/i", 1)],
    "p11-4": [("`header` with the `h1`", "header h1", 1), ("`nav` with the 2 links", "nav a", 2),
              ("`main` with 2 `section`", "main > section", 2),
              ("`footer` with the copyright", r"/<footer[\s\S]*(&copy;|©)[\s\S]*<\/footer>/i", 1)],
    "p11-5": [BOXES, ("The header has a color", 'header[style*="background"]', 1), ("`main` with 3 `section`", "main > section", 3),
              ("Subjects as a list", "section ul, section ol", 1), ("A timetable table", "section table", 1)],
    "h11-1": [BOXES, ("The `h1` is in the header", "header h1", 1), ("The links are in the nav", "nav a", 1)],
    "h11-2": [("A `main`", "main", 1), ("Each hobby in its own `section`", "main section", 2),
              ("An `h2` in each section", "section h2", 2)],

    # 12. Forms 1
    "p12-1": [("A `form`", "form", 1), ("A label \"Favorite food\"", r"/<label[^>]*>\s*Favorite food/i", 1),
              ("A text box", 'input[type="text"]', 1), labels_match(1), button("Send")],
    "p12-2": [("An email box", 'form input[type="email"]', 1), ("A password box", 'form input[type="password"]', 1),
              ("A label for each box", "label", 2), labels_match(2), button("Log in")],
    "p12-3": [("The name box has `id=\"name\"`", "input#name", 1), ("No `</input>`: input never closes", r"/<\/input>/i", 0),
              ("The password box hides the letters", 'input#pw[type="password"]', 1)],
    "p12-4": [("A label \"How old are you?\"", r"/<label[^>]*>\s*How old are you\?/i", 1), ("A number box", 'input[type="number"]', 1),
              ("From 1 to 100", 'input[min="1"][max="100"]', 1), ("Placeholder \"Your age\"", 'input[placeholder="Your age"]', 1),
              ("`required`", "input[required]", 1)],
    "p12-5": [("Name is `required`", 'input[type="text"][required]', 1), ("An email box", 'input[type="email"]', 1),
              ("A password box", 'input[type="password"]', 1), ("A birthday date box", 'input[type="date"]', 1),
              ("A label for every box", "label", 4), labels_match(4), ("A placeholder", "input[placeholder]", 1), button("Join")],
    "h12-1": [("A name box", 'input[type="text"]', 1), ("\"How many?\" from 1 to 5", 'input[type="number"][min="1"][max="5"]', 1),
              ("A label for each box", "label", 2), button("Order")],
    "h12-2": [("Name, email and date boxes", 'any:input[type="text"],input[type="email"],input[type="date"]', 3),
              ("All 3 are `required`", "input[required]", 3), ("A label for each box", "label", 3)],

    # 13. Forms 2
    "p13-1": [("3 checkboxes", 'input[type="checkbox"]', 3), ("Cats, dogs and fish", r"/I like cats[\s\S]*I like dogs[\s\S]*I like fish/i", 1),
              labels_match(3)],
    "p13-2": [("2 radio buttons", 'input[type="radio"]', 2), SAME_NAME, ("A label for each", "label", 2)],
    "p13-3": [("Both radios have `name=\"drink\"`", 'input[type="radio"][name="drink"]', 2),
              ("A real `<select>`, not an input", 'input[type="select"]', 0), ("The option is in a `select`", "select > option", 1),
              ("The textarea closes", r"/<\/textarea>/i", 1)],
    "p13-4": [("A label \"Favorite color\"", r"/<label[^>]*>\s*Favorite color/i", 1), ("5 colors", "select > option", 5),
              ("Blue is `selected`", r"/<option[^>]*selected[^>]*>\s*Blue/i", 1)],
    "p13-5": [("A name box", 'form input[type="text"]', 1), ("3 size radios", 'input[type="radio"]', 3), SAME_NAME,
              ("3 topping checkboxes", 'input[type="checkbox"]', 3), ("A drink drop-down", "select > option", 2),
              ("A message box", "form textarea", 1), button("Order")],
    "h13-1": [("The question \"What is 2 + 2?\"", r"/2\s*\+\s*2/", 1), ("3 radio answers", 'input[type="radio"]', 3), SAME_NAME,
              ("A label for each", "label", 3), button("Check")],
    "h13-2": [("A drop-down of 4 countries", "select > option", 4), ("3 checkboxes", 'input[type="checkbox"]', 3),
              ("A textarea \"Why?\"", r"/Why\?[\s\S]*<textarea|<textarea[\s\S]*Why\?/i", 1)],

    # 14. Practice day: Write to me
    "p14-1": [("3 links", "a[href]", 3), HOME, ("Hobbies goes to `hobbies.html`", 'a[href="hobbies.html"]', 1),
              ("\"Write to me\" goes to `contact.html`", r'/<a[^>]*href="contact\.html"[^>]*>\s*Write to me/i', 1)],
    "p14-2": [("A name box that is `required`", "form input[required]", 1), ("An email box", 'form input[type="email"]', 1),
              ("A label for each box", "label", 2), labels_match(2), button("Send")],
    "p14-3": [("The email label has `for=\"email\"`", 'label[for="email"]', 1),
              ("Both radios have `name=\"found\"`", 'input[type="radio"][name="found"]', 2),
              ("The textarea closes", r"/<\/textarea>/i", 1), ("`main` closes", r"/<\/main>/i", 1)],
    "p14-4": [("A radio question with 2 answers", 'input[type="radio"]', 2), SAME_NAME,
              ("A drop-down with 3 choices", "select > option", 3), ("A checkbox", 'input[type="checkbox"]', 1)],
    "p14-5": [BOXES, ("The menu has `contact.html`", 'nav a[href="contact.html"]', 1), ("The form is in `main`", "main form", 1),
              ("Every kind of box: text, email, radio, checkbox, select, textarea",
               'any:input[type="text"],input[type="email"],input[type="radio"],input[type="checkbox"],select,textarea', 6),
              ("A button", "form button", 1)],
    "h14-1": [BOXES, ("The menu has `contact.html`", 'nav a[href="contact.html"]', 1), ("The form is in `main`", "main form", 1),
              ("Every kind of box: text, email, radio, checkbox, select, textarea",
               'any:input[type="text"],input[type="email"],input[type="radio"],input[type="checkbox"],select,textarea', 6),
              ("A button", "form button", 1)],
    "h14-2": [("The question \"How many stars for my site?\"", r"/How many stars/i", 1),
              ("A number box from 1 to 5", 'input[type="number"][min="1"][max="5"]', 1), ("A label", "label", 1)],

    # 15. Review game and test
    "p15-1": SKELETON + [title("Test"), ("An `h1`", "h1", 1), ("A `p` with one `strong` word", "p strong", 1)],
    "p15-2": [("A numbers list of 3 planets", "ol > li", 3), ("Each planet links to Wikipedia", 'li > a[href*="wikipedia.org"]', 3),
              ("Each opens in a new tab", 'a[target="_blank"]', 3)],
    "p15-3": [("The header closes", r"/<\/header>/i", 1), ("The picture has `alt`", NO_EMPTY_ALT, 1),
              ("Water is H<sub>2</sub>O: `sub`", "sub", 1), ("The table has `border=\"1\"`", "table[border]", 1),
              ("The footer opens and closes", r"/<footer[\s\S]*<\/footer>/i", 1)],
    "p15-4": [("Title cells: Animal and Legs", r"/<th[^>]*>\s*Animal[\s\S]*<th[^>]*>\s*Legs/i", 1),
              ("3 animals", "tr:has(td)", 3)],
    "p15-5": [("A `form`", "form", 1), ("A name box that is `required`", "form input[required]", 1),
              ("A radio question with 2 answers", 'input[type="radio"]', 2), SAME_NAME,
              ("A drop-down with 3 choices", "select > option", 3), ("A button", "form button", 1)],
    "h15-1": [("A dots list of 10 tags", "ul > li", 10)],
    "h15-2": [("A table with title cells", "table th", 1),
              ("`br`, `hr`, `img` and `input`", r"/<td[^>]*>\s*(&lt;)?\s*(br|hr|img|input)\b/i", 4),
              ("What each one does", "tr:has(td + td)", 4)],

    # 16. Final project
    "p16-1": SKELETON + [BOXES, ("A nav with 4 links", "nav a", 4), ("`main` with 2 `section`", "main > section", 2)],
    "p16-2": [menu(2), ("A table with title cells", "table th", 1), ("A video", "iframe, video", 1)],
    "p16-3": [("The header closes", r"/<\/header>/i", 1), ("Pets goes to `pets.html`", 'a[href="pets.html"]', 1),
              ("The picture has `alt`", NO_EMPTY_ALT, 1), ("`strong` closes", r"/<\/strong>/i", 1),
              ("Pizza is in an `<li>`", "ol > li", 3)],
    "p16-4": [("Labels with `for`", "label[for]", 1), labels_match(1), SAME_NAME, ("The form has a button", "form button", 1)],
    "p16-5": [("Say which page", r"/My favorite page is\s*\w/i", 1), ("Say why, with \"because\"", r"/because/i", 1)],
    "h16-1": SKELETON + [BOXES, ("A nav with 4 links", "nav a", 4), ("`main` with 2 `section`", "main > section", 2)],
    "h16-2": [("A numbers list of 3 things", "ol > li", 3)],
}

NOT_TODAY = {"html", "head", "body", "title", "meta"}  # every page has these


def idea_checks(today, tags):
    """Homework task 3: his own page, built with what he knows, and something from today if it has new tags."""
    today = [t for t in today if t not in NOT_TODAY]
    known = [t for t in tags if t not in NOT_TODAY]
    rules = [("Use 3 different tags you know", "any:" + ",".join(known), 3),
             ("Write your own words", r"/>[^<]*[a-zA-Z]{3}/", 2)]
    if today:
        rules.insert(0, ("Use something new from today: " + ", ".join(f"`{t}`" for t in today), "any:" + ",".join(today), 1))
    return rules


def checks_for(key):
    rules = CHECKS.get(key)
    assert rules, f"answer_checks: no rules for task {key}"
    for label, rule, n in rules:
        assert isinstance(n, int) and n >= 0, f"answer_checks {key}: bad count for {label!r}"
        assert not rule.startswith("/") or rule.rindex("/") > 0, f"answer_checks {key}: bad regex {rule!r}"
    return rules
