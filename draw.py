#!/usr/bin/env python3
"""Draws the 21 November 2026 world-news summary image (1024x1024 PNG).
Drawn at 2x and downscaled. Every fact from the day's wire reporting:
- Russia's overnight strike on Ukraine (400+ drones, ~110 missiles),
  missiles down in Poland
- Trump-Xi-Putin three-way summit in Shenzhen, joint declaration
- ICJ finds Myanmar responsible for genocide against the Rohingya
- AI sell-off pushes Wall Street into correction; Nasdaq erases 2026
  gains, Nvidia -14%
- Saudi-led defences intercept three Houthi ballistic missiles at Riyadh
- Daraxonrasib pill: pancreatic cancer undetectable in 1 in 12 patients
Ticker: COP31 overtime, Europe protests, Honda/Toyota 1.6M recall.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os, sys

S = 2  # supersample
W = 1024 * S
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
PAPER = (246, 241, 231)
INK = (29, 39, 51)
SUB = (74, 85, 96)
WHITE = (255, 255, 255)
SLATE = (52, 73, 94)
LIGHT = (214, 220, 224)

def F(path, size):
    return ImageFont.truetype(path, size * S)

img = Image.new('RGB', (W, W), PAPER)
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=INK, anchor='la'):
    d.text((x * S, y * S), s, font=font, fill=fill, anchor=anchor)

def rect(x, y, w, h, fill, outline=None, ow=2):
    d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], fill=fill, outline=outline, width=ow * S)

def rrect(x, y, w, h, r, fill, outline=None, ow=2):
    d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S], radius=r * S, fill=fill, outline=outline, width=ow * S)

def ell(cx, cy, rx, ry, fill, outline=None, ow=2):
    d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=fill, outline=outline, width=ow * S)

def poly(pts, fill):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill)

def line(pts, fill, w=3):
    d.line([(x * S, y * S) for x, y in pts], fill=fill, width=w * S, joint='curve')

def star(cx, cy, r1, r2, n, fill):
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = -math.pi / 2 + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    poly(pts, fill)

# ---------------- masthead ----------------
rect(72, 58, 14, 108, (176, 58, 46))
text(104, 52, 'THE WORLD IN ONE DAY', F(FB, 40), (176, 58, 46))
_date = 'SATURDAY 21 NOVEMBER 2026'
_size = 64
while _size > 30 and d.textlength(_date, font=F(FB, _size)) > 876 * S:
    _size -= 2
text(102, 96, _date, F(FB, _size), INK)
line([(72, 182), (952, 182)], INK, 5)
line([(72, 192), (952, 192)], INK, 2)

# ---------------- panel scaffolding ----------------
PW, PH, GX, GY, X0, Y0 = 452, 236, 20, 14, 72, 208
CATS = [
    ('WAR IN EUROPE', 'KYIV · POLAND', (176, 58, 46)),
    ('SUMMIT', 'SHENZHEN', (31, 97, 141)),
    ('JUSTICE', 'THE HAGUE', (17, 120, 100)),
    ('MARKETS', 'NEW YORK', (154, 125, 10)),
    ('MIDDLE EAST', 'RIYADH', (108, 52, 131)),
    ('HEALTH', 'LONDON', (30, 132, 73)),
]
HEADLINES = [
    ['Russia strikes Ukraine,', 'missiles land', 'in Poland'],
    ['Trump, Xi and Putin', 'hold first', 'three-way summit'],
    ['World court finds', 'Myanmar guilty', 'of genocide'],
    ['AI sell-off pushes', 'Wall Street into', 'correction'],
    ['Saudi defences', 'intercept Houthi', 'missiles'],
    ['Pill clears', 'pancreatic tumours', 'in trial'],
]
SUBS = [
    ['400+ drones, 110 missiles', 'overnight; deaths in Kyiv'],
    ['Joint declaration on peace', 'and security issued'],
    ['State held responsible for', 'genocide of the Rohingya'],
    ['Nasdaq erases 2026 gains;', 'Nvidia plunges 14%'],
    ['Three ballistic missiles', 'aimed at Riyadh, stopped'],
    ['Cancer undetectable on', 'scans in 1 in 12 patients'],
]

def panel(i):
    col, row = i % 2, i // 2
    return X0 + col * (PW + GX), Y0 + row * (PH + GY)

for i in range(6):
    x, y = panel(i)
    tag, place, color = CATS[i]
    rect(x, y, PW, PH, WHITE, INK, 2)
    rect(x, y, PW, 30, color)
    text(x + 12, y + 5, tag, F(FB, 19), WHITE)
    text(x + PW - 12, y + 6, place, F(FB, 17), WHITE, 'ra')
    for j, hl in enumerate(HEADLINES[i]):
        text(x + 140, y + 46 + j * 35, hl, F(FB, 24), INK)
    for j, sl in enumerate(SUBS[i]):
        text(x + 140, y + 160 + j * 27, sl, F(FR, 19), SUB)

# ---------------- icons (zone: x+14 .. x+138, y+44 .. y+222) ----------------
def icon_zone(i):
    x, y = panel(i)
    return x, y

# 1 — war: skyline, bursts, missiles
x, y = icon_zone(0)
for bx, bw, bh in [(18, 22, 62), (44, 18, 88), (66, 24, 54), (94, 18, 76), (114, 16, 48)]:
    rect(x + bx, y + 222 - bh, bw, bh, SLATE)
for wx, wy in [(50, 160), (56, 176), (100, 168), (24, 186), (72, 190)]:
    rect(x + wx, y + wy, 5, 7, (241, 196, 15))
star(x + 52, y + 84, 20, 8, 8, (230, 126, 34))
star(x + 104, y + 66, 15, 6, 8, (241, 196, 15))
for mx, my in [(30, 58), (78, 44), (118, 96)]:
    poly([(x + mx, y + my), (x + mx + 8, y + my + 22), (x + mx - 6, y + my + 24)], (192, 57, 43))
    poly([(x + mx - 2, y + my + 24), (x + mx + 4, y + my + 24), (x + mx + 1, y + my + 34)], (243, 156, 18))

# 2 — summit: three flags
x, y = icon_zone(1)
ell(x + 68, y + 74, 30, 30, (252, 209, 92))
for k, fx in enumerate([16, 58, 100]):
    line([(x + fx, y + 96), (x + fx, y + 216)], INK, 3)
    rect(x + fx, y + 96, 36, 24, WHITE, INK, 1)
    if k == 0:  # US: stripes + canton
        for sIdx in range(4):
            rect(x + fx, y + 96 + sIdx * 6, 36, 3, (176, 58, 46))
        rect(x + fx, y + 96, 16, 12, (31, 97, 141))
    elif k == 1:  # China: red + stars
        rect(x + fx, y + 96, 36, 24, (222, 41, 16))
        ell(x + fx + 8, y + 104, 3.4, 3.4, (255, 222, 0))
        for sx, sy in [(16, 100), (18, 106), (16, 112)]:
            ell(x + fx + sx, y + sy, 1.6, 1.6, (255, 222, 0))
    else:  # Russia: tricolour
        rect(x + fx, y + 104, 36, 8, (31, 97, 141))
        rect(x + fx, y + 112, 36, 8, (211, 47, 47))

# 3 — justice: courthouse
x, y = icon_zone(2)
poly([(x + 66, y + 58), (x + 16, y + 92), (x + 116, y + 92)], SLATE)
rect(x + 14, y + 94, 104, 10, SLATE)
for cx in [22, 48, 74, 100]:
    rect(x + cx, y + 108, 10, 74, LIGHT, SLATE, 1)
rect(x + 14, y + 184, 104, 8, SLATE)
rect(x + 8, y + 194, 116, 8, SLATE)
rect(x + 2, y + 204, 128, 8, SLATE)
ell(x + 66, y + 75, 6, 6, (241, 196, 15))

# 4 — markets: plunging chart + chip
x, y = icon_zone(3)
rect(x + 20, y + 52, 34, 34, WHITE, INK, 3)
rect(x + 29, y + 61, 16, 16, (154, 125, 10))
for px in [26, 34, 42]:
    line([(x + px, y + 44), (x + px, y + 52)], INK, 3)
    line([(x + px, y + 86), (x + px, y + 94)], INK, 3)
line([(x + 16, y + 100), (x + 16, y + 210)], INK, 3)
line([(x + 16, y + 210), (x + 126, y + 210)], INK, 3)
pts = [(24, 118), (52, 112), (72, 138), (92, 132), (118, 182)]
line([(x + a, y + b) for a, b in pts], (192, 57, 43), 5)
poly([(x + 118, y + 182), (x + 104, y + 178), (x + 112, y + 166)], (192, 57, 43))

# 5 — Riyadh: skyline, dome, intercept
x, y = icon_zone(4)
rect(x + 14, y + 168, 26, 44, SLATE)
rect(x + 100, y + 156, 22, 56, SLATE)
ell(x + 66, y + 168, 24, 16, SLATE)
rect(x + 42, y + 168, 48, 44, SLATE)
rect(x + 63, y + 128, 5, 26, SLATE)
ell(x + 65.5, y + 124, 4, 4, (241, 196, 15))
line([(x + 120, y + 50), (x + 96, y + 80), (x + 78, y + 98)], (192, 57, 43), 4)
star(x + 72, y + 104, 17, 7, 8, (230, 126, 34))
line([(x + 20, y + 118), (x + 44, y + 110), (x + 60, y + 108)], (17, 120, 100), 3)

# 6 — health: capsule + clear scan
x, y = icon_zone(5)
cap = Image.new('RGBA', (80 * S, 170 * S), (0, 0, 0, 0))
cd = ImageDraw.Draw(cap)
cd.rounded_rectangle([22 * S, 16 * S, 58 * S, 92 * S], radius=18 * S, fill=(192, 57, 43), outline=INK, width=2 * S)
cd.rounded_rectangle([22 * S, 90 * S, 58 * S, 154 * S], radius=18 * S, fill=WHITE, outline=INK, width=2 * S)
cap = cap.rotate(32, expand=True, resample=Image.BICUBIC)
img.paste(cap, (int((x + 2) * S), int((y + 40) * S)), cap)
d = ImageDraw.Draw(img)
ell(x + 94, y + 182, 26, 26, (234, 250, 241), (30, 132, 73), 3)
line([(x + 82, y + 182), (x + 91, y + 192), (x + 108, y + 170)], (30, 132, 73), 5)

# ---------------- ticker ----------------
rect(72, 954, 880, 64, INK)
text(88, 964, 'ALSO TODAY — COP31 climate talks run into overtime without a fossil-fuel deal · Protests', F(FR, 17), WHITE)
text(88, 990, 'continue across Europe · Honda and Toyota recall 1.6 million cars over airbag risk', F(FR, 17), WHITE)

img = img.resize((1024, 1024), Image.LANCZOS)
out = sys.argv[1]
img.save(out, optimize=True)
print(out, os.path.getsize(out), 'bytes')
