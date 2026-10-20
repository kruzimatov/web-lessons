# Kids Web Course: HTML + CSS (age 8, from zero)

## Format

- 6 lessons a week, 20 to 40 minutes each, 24 lessons a month
- Online lessons (screen share). Student has a computer and an iPad
- Language: English first, short Uzbek hints where an Uzbek example explains better.
- He writes code in the live editor in Chrome. VS Code starts in lesson 6
- Homework after every lesson: 3 tasks, about 10 minutes

## Repo layout

| Folder | What | In git? |
|---|---|---|
| `generate/` | Lesson files (`lessons/lNN.py`), animations, builder | yes |
| `assets/`, `demo/` | Styles, scripts, demo page (copied into `site/`) | yes |
| `site/` | The built website. Vercel serves only this folder | yes |
| `teacher/` | Answers and course overview | **no**, local only |

Build: `python3 generate/build.py` from the repo root, then commit and push. Vercel redeploys on push.
Checker tests: `node generate/test_check.js`.
Keep the GitHub repo private: the lesson files in `generate/lessons/` contain the answers.

## Lesson template (the same for every lesson)

`build.py` checks these rules and stops if a lesson breaks one.

| Page | Who | Contents |
|---|---|---|
| `lesson.html` | Teacher, screen share | Warm-up: 3 quiz questions on the last lesson (none in lesson 1). Then 1 to 4 parts. Each part: short explanation + Uzbek hint, animation if it helps, example code, at least 1 "Your turn" editor, exactly 1 quiz question. Then "Watch out!" with 3 to 5 mistakes. |
| `practice.html` | Student, in class | "When I'm stuck" card. Exactly 5 tasks: Easy, Medium, Find the bug, Medium, Mini project. Each task has Hint 1 (small) and Hint 2 (bigger). No answers. Code autosaves. |
| `homework.html` | Student, at home | "When I'm stuck" card. 2 set tasks + task 3 "Your idea" (he builds anything with today's tags). Code autosaves. "Copy my homework" copies all 3 for Telegram. |
| `teacher/lessonNN_answers.html` | Teacher only | Practice and homework answers. Never publish the `teacher/` folder. |

Every editor: colored code, line numbers, auto-closing tags (CodeMirror from cdnjs, plain box without internet) and a "Check my code" button (`assets/check.js`, tests in `generate/test_check.js`) that explains mistakes with line numbers.

Course-wide pages: `cheatsheet.html` (My tags: every tag with an example, by lesson), `playground.html` (3 free editors that save), `teacher/overview.html` (every lesson on one page).

Timing (40 min): warm-up 5, parts 20 to 25, practice 10 to 15. Homework is shown at the end.
No teacher notes on the pages: the student sees the shared screen.

## Part 1: HTML (lessons 1 to 16, about 3 weeks)

Rule: every lesson is one full topic, taught completely. No tag family is split.

| # | Week | Lesson |
|---|---|---|
| 1 | 1 | What is HTML: websites, tags, `h1` to `h6`, `p`, skeleton, comments |
| 2 | 1 | Formatting text: `br`, `hr`, `strong`/`b`, `em`/`i`, `u`, nesting, `mark`, `small`, `del`, `sub`, `sup`, `&lt;` `&gt;` `&amp;` `&copy;` |
| 3 | 1 | Lists: `ul`, `ol`, `li`, nested lists, `start`, `type`, `reversed` |
| 4 | 1 | Practice day: "About me" page |
| 5 | 1 | Links: `a`, `href`, `target="_blank"`, `title`, link menus |
| 6 | 1 | VS Code, `my-website` folder, `!` + Tab, meta lines, links between own pages |
| 7 | 2 | Images: `img`, `src`, `alt`, `width`, `images/` folder, image links |
| 8 | 2 | Tables: `table`, `tr`, `td`, `th`, `thead`, `tbody`, `colspan`, `rowspan`, `border` |
| 9 | 2 | YouTube and maps `iframe`, `video`, `audio`, `controls` |
| 10 | 2 | Practice day: 3-page website |
| 11 | 2 | `div`, `span`, `header`, `nav`, `main`, `section`, `footer` |
| 12 | 2 | Forms 1: `form`, `label`, `input` (text, email, password, number, date), `button`, `placeholder`, `required`, `min`, `max` |
| 13 | 3 | Forms 2: checkbox, radio, `select`, `option`, `textarea` |
| 14 | 3 | Practice day: "Write to me" contact page |
| 15 | 3 | Review game (4 rounds) + test |
| 16 | 3 | Final project, show it to the family |

## Part 2: CSS (month 2, same template)

| # | Lesson |
|---|---|
| 17 | What CSS is: `style` attribute, `<style>`, external `style.css`, element selectors |
| 18 | Colors and backgrounds: names, hex, rgb, `background-color`, `background-image` |
| 19 | Classes, ids, grouping selectors |
| 20 | Text and fonts: `font-family`, Google Fonts, `font-size`, `text-align`, `line-height` |
| 21 | Box model 1: `width`, `height`, `border`, `border-radius`, `padding` |
| 22 | Project: profile card |
| 23 | Box model 2: `margin`, centering, `box-sizing`, Chrome DevTools |
| 24 | Links and buttons: `:hover`, `cursor`, `transition` |
| 25 | `display`: block, inline, inline-block |
| 26 | Flexbox 1: `display: flex`, `justify-content`, `align-items`, `gap` |
| 27 | Flexbox 2: `flex-direction`, `flex-wrap`, building a navbar |
| 28 | Project: styled website |
| 29 | Responsive: `@media`, phone and computer |
| 30 | Final CSS project |

## Teacher tips

- First lesson intro, short and calm: "Salom! Mening ismim Xayrullo. Men web saytlar
  yasayman. Bir oydan keyin siz ham o'zingizning saytingizni yasaysiz. Keling, boshlaymiz!"
  Then open `demo/index.html` and show what he will build.
- He types, you don't. Hands off his keyboard, even when it is slow.
- Praise the attempt, not only the result. Bugs are a game: "xatoni topdingiz!"
- If he is tired after 20 minutes, stop and do the project step. Short and happy beats long.
- Online: he types in the live editor and shares his screen. The live editor on lesson pages
  also works on his iPad once the pages are hosted (GitHub Pages or a shared link).
- At home he can practise in the live editor on any lesson page.
