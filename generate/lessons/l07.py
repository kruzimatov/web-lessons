PUPPY = "https://picsum.photos/id/237/400/300"
PUG = "https://picsum.photos/id/1025/400/300"
LION = "https://picsum.photos/id/1074/400/300"
WALRUS = "https://picsum.photos/id/1084/400/300"
LEOPARD = "https://picsum.photos/id/219/400/300"
DEER = "https://picsum.photos/id/1003/400/300"
BIRD = "https://picsum.photos/id/1024/400/300"

LESSON = {
    "n": 7,
    "week": 2,
    "folder": "week2/lesson07_images",
    "title": "Images",
    "goal": "Today you put pictures on your pages, change their size and make a picture you can click.",
    "cheats": [
        ("<img src=\"dog.jpg\" alt=\"A dog\">", "A picture. No closing tag"),
        ("alt=\"A dog\"", "Words that describe the picture"),
        ("width=\"200\"", "Picture width in pixels"),
        ("src=\"images/cat.jpg\"", "A picture in your images folder"),
        ("<a href=\"...\"><img ...></a>", "A picture you can click"),
    ],
    "review": [
        ("quiz", "What is the home page file called?", ["`index.html`", "`home.html`", "`start.html`"], 0),
        ("quiz", "How do you link to your own page `pets.html`?", ["`href=\"pets.html\"`", "`href=\"https://pets\"`", "`src=\"pets.html\"`"], 0),
        ("quiz", "You changed the code but Chrome shows the old page. Why?", ["You did not save and refresh", "Chrome is broken", "HTML is too old"], 0),
    ],
    "blocks": [
        ("h", "Part 1: The img tag"),
        ("say", "Pictures make a page fun. The tag is `<img>`. It has **no closing tag**: the picture is the content."),
        ("anim", "image_frame", "`src` is the picture, `alt` is the words you see if it cannot load."),
        ("code", f"<img src=\"{PUPPY}\" alt=\"A black puppy\">", "A picture from the internet"),
        ("table", ["Part", "Meaning"], [
            ["`<img>`", "Image. No closing tag"],
            ["`src=\"...\"`", "Source: where the picture is"],
            ["`alt=\"...\"`", "Words that describe the picture, for people who cannot see it"],
        ]),
        ("uz", "src bu rasm manzili. alt bu rasm haqida so'z: rasm ochilmasa, shu yoziladi."),
        ("try", "Change the `src` number 237 to 1025. What animal is it now? Change the `alt` too.",
         f"<h2>My favorite animal</h2>\n<img src=\"{PUPPY}\" alt=\"A black puppy\">"),
        ("say", "Now break it on purpose: delete one letter from the `src`. What do you see instead of the picture? That is the `alt`!"),
        ("quiz", "What does `alt` do?", ["Makes the picture bigger", "Describes the picture in words", "Adds a link"], 1),

        ("h", "Part 2: Picture size"),
        ("say", "`width` makes a picture wider or smaller. The number is in **pixels**, tiny dots on the screen."),
        ("code", f"<img src=\"{LION}\" alt=\"A lioness\" width=\"150\">\n<img src=\"{LION}\" alt=\"A lioness\" width=\"300\">", "Same picture, two sizes"),
        ("say", "Use only `width`. The browser changes the height for you, so the picture is not squeezed."),
        ("try", "Make the 3 pictures the same size: all `width=\"200\"`.",
         f"<img src=\"{WALRUS}\" alt=\"Walruses on a beach\" width=\"120\">\n<img src=\"{LEOPARD}\" alt=\"A leopard on a road\" width=\"300\">\n<img src=\"{DEER}\" alt=\"A baby deer\">"),
        ("quiz", "Which one changes the size of a picture?", ["`alt=\"200\"`", "`width=\"200\"`", "`src=\"200\"`"], 1),

        ("h", "Part 3: Your own pictures, and pictures you can click"),
        ("say", "For your real website, put pictures in an `images` folder inside `my-website`. Then the `src` is the folder name, a `/`, and the file name."),
        ("code", "<img src=\"images/cat.jpg\" alt=\"My cat Momo\" width=\"300\">", "A picture from YOUR folder"),
        ("steps", [
            "In VS Code, make a new folder in `my-website`: `images`",
            "Ask a parent to help you save a photo into it, for example `cat.jpg`",
            "Write `<img src=\"images/cat.jpg\" alt=\"...\">`",
        ]),
        ("say", "Put an `<img>` inside an `<a>` and the picture becomes a link!"),
        ("code", f"<a href=\"https://en.wikipedia.org/wiki/Pug\" target=\"_blank\">\n  <img src=\"{PUG}\" alt=\"A pug in a blanket\" width=\"250\">\n</a>", "Click the picture to go to Wikipedia"),
        ("try", "Make the bird picture a link to `https://en.wikipedia.org/wiki/Bird`.",
         f"<img src=\"{BIRD}\" alt=\"A big bird flying\" width=\"250\">"),
        ("quiz", "Your picture `dog.png` is in the `images` folder. What is the src?", ["`src=\"dog.png\"`", "`src=\"images/dog.png\"`", "`src=\"images\"`"], 1),
    ],
    "mistakes": [
        "Writing `</img>`. `<img>` has no closing tag",
        "No `alt`. Every picture needs words that describe it",
        "Wrong file name: `Cat.JPG` and `cat.jpg` are different names",
        "Setting width AND a wrong height. The picture gets squeezed",
    ],
    "practice": [
        {
            "task": "Show the puppy picture with a good alt. Puppy: `https://picsum.photos/id/237/400/300`",
            "hints": ["`<img src=\"...\" alt=\"...\">`", "alt: what is in the picture? A black puppy."],
            "start": "",
            "answer": f"<img src=\"{PUPPY}\" alt=\"A black puppy\">",
        },
        {
            "task": "An h2 \"Wild animals\" and 3 pictures (lioness 1074, leopard 219, walruses 1084), all `width=\"200\"`. Change only the number in the address.",
            "hints": ["Change only the number: 1074, 219, 1084.", "Each one: `width=\"200\"`."],
            "start": "<h2>Wild animals</h2>\n",
            "answer": f"<h2>Wild animals</h2>\n<img src=\"{LION}\" alt=\"A lioness\" width=\"200\">\n<img src=\"{LEOPARD}\" alt=\"A leopard\" width=\"200\">\n<img src=\"{WALRUS}\" alt=\"Walruses\" width=\"200\">",
        },
        {
            "task": "There are 3 mistakes. Fix them.",
            "hints": ["Look at the spelling of src. Does img close? Does every picture have alt?", "`scr` should be `src`. Delete `</img>`. Add alt to the pug."],
            "start": f"<img scr=\"{DEER}\" alt=\"A baby deer\"></img>\n<img src=\"{PUG}\" width=\"200\">",
            "answer": f"<img src=\"{DEER}\" alt=\"A baby deer\">\n<img src=\"{PUG}\" alt=\"A pug\" width=\"200\">",
        },
        {
            "task": "Make the leopard picture a link to `https://en.wikipedia.org/wiki/Leopard`, opening in a new tab.",
            "hints": ["Put the `<img>` inside an `<a>`.", "`<a href=\"...\" target=\"_blank\"><img ...></a>`"],
            "start": f"<img src=\"{LEOPARD}\" alt=\"A leopard\" width=\"250\">",
            "answer": f"<a href=\"https://en.wikipedia.org/wiki/Leopard\" target=\"_blank\">\n  <img src=\"{LEOPARD}\" alt=\"A leopard\" width=\"250\">\n</a>",
        },
        {
            "task": "\"Animal cards\": for 3 animals, an h2 with the name, a picture (`width=\"200\"`) and a p with one fact. Make each picture a link to its Wikipedia page.",
            "hints": ["For each animal: h2, a with img inside, p.", "Copy one animal, then change the words 2 times."],
            "start": "<h1>Animal cards</h1>\n",
            "answer": f"<h1>Animal cards</h1>\n<h2>Lion</h2>\n<a href=\"https://en.wikipedia.org/wiki/Lion\" target=\"_blank\"><img src=\"{LION}\" alt=\"A lioness\" width=\"200\"></a>\n<p>Lions can sleep up to 20 hours a day.</p>\n<h2>Deer</h2>\n<a href=\"https://en.wikipedia.org/wiki/Deer\" target=\"_blank\"><img src=\"{DEER}\" alt=\"A baby deer\" width=\"200\"></a>\n<p>Baby deer have white spots.</p>\n<h2>Walrus</h2>\n<a href=\"https://en.wikipedia.org/wiki/Walrus\" target=\"_blank\"><img src=\"{WALRUS}\" alt=\"Walruses\" width=\"200\"></a>\n<p>Walruses use their tusks to climb.</p>",
        },
    ],
    "homework": [
        {
            "task": "Put an `images` folder in `my-website` with one photo (ask a parent). Show it on `index.html` with alt and width. Copy the img line here.",
            "answer": "<img src=\"images/me.jpg\" alt=\"Me at the park\" width=\"300\">",
        },
        {
            "task": "On `pets.html` (or your third page), add 2 pictures from picsum.photos with good alt words.",
            "answer": f"<img src=\"{PUPPY}\" alt=\"A black puppy\" width=\"250\">\n<img src=\"{PUG}\" alt=\"A pug in a blanket\" width=\"250\">",
        },
    ],
}
