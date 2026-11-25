"""Front page for Wednesday 25 November 2026, drawn with Pillow.

One page, 54 numbered stories: 3 heroes, 12 cards and 39 briefs.
Everything on the page is laid out from the data tables below, so the
printed counts, the region bar and the story numbers cannot drift
apart.  The drawing is deterministic: fixed fonts, fixed geometry,
no clock, no randomness and no network.
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
CREAM = (247, 240, 219)
PAPER = (251, 247, 231)
NAVY = (13, 47, 59)
INK = (24, 22, 18)
RED = (178, 34, 30)
GOLD = (190, 148, 52)
GREY = (92, 88, 78)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def width(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap(draw, text, fnt, limit):
    """Greedy word wrap to a pixel limit; returns a list of lines."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if width(draw, trial, fnt) <= limit or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def shrink(draw, text, path, size, limit, floor=7):
    """Largest size at or below `size` that keeps text inside limit."""
    while size > floor and width(draw, text, font(path, size)) > limit:
        size -= 1
    return font(path, size)


REGION_STYLE = {
    "ASIA": ((38, 110, 110), "Asia"),
    "EUROPE": ((196, 96, 44), "Europe"),
    "MIDDLE EAST": ((128, 128, 52), "M. East"),
    "N. AMERICA": ((168, 52, 44), "N. America"),
    "AFRICA": ((62, 122, 62), "Africa"),
    "OCEANIA": ((106, 74, 138), "Oceania"),
    "S. AMERICA": ((24, 62, 110), "S. America"),
}

REGION_BAR = [
    ("ASIA · 10", 140),
    ("EUROPE · 16", 150),
    ("MIDDLE EAST · 7", 145),
    ("N. AMERICA · 10", 165),
    ("AFRICA · 7", 115),
    ("OCEANIA · 2", 135),
    ("S. AMERICA · 2", 150),
]

NUMBERS = [
    ("00:18", "Shenzhou-24 lifts off"),
    ("2", "Tankers hit mines, Hormuz"),
    ("−6.2%", "Kospi falls in Seoul"),
    ("4.3%", "US GDP, Q3 revised up"),
    ("79", "Pete Edochie's age"),
    ("19", "Civilians killed in Sudan"),
]

TIMELINE = (
    "00:18 Shenzhou-24 launches  ·  03:56 Docking at Tiangong  ·  "
    "06:35 Crew boards Tiangong  ·  09:46 IRGC: two tankers hit mines  ·  "
    "13:30 US GDP 4.3%; PCE hot"
)

HEROES = [
    {
        "num": 1, "region": "ASIA", "topic": "SPACE", "tag": "CONFIRMED",
        "headline": "Shenzhou-24 launches; first Pakistani in orbit",
        "body": "Muhammad Zeeshan Ali, 40, flies to Tiangong with Tang "
                "Hongbo and Wu Yi. Docked 03:56 UTC; crew aboard 06:35. "
                "(Reuters, Xinhua)",
        "scene": "rocket",
    },
    {
        "num": 2, "region": "MIDDLE EAST", "topic": "WAR", "tag": "CLAIM",
        "headline": "Two tankers hit mines in Hormuz; Houthis hit Ras Tanura",
        "body": "IRGC: two tankers exploded and burned on an unauthorised "
                "route; Houthis say they struck Saudi Arabia's Ras Tanura "
                "refinery. (Reuters)",
        "scene": "hormuz",
    },
    {
        "num": 3, "region": "ASIA", "topic": "MARKETS", "tag": "CONFIRMED",
        "headline": "Asian shares tumble as AI rout returns",
        "body": "Kospi falls 6.2%, Taiex 4.8%, Nikkei 2.8% as the AI sell-off "
                "returns; Samsung −9.9%, SoftBank −14.8%. Closes. (Reuters, AP)",
        "scene": "chart",
    },
]

# Cards are placed in the order they appear on the printed page:
# the first printed row holds 4, 5, 6, 7, 8, 15 and the second 9-14.
CARDS = [
    {"num": 4, "region": "EUROPE", "tag": "REPORTED", "label": "2 HIT",
     "headline": "Ukraine drones hit two Russian refineries",
     "body": "Syzran and Kuibyshev ablaze; one killed, 145 downed. (Reuters)",
     "scene": "refinery"},
    {"num": 5, "region": "AFRICA", "tag": "CONFIRMED", "label": "79",
     "headline": "Nollywood icon Pete Edochie dies at 79",
     "body": "Okonkwo of 'Things Fall Apart' dies in Enugu. (Family, Punch)",
     "scene": "face"},
    {"num": 6, "region": "MIDDLE EAST", "tag": "CONFIRMED", "label": "HODEIDAH",
     "headline": "Jeddah threatened; Hodeidah struck",
     "body": "Houthis vow to hit Jeddah; coalition hits Hodeidah. (Reuters)",
     "scene": "port"},
    {"num": 7, "region": "N. AMERICA", "tag": "CONFIRMED", "label": "4.3%",
     "headline": "US GDP jumps to 4.3%; core PCE hot",
     "body": "Q3 growth up from 3.4%; core PCE 3.3% tops forecasts. (BEA)",
     "scene": "bars"},
    {"num": 8, "region": "MIDDLE EAST", "tag": "REPORTED", "label": "4 DEAD",
     "headline": "Israel kills Hamas colonel Abuelouf",
     "body": "Airstrike kills Abuelouf, 47, wife and two daughters. (Reuters)",
     "scene": "city"},
    {"num": 15, "region": "ASIA", "tag": "CONFIRMED", "label": "DELHI",
     "headline": "Nepal PM Shah meets Modi in Delhi",
     "body": "First foreign trip; talks, energy, deals. (Reuters)",
     "scene": "flags"},
    {"num": 9, "region": "EUROPE", "tag": "OFFICIAL", "label": "NEW UNIT",
     "headline": "Germany announces new drone regiment",
     "body": "Pistorius sets up a Bundeswehr unit for recon. (Wires)",
     "scene": "drone"},
    {"num": 10, "region": "ASIA", "tag": "CONFIRMED", "label": "SHANGHAI",
     "headline": "Shanghai pledges loyalty to Beijing",
     "body": "City backs Beijing as Chen Jining faces inquiry. (Reuters)",
     "scene": "gate"},
    {"num": 11, "region": "AFRICA", "tag": "REPORTED", "label": "ITURI",
     "headline": "WHO pulls Ebola staff out of DRC hospital",
     "body": "Teams sheltered 3 days in Ituri amid fighting. (WHO)",
     "scene": "cross"},
    {"num": 12, "region": "EUROPE", "tag": "REPORTED", "label": "KREMLIN",
     "headline": "Putin: Russia will answer refinery raids",
     "body": "Kremlin vows a response to strikes inside Russia. (AAP)",
     "scene": "wall"},
    {"num": 13, "region": "EUROPE", "tag": "CONFIRMED", "label": "BENGHAZI",
     "headline": "Zelenskyy: Libya strike was self-defence",
     "body": "Kyiv defends its drone attack at Benghazi. (Reuters)",
     "scene": "ship"},
    {"num": 14, "region": "N. AMERICA", "tag": "CONFIRMED", "label": "FREEDOM",
     "headline": "Trump gives Giuliani Medal of Freedom",
     "body": "President honours ex-New York mayor. (Wash. Post)",
     "scene": "medal"},
]

BRIEFS = [
    (16, "ASIA", "Hong Kong −1.1%, Shanghai −2%"),
    (17, "ASIA", "India markets reopen after holiday"),
    (18, "ASIA", "Ex-police chief in treason probe"),
    (19, "ASIA", "Japan service prices at 36-yr high"),
    (20, "ASIA", "Iran rial plunges to record low"),
    (21, "ASIA", "Bogor mine: 7 dead, 19 missing"),
    (22, "OCEANIA", "Australia CPI 4.9%; core 3.8%"),
    (23, "OCEANIA", "Solomons sign Australia pact"),
    (24, "EUROPE", "EU-Balkans summit opens"),
    (25, "EUROPE", "€45bn Ukraine loan row"),
    (26, "EUROPE", "Leak: Russian war dead 490k+"),
    (27, "EUROPE", "Two held over William burglary"),
    (28, "EUROPE", "Eurozone inflation hits 4.0%"),
    (29, "EUROPE", "EU: no return to Russian gas"),
    (30, "EUROPE", "Pope decries COP31 collapse"),
    (31, "EUROPE", "Zelenskyy: Kyiv needs €115bn"),
    (32, "MIDDLE EAST", "Saudi budget sees 2027 growth"),
    (33, "MIDDLE EAST", "Iran says no talks with US"),
    (34, "MIDDLE EAST", "US warns Americans on Houthis"),
    (35, "MIDDLE EAST", "Iran: Hormuz reopen in 48 hrs"),
    (36, "AFRICA", "Emir suspended in assault claim"),
    (37, "AFRICA", "Rebels pull back from DRC areas"),
    (38, "AFRICA", "HIV may rebound after 20% cut"),
    (39, "AFRICA", "Sudan: RSF strikes kill 19"),
    (40, "AFRICA", "2 Libyan officers die in Benghazi"),
    (41, "N. AMERICA", "Fed 100% to hike in Dec"),
    (42, "N. AMERICA", "Trump pardons turkeys"),
    (43, "N. AMERICA", "Democrats clinch 259+"),
    (44, "N. AMERICA", "Hack clues point to China"),
    (45, "N. AMERICA", "Abrego Garcia flies to Spain"),
    (46, "N. AMERICA", "Anthropic below IPO price"),
    (47, "N. AMERICA", "Amazon buys Decart"),
    (48, "S. AMERICA", "Citi weighs Venezuela return"),
    (49, "S. AMERICA", "Cartagena hostages freed"),
    (50, "EUROPE", "Russian strike kills 2 in Odesa"),
    (51, "N. AMERICA", "Dow dives as PCE runs hot"),
    (52, "EUROPE", "EasyJet profit falls 89% on fuel"),
    (53, "EUROPE", "Roche breast drug wins FDA nod"),
    (54, "EUROPE", "US halts Patriot supplies to Kyiv"),
]

DATE_CHECK_A = (
    "Left out on purpose (all Tuesday 24 Nov): Dell's record quarter · "
    "Huawei guilty verdict · Dow tops 50,000 · Gaza strike kills Hamas chief Abu Nahel"
)
DATE_CHECK_B = (
    "Nepal 5.3 quake · Riyadh tower strike · Poland US troops push · "
    "Hasina return plan · Ukraine's $125bn plea · CIA/ODNI breach · "
    "Senegal AFCON ruling · Cartagena hostages · UCL results"
)
TAG_LEGEND = (
    "TAGS: CONFIRMED = 2+ outlets · REPORTED = one outlet · "
    "CLAIM = one side's account · OFFICIAL = on the record"
)


def badge(draw, x, y, num, colour, size=15):
    draw.rectangle([x, y, x + size, y + size], fill=colour)
    label = str(num)
    fnt = font(SANS_B, 10 if len(label) == 1 else 8)
    tw = width(draw, label, fnt)
    draw.text((x + (size - tw) / 2, y + 1), label, font=fnt, fill=WHITE)


def tag_chip(draw, right, y, tag):
    colour = RED if tag in ("CLAIM", "REPORTED") else NAVY
    fnt = font(SANS_B, 8)
    tw = width(draw, tag, fnt) + 10
    draw.rectangle([right - tw, y, right, y + 13], fill=colour)
    draw.text((right - tw + 5, y + 2), tag, font=fnt, fill=WHITE)
    return right - tw


def scene_rocket(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NAVY)
    for sx, sy in [(0.08, 0.2), (0.2, 0.65), (0.88, 0.75), (0.7, 0.15),
                   (0.35, 0.3), (0.55, 0.7), (0.95, 0.35)]:
        px, py = x0 + sx * (x1 - x0), y0 + sy * (y1 - y0)
        draw.text((px, py), "·", font=font(SANS_B, 14), fill=(240, 210, 120))
    cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2
    draw.polygon([(cx, cy - 26), (cx + 11, cy - 4), (cx - 11, cy - 4)], fill=WHITE)
    draw.rectangle([cx - 11, cy - 4, cx + 11, cy + 16], fill=WHITE)
    draw.ellipse([cx - 5, cy - 14, cx + 5, cy - 4], fill=RED)
    draw.polygon([(cx - 11, cy + 8), (cx - 20, cy + 22), (cx - 11, cy + 22)], fill=RED)
    draw.polygon([(cx + 11, cy + 8), (cx + 20, cy + 22), (cx + 11, cy + 22)], fill=RED)
    draw.polygon([(cx - 5, cy + 16), (cx + 5, cy + 16), (cx, cy + 30)],
                 fill=(240, 160, 40))
    draw.text((x1 - 86, y1 - 24), "00:18 UTC", font=font(SANS_B, 12),
              fill=(240, 200, 90))


def scene_hormuz(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(216, 178, 118))
    draw.rectangle([x0, y0 + (y1 - y0) * 2 // 3, x1, y1], fill=(96, 128, 138))
    for i, fx in enumerate((0.22, 0.62)):
        sx = x0 + fx * (x1 - x0)
        sy = y0 + (y1 - y0) * 2 // 3 - 6
        draw.rectangle([sx, sy, sx + 52, sy + 9], fill=(40, 40, 40))
        draw.rectangle([sx + 8, sy - 7, sx + 40, sy], fill=(150, 52, 40))
        draw.ellipse([sx + 16, sy + 10, sx + 30, sy + 22], fill=(240, 150, 50))
        draw.ellipse([sx + 30, sy + 12, sx + 40, sy + 20], fill=(230, 90, 40))
    label = "HORMUZ · TWO TANKERS"
    fnt = font(SANS_B, 10)
    draw.text(((x0 + x1 - width(draw, label, fnt)) / 2, y1 - 16), label,
              font=fnt, fill=(60, 44, 20))


def scene_chart(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NAVY)
    base = y1 - 12
    heights = [44, 30, 38, 20, 26, 12]
    bw = (x1 - x0 - 90) // len(heights)
    for i, h in enumerate(heights):
        bx = x0 + 14 + i * bw
        draw.rectangle([bx, base - h, bx + bw - 8, base], fill=RED)
    pts = [(x0 + 14, y0 + 14), (x1 - 80, base - 34)]
    draw.line(pts, fill=(240, 200, 120), width=2)
    draw.text((x1 - 72, y0 + 12), "−6.2%", font=font(SANS_B, 17),
              fill=(240, 220, 160))


def card_scene(draw, box, scene, label):
    x0, y0, x1, y1 = box
    palettes = {
        "refinery": (74, 70, 66), "face": (214, 196, 130), "port": (140, 62, 44),
        "bars": (24, 52, 92), "city": (104, 100, 96), "flags": (224, 148, 60),
        "drone": (30, 54, 84), "gate": (178, 44, 38), "cross": (96, 110, 128),
        "wall": (120, 44, 38), "ship": (36, 84, 96), "medal": (128, 52, 96),
    }
    draw.rectangle(box, fill=palettes.get(scene, NAVY))
    mid_y = (y0 + y1) // 2
    if scene == "refinery":
        for i, tx in enumerate((x0 + 12, x0 + 34, x0 + 56)):
            draw.rectangle([tx, y0 + 8, tx + 12, y1 - 6], fill=(168, 164, 156))
            draw.rectangle([tx, y0 + 8, tx + 12, y0 + 13], fill=(200, 196, 188))
    elif scene == "face":
        cx, cy = x0 + 34, mid_y
        draw.ellipse([cx - 16, cy - 15, cx + 16, cy + 17], outline=INK, width=2)
        draw.ellipse([cx - 8, cy - 6, cx - 4, cy - 2], fill=INK)
        draw.ellipse([cx + 4, cy - 6, cx + 8, cy - 2], fill=INK)
        draw.arc([cx - 9, cy + 1, cx + 9, cy + 13], 15, 165, fill=INK, width=2)
    elif scene == "bars":
        for i, h in enumerate((10, 16, 13, 22)):
            bx = x0 + 12 + i * 18
            draw.rectangle([bx, y1 - 8 - h, bx + 12, y1 - 8], fill=(240, 190, 70))
    elif scene == "drone":
        cx, cy = x0 + 30, mid_y
        draw.line([cx - 16, cy, cx + 16, cy], fill=WHITE, width=2)
        draw.line([cx, cy - 9, cx, cy + 9], fill=WHITE, width=2)
        for dx, dy in ((-16, -9), (16, -9), (-16, 9), (16, 9)):
            draw.ellipse([cx + dx - 5, cy + dy - 3, cx + dx + 5, cy + dy + 3],
                         outline=WHITE, width=1)
    elif scene == "cross":
        cx, cy = x0 + 30, mid_y
        draw.rectangle([cx - 4, cy - 13, cx + 4, cy + 13], fill=WHITE)
        draw.rectangle([cx - 12, cy - 4, cx + 12, cy + 4], fill=WHITE)
    elif scene == "medal":
        draw.polygon([(x0 + 22, y0 + 4), (x0 + 32, y0 + 4), (x0 + 27, y1 - 14)],
                     fill=(240, 200, 90))
        draw.ellipse([x0 + 18, y1 - 22, x0 + 36, y1 - 4], outline=(240, 200, 90), width=3)
    fnt = shrink(draw, label, SANS_B, 13, x1 - x0 - 70)
    draw.text((x1 - width(draw, label, fnt) - 8, mid_y - 8), label, font=fnt,
              fill=WHITE)


LAND = [
    [(0.02, 0.35), (0.08, 0.18), (0.20, 0.10), (0.32, 0.14), (0.30, 0.28),
     (0.24, 0.38), (0.26, 0.48), (0.20, 0.55), (0.15, 0.48), (0.08, 0.45)],
    [(0.22, 0.58), (0.30, 0.55), (0.34, 0.65), (0.30, 0.82), (0.25, 0.92),
     (0.21, 0.80), (0.19, 0.66)],
    [(0.44, 0.22), (0.52, 0.14), (0.58, 0.20), (0.56, 0.32), (0.50, 0.36),
     (0.45, 0.32)],
    [(0.46, 0.42), (0.56, 0.38), (0.62, 0.48), (0.58, 0.68), (0.52, 0.78),
     (0.47, 0.62)],
    [(0.58, 0.16), (0.75, 0.08), (0.92, 0.14), (0.95, 0.30), (0.85, 0.42),
     (0.78, 0.52), (0.72, 0.42), (0.64, 0.38), (0.58, 0.28)],
    [(0.74, 0.55), (0.84, 0.53), (0.88, 0.60), (0.80, 0.63)],
    [(0.84, 0.68), (0.94, 0.66), (0.96, 0.76), (0.88, 0.80), (0.83, 0.74)],
]

PINS = [
    (1, "ASIA", 0.76, 0.29), (2, "MIDDLE EAST", 0.625, 0.41),
    (3, "ASIA", 0.875, 0.27), (4, "EUROPE", 0.64, 0.21),
    (5, "AFRICA", 0.465, 0.54), (6, "MIDDLE EAST", 0.59, 0.475),
    (7, "N. AMERICA", 0.10, 0.36), (8, "MIDDLE EAST", 0.55, 0.355),
    (9, "EUROPE", 0.48, 0.23), (10, "ASIA", 0.835, 0.375),
    (11, "AFRICA", 0.525, 0.605), (12, "EUROPE", 0.55, 0.155),
    (13, "AFRICA", 0.505, 0.42), (14, "N. AMERICA", 0.205, 0.295),
    (15, "ASIA", 0.705, 0.405),
]


def inside(px, py, poly):
    hit = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > py) != (yj > py):
            cross = (xj - xi) * (py - yi) / (yj - yi) + xi
            if px < cross:
                hit = not hit
        j = i
    return hit


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 242, 238), outline=GREY)
    step = 7
    gx = x0 + 6
    while gx < x1 - 4:
        gy = y0 + 6
        while gy < y1 - 4:
            nx = (gx - x0) / (x1 - x0)
            ny = (gy - y0) / (y1 - y0)
            if any(inside(nx, ny, poly) for poly in LAND):
                draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(110, 130, 120))
            gy += step
        gx += step
    for num, region, nx, ny in PINS:
        px, py = x0 + nx * (x1 - x0), y0 + ny * (y1 - y0)
        colour = REGION_STYLE[region][0]
        r = 8
        draw.ellipse([px - r, py - r, px + r, py + r], fill=colour, outline=WHITE)
        label = str(num)
        fnt = font(SANS_B, 9 if len(label) == 1 else 7)
        draw.text((px - width(draw, label, fnt) / 2, py - 5), label,
                  font=fnt, fill=WHITE)


def masthead(draw):
    draw.rectangle([8, 8, PAGE - 8, 126], fill=NAVY)
    draw.rectangle([8, 8, PAGE - 8, 126], outline=GOLD, width=2)
    small = font(SANS_B, 11)
    draw.text((20, 17), "THE DAY IN WORLD NEWS", font=small, fill=(240, 200, 120))
    right = "54 STORIES · 7 REGIONS · ONE PAGE"
    draw.text((PAGE - 20 - width(draw, right, small), 17), right, font=small,
              fill=(240, 200, 120))
    # A small watching eye in the middle of the top line.
    cx, cy = PAGE // 2, 24
    draw.ellipse([cx - 17, cy - 9, cx + 17, cy + 9], outline=(240, 200, 120), width=2)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    title = "Wednesday 25 November 2026"
    fnt = shrink(draw, title, SERIF_B, 50, PAGE - 60)
    draw.text(((PAGE - width(draw, title, fnt)) / 2, 34), title, font=fnt, fill=WHITE)
    sub = "Every story on this page happened, or was first reported, on this day."
    fnt = font(SERIF_I, 16)
    draw.text((20, 98), sub, font=fnt, fill=(232, 222, 190))
    draw.text((PAGE - 32, 96), "◆", font=font(SANS, 14), fill=(240, 200, 120))


def region_bar(draw):
    colours = [REGION_STYLE[name][0] for name in
               ("ASIA", "EUROPE", "MIDDLE EAST", "N. AMERICA", "AFRICA",
                "OCEANIA", "S. AMERICA")]
    x, y = 12, 131
    fnt = font(SANS_B, 11)
    for (label, seg_w), colour in zip(REGION_BAR, colours):
        draw.rectangle([x, y, x + seg_w, y + 24], fill=colour)
        draw.text((x + (seg_w - width(draw, label, fnt)) / 2, y + 6), label,
                  font=fnt, fill=WHITE)
        x += seg_w


def numbers_strip(draw):
    y = 159
    label_f = font(SANS_B, 10)
    draw.text((14, y + 2), "BY THE", font=label_f, fill=RED)
    draw.text((14, y + 15), "NUMBERS", font=label_f, fill=RED)
    col_w = (PAGE - 110) // 6
    big = font(SERIF_B, 25)
    small = font(SANS, 9)
    for i, (value, caption) in enumerate(NUMBERS):
        x = 96 + i * col_w
        if i:
            draw.line([x - 8, y, x - 8, y + 34], fill=(200, 190, 160))
        draw.text((x, y), value, font=big, fill=INK)
        for j, line in enumerate(wrap(draw, caption, small, col_w - 12)):
            draw.text((x, y + 28 + j * 10), line, font=small, fill=GREY)
    draw.line([12, y + 42, PAGE - 12, y + 42], fill=GOLD, width=1)


def timeline_strip(draw):
    y = 206
    draw.text((14, y), "THE DAY IN UTC", font=font(SANS_B, 10), fill=RED)
    fnt = shrink(draw, TIMELINE, SANS, 11, PAGE - 130)
    draw.text((122, y), TIMELINE, font=fnt, fill=INK)
    draw.line([12, y + 15, PAGE - 12, y + 15], fill=GOLD, width=1)


def hero(draw, x, w, item):
    y = 226
    scene_box = [x, y, x + w, y + 88]
    if item["scene"] == "rocket":
        scene_rocket(draw, scene_box)
    elif item["scene"] == "hormuz":
        scene_hormuz(draw, scene_box)
    else:
        scene_chart(draw, scene_box)
    colour, _ = REGION_STYLE[item["region"]]
    ty = y + 94
    badge(draw, x, ty, item["num"], colour)
    draw.text((x + 20, ty + 2), f"{item['region']} · {item['topic']}",
              font=font(SANS_B, 11), fill=colour)
    tag_chip(draw, x + w, ty, item["tag"])
    hy = ty + 19
    head_f = font(SERIF_B, 21)
    for line in wrap(draw, item["headline"], head_f, w)[:3]:
        draw.text((x, hy), line, font=head_f, fill=INK)
        hy += 23
    body_f = font(SANS, 11)
    for line in wrap(draw, item["body"], body_f, w)[:4]:
        draw.text((x, hy + 2), line, font=body_f, fill=(60, 56, 48))
        hy += 13


def card(draw, x, y, w, item):
    colour, _ = REGION_STYLE[item["region"]]
    card_scene(draw, [x, y, x + w, y + 38], item["scene"], item["label"])
    ty = y + 42
    badge(draw, x, ty, item["num"], colour, size=13)
    draw.text((x + 17, ty + 1), item["region"], font=font(SANS_B, 8), fill=colour)
    tag_chip(draw, x + w, ty, item["tag"])
    hy = ty + 15
    head_f = font(SERIF_B, 13)
    for line in wrap(draw, item["headline"], head_f, w)[:3]:
        draw.text((x, hy), line, font=head_f, fill=INK)
        hy += 14
    body_f = font(SANS, 8)
    for line in wrap(draw, item["body"], body_f, w)[:3]:
        draw.text((x, hy + 1), line, font=body_f, fill=(70, 66, 58))
        hy += 10


def bottom_section(draw):
    y = 706
    draw.text((12, y), "WHERE THE NEWS HAPPENED", font=font(SANS_B, 11), fill=INK)
    head = "ALSO ON WEDNESDAY 25 NOVEMBER — 39 MORE STORIES"
    draw.text((364, y), head, font=font(SANS_B, 11), fill=INK)
    draw.line([12, y + 15, PAGE - 12, y + 15], fill=INK, width=1)
    draw_map(draw, [12, y + 20, 348, y + 196])
    draw.text((14, y + 200), "Dots mark stories 1–15; pin colour = continent.",
              font=font(SANS, 9), fill=GREY)
    # Briefs in three columns of thirteen: 16-28, 29-41, 42-54.
    col_x = [364, 584, 804]
    col_w = 208
    num_f = font(SANS_B, 8)
    body_f = font(SANS, 9)
    for col in range(3):
        chunk = BRIEFS[col * 13:(col + 1) * 13]
        for row, (num, region, text) in enumerate(chunk):
            by = y + 22 + row * 15
            colour, short = REGION_STYLE[region]
            draw.rectangle([col_x[col], by, col_x[col] + 14, by + 11], fill=colour)
            label = str(num)
            draw.text((col_x[col] + (14 - width(draw, label, num_f)) / 2, by + 1),
                      label, font=num_f, fill=WHITE)
            line = f"{short}: {text}"
            fnt = shrink(draw, line, SANS, 9, col_w - 18, floor=7)
            draw.text((col_x[col] + 17, by + 1), line, font=fnt, fill=INK)


def date_check(draw):
    y = 932
    draw.rectangle([12, y, PAGE - 12, y + 42], outline=RED, width=2)
    draw.text((20, y + 5), "DATE CHECK — NOT WEDNESDAY NEWS",
              font=font(SANS_B, 10), fill=RED)
    fnt = shrink(draw, TAG_LEGEND, SANS, 8, 430)
    draw.text((PAGE - 20 - width(draw, TAG_LEGEND, fnt), y + 6), TAG_LEGEND,
              font=fnt, fill=GREY)
    small = font(SANS, 9)
    draw.text((20, y + 19), DATE_CHECK_A, font=shrink(draw, DATE_CHECK_A, SANS, 9, PAGE - 44),
              fill=INK)
    draw.text((20, y + 31), DATE_CHECK_B, font=shrink(draw, DATE_CHECK_B, SANS, 9, PAGE - 44),
              fill=INK)
    foot = font(SANS, 9)
    draw.text((12, y + 50),
              "Every story on this page happened, or was first reported, on Wednesday 25 November 2026.",
              font=foot, fill=GREY)
    draw.text((12, y + 63),
              "Sources: Reuters, AP, AFP, CNN, Euronews, AAP, WHO, Kyiv Independent, DeepDraft. "
              "Original drawings. Claims are attributed, not stated as fact. "
              "Wires read to 14:15 UTC, Wed 25 Nov 2026.",
              font=shrink(draw, "Sources: Reuters, AP, AFP, CNN, Euronews, AAP, WHO, Kyiv Independent, DeepDraft. "
                                 "Original drawings. Claims are attributed, not stated as fact. "
                                 "Wires read to 14:15 UTC, Wed 25 Nov 2026.", SANS, 9, PAGE - 24),
              fill=GREY)


def build_page():
    img = Image.new("RGB", (PAGE, PAGE), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, PAGE - 1, PAGE - 1], outline=NAVY, width=3)
    draw.rectangle([5, 5, PAGE - 6, PAGE - 6], outline=GOLD, width=1)
    masthead(draw)
    region_bar(draw)
    numbers_strip(draw)
    timeline_strip(draw)
    hero_w = 328
    for i, item in enumerate(HEROES):
        hero(draw, 12 + i * (hero_w + 8), hero_w, item)
    card_w = 162
    for i, item in enumerate(CARDS):
        row, col = divmod(i, 6)
        card(draw, 12 + col * (card_w + 5), 462 + row * 120, card_w, item)
    bottom_section(draw)
    date_check(draw)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build_page().save(out, format="PNG", optimize=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
