SIMPLE = """<table border="1">
  <tr>
    <td>Monday</td>
    <td>School</td>
    <td>Football</td>
  </tr>
  <tr>
    <td>Tuesday</td>
    <td>School</td>
    <td>Chess</td>
  </tr>
</table>"""

WITH_HEAD = """<table border="1">
  <thead>
    <tr>
      <th>Day</th>
      <th>Morning</th>
      <th>Evening</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Monday</td>
      <td>School</td>
      <td>Football</td>
    </tr>
    <tr>
      <td>Tuesday</td>
      <td>School</td>
      <td>Chess</td>
    </tr>
  </tbody>
</table>"""

LESSON = {
    "n": 8,
    "week": 2,
    "folder": "week2/lesson08_tables",
    "title": "Tables",
    "goal": "Today you make tables: a timetable, a scoreboard and more.",
    "cheats": [
        ("<table border=\"1\">", "A table with lines"),
        ("<tr> ... </tr>", "One row"),
        ("<td>Monday</td>", "One cell"),
        ("<th>Day</th>", "A title cell, bold"),
        ("<thead>, <tbody>", "Top part, body part"),
        ("colspan=\"2\"", "Cell 2 columns wide"),
        ("rowspan=\"2\"", "Cell 2 rows tall"),
    ],
    "review": [
        ("quiz", "Which tag shows a picture?", ["`<pic>`", "`<img>`", "`<src>`"], 1),
        ("quiz", "What does `alt` do?", ["Describes the picture in words", "Makes it bigger", "Makes it a link"], 0),
        ("quiz", "Does `<img>` have a closing tag?", ["Yes, `</img>`", "No"], 1),
    ],
    "blocks": [
        ("h", "Part 1: Rows and cells"),
        ("say", "A **table** shows information in rows and columns, like a school timetable."),
        ("anim", "table_grid", "A table is built row by row, cell by cell."),
        ("table", ["Tag", "Means"], [
            ["`<table>`", "The whole table"],
            ["`<tr>`", "Table row: one line across"],
            ["`<td>`", "Table data: one cell (box)"],
        ]),
        ("uz", "tr bu qator. td bu bitta katak. Avval qator, keyin uning kataklari."),
        ("code", SIMPLE, "2 rows, 3 cells in each row. `border=\"1\"` shows the lines"),
        ("try", "Add a third row: Wednesday, School, Swimming.", SIMPLE),
        ("quiz", "Which tag makes a new row?", ["`<td>`", "`<tr>`", "`<table>`"], 1),

        ("h", "Part 2: Header cells"),
        ("say", "The first row usually has the **titles** of the columns. Use `<th>` instead of `<td>`: it is bold and centered."),
        ("code", WITH_HEAD, "`<thead>` holds the title row, `<tbody>` holds the rest"),
        ("table", ["Tag", "Means"], [
            ["`<th>`", "Table header: a title cell, bold"],
            ["`<thead>`", "The top part, with the title row"],
            ["`<tbody>`", "The body, with all other rows"],
        ]),
        ("try", "Make a scoreboard: columns Player and Goals, and 3 players.",
         "<table border=\"1\">\n  <thead>\n    <tr>\n      <th>Player</th>\n      <th>Goals</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>Ali</td>\n      <td>3</td>\n    </tr>\n  </tbody>\n</table>"),
        ("quiz", "Which tag makes a bold title cell?", ["`<th>`", "`<td>`", "`<title>`"], 0),

        ("h", "Part 3: Big cells"),
        ("say", "A cell can be wider than one column: `colspan=\"2\"`. Or taller than one row: `rowspan=\"2\"`."),
        ("code", "<table border=\"1\">\n  <tr>\n    <th>Day</th>\n    <th>Morning</th>\n    <th>Evening</th>\n  </tr>\n  <tr>\n    <td>Saturday</td>\n    <td colspan=\"2\">Fun day!</td>\n  </tr>\n</table>", "`colspan=\"2\"`: one cell, 2 columns wide"),
        ("uz", "colspan katakni eniga cho'zadi, rowspan bo'yiga."),
        ("try", "Add a Sunday row where one cell says \"Family day\" across 2 columns.",
         "<table border=\"1\">\n  <tr>\n    <th>Day</th>\n    <th>Morning</th>\n    <th>Evening</th>\n  </tr>\n  <tr>\n    <td>Saturday</td>\n    <td colspan=\"2\">Fun day!</td>\n  </tr>\n</table>"),
        ("quiz", "One cell 3 columns wide. What do you write?", ["`rowspan=\"3\"`", "`colspan=\"3\"`", "`width=\"3\"`"], 1),
    ],
    "mistakes": [
        "Writing `<td>` without a `<tr>` around it",
        "Rows with different numbers of cells: the table looks broken",
        "Forgetting `border=\"1\"`: the table has no lines and looks like plain text",
        "Using `<td>` for the title row instead of `<th>`",
    ],
    "practice": [
        {
            "task": "A table with 2 rows: your name and age, and a friend's name and age. Use `border=\"1\"`.",
            "hints": ["`<table border=\"1\">`, then 2 `<tr>`.", "Each row has 2 `<td>`: name and age."],
            "start": "",
            "answer": "<table border=\"1\">\n  <tr>\n    <td>Ali</td>\n    <td>8</td>\n  </tr>\n  <tr>\n    <td>Sara</td>\n    <td>9</td>\n  </tr>\n</table>",
        },
        {
            "task": "\"My pets\" table with title cells Animal, Name, Age and 3 rows.",
            "hints": ["Title row uses `<th>`.", "Animal, Name, Age: 3 cells in every row."],
            "start": "<h2>My pets</h2>\n",
            "answer": "<h2>My pets</h2>\n<table border=\"1\">\n  <thead>\n    <tr>\n      <th>Animal</th>\n      <th>Name</th>\n      <th>Age</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr><td>Cat</td><td>Momo</td><td>3</td></tr>\n    <tr><td>Dog</td><td>Rex</td><td>5</td></tr>\n    <tr><td>Fish</td><td>Nemo</td><td>1</td></tr>\n  </tbody>\n</table>",
        },
        {
            "task": "There are 3 mistakes. Fix them.",
            "hints": ["Does every row close? Are cells `<td>`? Are titles `<th>`?", "Add `</tr>` after Goals. `<tr>3</tr>` should be `<td>3</td>`. Name and Goals are `<th>`."],
            "start": "<table border=\"1\">\n  <tr>\n    <td>Name</td>\n    <td>Goals</td>\n  <tr>\n    <td>Ali</td>\n    <tr>3</tr>\n  </tr>\n</table>",
            "answer": "<table border=\"1\">\n  <tr>\n    <th>Name</th>\n    <th>Goals</th>\n  </tr>\n  <tr>\n    <td>Ali</td>\n    <td>3</td>\n  </tr>\n</table>",
        },
        {
            "task": "Times table: title cells \"x\", 1, 2, 3, then rows for 2 and 3 (2 × 1 = 2 ...).",
            "hints": ["First row: x, 1, 2, 3 as `<th>`.", "Row 2: 2, 4, 6. Row 3: 3, 6, 9."],
            "start": "",
            "answer": "<table border=\"1\">\n  <tr><th>x</th><th>1</th><th>2</th><th>3</th></tr>\n  <tr><th>2</th><td>2</td><td>4</td><td>6</td></tr>\n  <tr><th>3</th><td>3</td><td>6</td><td>9</td></tr>\n</table>",
        },
        {
            "task": "Your week timetable: Day, Morning, Evening for Monday to Friday, plus Saturday with one \"Fun day!\" cell using `colspan=\"2\"`.",
            "hints": ["Copy the Monday row 4 times and change the words.", "Saturday: `<td colspan=\"2\">Fun day!</td>`."],
            "start": "<h2>My week</h2>\n",
            "answer": "<h2>My week</h2>\n<table border=\"1\">\n  <thead>\n    <tr><th>Day</th><th>Morning</th><th>Evening</th></tr>\n  </thead>\n  <tbody>\n    <tr><td>Monday</td><td>School</td><td>Coding</td></tr>\n    <tr><td>Tuesday</td><td>School</td><td>Football</td></tr>\n    <tr><td>Wednesday</td><td>School</td><td>Coding</td></tr>\n    <tr><td>Thursday</td><td>School</td><td>Swimming</td></tr>\n    <tr><td>Friday</td><td>School</td><td>Coding</td></tr>\n    <tr><td>Saturday</td><td colspan=\"2\">Fun day!</td></tr>\n  </tbody>\n</table>",
        },
    ],
    "homework": [
        {
            "task": "\"My favorite foods\" table: Food, Taste (sweet or salty), Score (1 to 10). 4 rows. Put it on one of your pages.",
            "answer": "<table border=\"1\">\n  <tr><th>Food</th><th>Taste</th><th>Score</th></tr>\n  <tr><td>Pizza</td><td>Salty</td><td>10</td></tr>\n  <tr><td>Cake</td><td>Sweet</td><td>9</td></tr>\n  <tr><td>Plov</td><td>Salty</td><td>10</td></tr>\n  <tr><td>Apple</td><td>Sweet</td><td>7</td></tr>\n</table>",
        },
        {
            "task": "A football score table: Team, Played, Won, with 3 teams. Use thead and tbody.",
            "answer": "<table border=\"1\">\n  <thead>\n    <tr><th>Team</th><th>Played</th><th>Won</th></tr>\n  </thead>\n  <tbody>\n    <tr><td>Red</td><td>5</td><td>4</td></tr>\n    <tr><td>Blue</td><td>5</td><td>3</td></tr>\n    <tr><td>Green</td><td>5</td><td>1</td></tr>\n  </tbody>\n</table>",
        },
    ],
}
