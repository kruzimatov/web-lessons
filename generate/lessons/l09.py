YOUTUBE = '<iframe width="400" height="225" src="https://www.youtube.com/embed/jNQXAC9IVRw" title="The first YouTube video" allowfullscreen></iframe>'
MAP = '<iframe width="400" height="300" src="https://www.google.com/maps?q=Tashkent&output=embed" title="Map of Tashkent"></iframe>'
VIDEO = '<video src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4" width="400" controls></video>'
AUDIO = '<audio src="https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3" controls></audio>'

LESSON = {
    "n": 9,
    "week": 2,
    "folder": "week2/lesson09_video_audio_maps",
    "title": "YouTube, maps, video and sound",
    "goal": "Today you put a YouTube video, a map, a video and a dinosaur roar on your page.",
    "sandbox": "allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox allow-presentation",
    "cheats": [
        ("<iframe src=\"https://www.youtube.com/embed/...\"></iframe>", "A YouTube video (Share, Embed)"),
        ("src=\"https://www.google.com/maps?q=Paris&output=embed\"", "A map in an iframe"),
        ("<video src=\"film.mp4\" controls></video>", "A video file"),
        ("<audio src=\"roar.mp3\" controls></audio>", "A sound file"),
        ("controls", "Shows the play button"),
    ],
    "review": [
        ("quiz", "Which tag makes one row in a table?", ["`<td>`", "`<tr>`", "`<th>`"], 1),
        ("quiz", "Which tag makes a bold title cell?", ["`<th>`", "`<td>`", "`<b>`"], 0),
        ("quiz", "One cell 2 columns wide:", ["`colspan=\"2\"`", "`rowspan=\"2\"`", "`width=\"2\"`"], 0),
    ],
    "blocks": [
        ("h", "Part 1: YouTube videos"),
        ("say", "An `<iframe>` is a **window** inside your page that shows another website. YouTube gives you one for every video."),
        ("anim", "embed_window", "iframe is a window to another website. video and audio play files."),
        ("code", YOUTUBE, "The very first YouTube video, from 2005"),
        ("table", ["Part", "Meaning"], [
            ["`src`", "The video address. It has `/embed/` in it"],
            ["`width`, `height`", "The size of the window"],
            ["`title`", "Says what is inside, for people who cannot see"],
            ["`allowfullscreen`", "Lets you watch it on the full screen"],
        ]),
        ("steps", [
            "On YouTube, open a video and click **Share**",
            "Click **Embed**",
            "Click **Copy** and paste the code into your page",
        ]),
        ("uz", "iframe bu sahifa ichidagi oyna: unda boshqa sayt ko'rinadi."),
        ("try", "Make the video window bigger: `width=\"560\"` and `height=\"315\"`. Press play!", YOUTUBE),
        ("quiz", "Which tag shows a YouTube video on your page?", ["`<video>`", "`<iframe>`", "`<youtube>`"], 1),

        ("h", "Part 2: Maps"),
        ("say", "An iframe can show a Google map too. Put the name of a place after `q=`."),
        ("code", MAP, "A map of Tashkent"),
        ("try", "Change Tashkent to your city, or to Paris, Tokyo or London.", MAP),
        ("uz", "q= dan keyin shahar nomini yozing: xarita o'sha joyni ko'rsatadi."),
        ("quiz", "In the map address, where do you write the place?", ["After `q=`", "After `width=`", "In the `title`"], 0),

        ("h", "Part 3: Video and sound files"),
        ("say", "For a video FILE (not YouTube) use `<video>`. For sound use `<audio>`. Add `controls` to get the play button."),
        ("code", VIDEO, "A video file with a play button"),
        ("code", AUDIO, "A T-Rex roar!"),
        ("table", ["Tag", "Plays", "Need"], [
            ["`<video>`", "A video file (.mp4)", "`src`, `controls`"],
            ["`<audio>`", "A sound file (.mp3)", "`src`, `controls`"],
        ]),
        ("try", "Press play on both. Then delete `controls` from the audio. What happens?", VIDEO + "\n<br>\n" + AUDIO),
        ("quiz", "What gives you the play button?", ["`play`", "`controls`", "`button`"], 1),
    ],
    "mistakes": [
        "Copying the normal YouTube link. The iframe needs the `/embed/` link from Share, Embed",
        "Forgetting `controls`: the video is there but you cannot press play",
        "Forgetting `</iframe>`, `</video>` or `</audio>`. These tags DO need closing",
        "No internet: videos and maps need the internet to load",
    ],
    "practice": [
        {
            "task": "Show the first YouTube video (code `jNQXAC9IVRw`) with width 400 and height 225.",
            "hints": ["Look at the YouTube code in the lesson.", "The address is `https://www.youtube.com/embed/jNQXAC9IVRw`."],
            "start": "",
            "answer": YOUTUBE,
        },
        {
            "task": "\"Where I live\": an h2 and a map of your city.",
            "hints": ["Copy the map code from the lesson.", "Change the city after `q=`."],
            "start": "<h2>Where I live</h2>\n",
            "answer": "<h2>Where I live</h2>\n" + MAP,
        },
        {
            "task": "There are 3 mistakes. Fix them.",
            "hints": ["What gives the play button? Does video close?", "Video needs `controls` and `</video>`. Audio: `control` should be `controls`."],
            "start": "<video src=\"https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4\" width=\"400\">\n<audio src=\"https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3\" control></audio>",
            "answer": VIDEO + "\n" + AUDIO,
        },
        {
            "task": "\"Dinosaur page\": an h1, a p with a fact, and the T-Rex roar with controls.",
            "hints": ["h1, p, then the audio code.", "Do not forget `controls`."],
            "start": "",
            "answer": "<h1>Dinosaurs</h1>\n<p>The T-Rex lived more than 66 million years ago.</p>\n" + AUDIO,
        },
        {
            "task": "\"My media page\": an h1, then 3 parts with h2: a YouTube video, a map of a place you want to visit, and the flower video. One p under each h2.",
            "hints": ["3 parts: h2, p, then the media code.", "YouTube, map, video. Copy each from the lesson."],
            "start": "<h1>My media page</h1>\n",
            "answer": "<h1>My media page</h1>\n<h2>A video</h2>\n<p>The first YouTube video.</p>\n" + YOUTUBE + "\n<h2>I want to visit</h2>\n<p>Tokyo looks fun.</p>\n" + MAP.replace("Tashkent", "Tokyo") + "\n<h2>Flowers</h2>\n<p>A flower opening.</p>\n" + VIDEO,
        },
    ],
    "homework": [
        {
            "task": "Find a YouTube video you like (ask a parent). Use Share, Embed and copy the iframe here.",
            "answer": '<iframe width="560" height="315" src="https://www.youtube.com/embed/..." title="My favorite video" allowfullscreen></iframe>',
        },
        {
            "task": "A map of a place you want to visit, with an h2 above it saying why.",
            "answer": "<h2>I want to see Paris, the Eiffel Tower is there!</h2>\n" + MAP.replace("Tashkent", "Paris"),
        },
    ],
}
