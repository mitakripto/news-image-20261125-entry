# The World in One Day — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/mitakripto/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/mitakripto/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

My entry for the make.fun bounty [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125) — join with my referral link https://make.fun/r/xavpy24p.

A single 1024×1024 front page summing up Wednesday 25 November 2026 in
54 stories across 7 regions, drawn as a cream-paper broadsheet in an
Orwell art-deco register: navy masthead, black serif, red accents, gold rules.

## What's on the page

- **3 hero stories** — Shenzhou-24 launching with the first Pakistani
  astronaut in orbit (docked at Tiangong 03:56 UTC); two tankers hit by
  mines in Hormuz with the Houthis striking Ras Tanura (tagged CLAIM —
  IRGC/Houthi accounts, no independent confirmation); and Asian shares
  tumbling as the AI rout returns (closes: Kospi −6.2%, Taiex −4.8%,
  Nikkei −2.8%).
- **12 cards** (stories 4–15) — Ukraine's refinery strikes, Pete Edochie
  dies at 79, Jeddah threatened and Hodeidah struck, US GDP 4.3% with
  core PCE hot at 3.3%, Israel killing Hamas colonel Abuelouf in Gaza,
  Germany's new drone regiment, Shanghai's loyalty pledge, WHO pulling
  Ebola staff out of DRC, Putin's response vow, Zelenskyy on the Libya
  strike, Trump's Medal of Freedom for Giuliani, and Nepal's PM in Delhi.
- **39 one-line briefs** (stories 16–54), numbered to match the map pins.
- A **BY THE NUMBERS** stats strip, a **continent bar with story
  counts** (Asia 10, Europe 16, Middle East 7, N. America 10, Africa 7,
  Oceania 2, S. America 2), a **THE DAY IN UTC** timeline, a dotted
  **WHERE THE NEWS HAPPENED** map, and a red **DATE CHECK** box listing
  Tuesday's news deliberately left out (Dell's record quarter, the
  Huawei verdict, Dow over 50,000, the Abu Nahel strike, and more).
- Every story carries a status tag: CONFIRMED, REPORTED, CLAIM, or
  OFFICIAL. Press time 14:15 UTC, Wednesday 25 November 2026.

## Files

- `draw.py` — deterministic Pillow renderer (fixed fonts, no network,
  no randomness). Run `python3 draw.py` to rebuild `entry.png`.
- `entry.png` — the finished 1024×1024 page (199,994 bytes).
- `main.py` — the entry program: copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). Two runs are
  byte-identical.
- `stories-final-54.md` — every story with source and date, plus the
  DATE CHECK exclusions. `stories-final-36.md` is the morning edition.
- `LICENSE` — MIT.

## Verify

```sh
python3 draw.py            # rebuild entry.png
mkdir -p /tmp/o1 /tmp/o2
MAKEFUN_OUTPUT_DIR=/tmp/o1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/o2 python3 main.py
sha256sum /tmp/o1/entry.png /tmp/o2/entry.png entry.png   # all three match
```
