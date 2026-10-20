"""Game Zone page: Block Builder missions, Tag Racer and the Garage. Content lives in game_data.py."""

import json

from game_data import MISSIONS, QUESTIONS
from html_kit import esc, fmt, need_item, page, play

ARTS = {"sign", "house", "tree", "car", "rocket", "castle"}
PIXEL_FONT = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap">\n'
              '<link rel="stylesheet" href="assets/game.css">\n')


def check_game():
    ids = [m["id"] for m in MISSIONS]
    assert len(ids) == len(set(ids)), "game: two missions share an id"
    for m in MISSIONS:
        assert m["art"] in ARTS, f'game mission {m["id"]}: unknown art {m["art"]}'
        assert m["needs"], f'game mission {m["id"]}: needs at least 1 task'
    for q in QUESTIONS:
        assert len(set(q[2:])) == 3, f"game question {q[1]!r}: the 3 answers must differ"


def mission(k, m):
    needs = "".join(need_item(*n) for n in m["needs"])
    return (
        f'<section class="mission" id="m-{m["id"]}" data-id="{m["id"]}" data-art="{m["art"]}" hidden>'
        '<button type="button" class="back">Back to the map</button>'
        '<div class="mission-top"><div class="scene"><div class="art" aria-hidden="true"></div>'
        f'<p class="built">0 of {len(m["needs"])} built</p></div>'
        f'<div><h2>Level {k}: {esc(m["title"])}</h2><p class="story">{fmt(m["story"])}</p>'
        f'<ul class="needs">{needs}</ul></div></div>'
        + play(m["start"], save=f'game-{m["id"]}', lazy=True)
        + '<p class="finish"><button type="button" class="build-btn">Build it!</button>'
        '<span class="note" aria-live="polite"></span></p></section>'
    )


def level_button(k, m):
    return (
        f'<button type="button" class="level" data-go="{m["id"]}">'
        f'<span class="block">{k}</span><span class="name">{esc(m["title"])}</span>'
        f'<span class="stars" data-stars="{m["id"]}"></span><small>Lesson {m["lesson"]}</small></button>'
    )


def game_page():
    check_game()
    levels = "".join(level_button(k, m) for k, m in enumerate(MISSIONS, 1))
    missions = "".join(mission(k, m) for k, m in enumerate(MISSIONS, 1))
    lessons = sorted({q[0] for q in QUESTIONS})
    upto = "".join(f'<option value="{n}"{" selected" if n == lessons[-1] else ""}>{n}</option>' for n in lessons)
    data = json.dumps([list(q) for q in QUESTIONS]).replace("</", "<\\/")  # answers like </p> must not end the script
    body = f"""<h1><small>Play and learn</small>Game Zone</h1>
<div class="hud"><span class="gem" aria-hidden="true"></span><b id="gems">0</b> diamonds
<span class="star-icon" aria-hidden="true"></span><b id="star-total">0</b> of {3 * len(MISSIONS)} stars
<button type="button" id="sound" aria-pressed="true">Sound: on</button>
<button type="button" id="share">Copy my progress</button></div>
<p class="shared" id="shared" aria-live="polite"></p>
<div class="modes">
<button type="button" data-mode="builder" aria-pressed="true">Block Builder</button>
<button type="button" data-mode="racer" aria-pressed="false">Tag Racer</button>
<button type="button" data-mode="garage" aria-pressed="false">Garage</button></div>

<section class="mode" id="builder">
<p class="goal">Write the code, and watch your building grow block by block. Finish a level to win stars and diamonds!</p>
<div class="map">{levels}</div>
{missions}
</section>

<section class="mode" id="racer" hidden>
<p class="goal">Drive into the sign with the right answer. Every right answer gives you a diamond!</p>
<label class="upto">Questions from lessons 1 to <select id="upto">{upto}</select></label>
<p class="question" id="question" aria-live="polite">Press Start to drive!</p>
<div class="road-wrap"><canvas id="road" width="360" height="520" aria-label="Race track"></canvas>
<div class="overlay" id="overlay"><p class="over-title">Tag Racer</p><p id="over-text">Use the arrow keys or the buttons.</p>
<button type="button" id="go" class="build-btn">Start</button></div></div>
<div class="pads"><button type="button" id="left" aria-label="Move left">&#9664;</button>
<p class="racer-stats">Score <b id="score">0</b><br>Best <b id="best">0</b><br><span id="hearts" aria-label="Lives"></span></p>
<button type="button" id="right" aria-label="Move right">&#9654;</button></div>
<script type="application/json" id="questions">{data}</script>
</section>

<section class="mode" id="garage" hidden>
<p class="goal">Spend your diamonds on new cars, then drive them in Tag Racer.</p>
<div class="cars" id="cars"></div>
</section>
<div class="confetti" aria-hidden="true"></div>"""
    return page("Game Zone", body, root="", current="game.html", head=PIXEL_FONT,
                scripts=("game.js", "builder.js", "racer.js"))
