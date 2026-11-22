# The World in One Day — Saturday 21 November 2026
# Poster style: cream paper, navy band, serif masthead, number strip,
# region bar, 13 illustrated cards, dotted map, DATE CHECK box.
# Rendered at 2x then downscaled (LANCZOS) for smooth edges and rich colour.
# Deterministic: no random module, sine-hash grain only.
import math
from PIL import Image, ImageDraw, ImageFont

SS = 2                      # supersample factor
W, H = 1024 * SS, 1024 * SS
PAPER = (246, 239, 220)     # cream paper
INK = (26, 26, 26)
NAVY = (27, 42, 74)
RED = (178, 34, 34)
DRED = (139, 0, 0)
GREY = (110, 105, 92)
LGREY = (230, 224, 205)
RULE = (120, 110, 88)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(path, size):
    return ImageFont.truetype(FD + path, size * SS)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def vgrad(d, box, top, bot, steps=48):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        d.rectangle([x0, y0 + h * t0, x1, y0 + h * t1], fill=mix(top, bot, (t0 + t1) / 2))

def grain(img, amp=7):
    # deterministic sine-hash grain tiled over the picture
    px = img.load()
    w, h = img.size
    for yy in range(0, h, 3):
        for xx in range(0, w, 3):
            v = math.sin(xx * 12.9898 + yy * 78.233) * 43758.5453
            n = int((v - math.floor(v)) * amp * 2 - amp)
            if n:
                r, g, b = px[xx, yy]
                px[xx, yy] = (max(0, min(255, r + n)), max(0, min(255, g + n)),
                              max(0, min(255, b + n)))

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def banner(d, x, y, text, font):
    w_ = d.textlength(text, font=font) + 18 * SS
    d.rectangle([x, y, x + w_, y + 15 * SS], fill=RED)
    d.text((x + 9 * SS, y + 2 * SS), text, font=font, fill=(255, 255, 255))
    return w_

def srcstrip(d, x, y, w_, text, font):
    d.rectangle([x, y, x + w_, y + 12 * SS], fill=(20, 20, 20))
    d.text((x + 8 * SS, y + 1 * SS), text, font=font, fill=(240, 240, 235))

def card_frame(d, x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], outline=(190, 182, 160), width=2 * SS)
    d.rectangle([x + 3 * SS, y + 3 * SS, x + w_ + 4 * SS, y + h_ + 4 * SS],
                outline=(210, 202, 182), width=1 * SS)

# ---------------------------------------------------------------- data
NUMBERS = [
    ("400+", "drones over Ukraine"),
    ("110", "missiles in one night"),
    ("6.7", "Peru quake magnitude"),
    ("3", "missiles downed over Riyadh"),
    ("146", "walk away after jet fire"),
    ("$58,983", "Bitcoin price"),
]
REGIONS = [
    ("EUROPE 11", (27, 42, 74)), ("ASIA 10", (178, 34, 34)),
    ("AMERICAS 8", (46, 110, 62)), ("MIDDLE EAST 5", (150, 110, 20)),
    ("AFRICA 4", (122, 82, 40)), ("OCEANIA 3", (40, 110, 110)),
    ("WORLD 2", (96, 60, 140)),
]
# each card: place, tagline, headline, body, badge, source, scene key
CARDS = [
    dict(place="ANTALYA, TURKIYE", tag="CLIMATE", head="COP31 talks run into overtime with no deal",
         body="Draft text lost its fossil-fuel language as talks ran past deadline. (AP)",
         badge="DAY 13 OF 12", src="Summit president · Reuters", scene="cop"),
    dict(place="RIYADH", tag="MISSILES", head="Coalition downs three missiles over Riyadh",
         body="Saudi-led defences stopped three Houthi missiles aimed at the capital. (Reuters)",
         badge="3 INTERCEPTED", src="Coalition statement · Reuters", scene="riyadh"),
    dict(place="JUNIN, PERU", tag="QUAKE", head="M6.7 quake shakes central Peru",
         body="Deep quake struck at 00:09 GMT near Junin, felt in Lima. No deaths. (USGS)",
         badge="M6.7", src="USGS · Local reports", scene="quake"),
    dict(place="KYIV", tag="WAR", head="Russia hits Kyiv again, 42 hurt",
         body="Homes ablaze in Kyiv; 42 hurt in Kryvyi Rih. (Kyiv Post)",
         badge="42 HURT", src="Kyiv Post", scene="kyiv"),
    dict(place="DAVAO", tag="AVIATION", head="146 walk away after jet fire",
         body="Jet shut an engine down and landed safely. (Philstar)",
         badge="146 SAFE", src="Philstar", scene="jet"),
    dict(place="MERCURY", tag="SPACE", head="BepiColombo's Mercury flyby",
         body="Final flyby sets up orbit insertion in 2027. (ESA)",
         badge="FLYBY 6", src="ESA", scene="mercury"),
    dict(place="WARSAW", tag="NATO", head="Poland calls NATO talks over drone",
         body="NATO calls the debris fall a grave violation. (Reuters)",
         badge="NATO ALERT", src="Reuters", scene="warsaw"),
    dict(place="LAS VEGAS", tag="F1", head="Vegas: Verstappen fastest",
         body="Norris on pole as title rivals split practice. (F1)",
         badge="RACE NIGHT", src="F1", scene="vegas"),
    dict(place="WELLINGTON", tag="CRICKET", head="Rahul's 136 puts India in charge",
         body="Rahul's century gave India the lead. (ESPNcricinfo)",
         badge="136 RUNS", src="ESPNcricinfo", scene="cricket"),
    dict(place="BAYELSA", tag="NIGERIA", head="Boat capsizes in Bayelsa",
         body="A boat of mourners capsized in Bayelsa. (Punch)",
         badge="BOAT LOST", src="Punch", scene="boat"),
    dict(place="BITCOIN", tag="MARKETS", head="Bitcoin slides below $59,000",
         body="Bitcoin fell 3.9% as the Nasdaq sank 5.28%. (CoinDesk)",
         badge="$58,983", src="CoinDesk", scene="bitcoin"),
    dict(place="HORMUZ", tag="DRONES", head="US denies Iran downed a drone",
         body="Iran claimed an MQ-9 kill; US denies it. (Reuters)",
         badge="US DENIES", src="Reuters", scene="drone"),
    dict(place="CANBERRA", tag="AI SAFETY", head="Australia, China talk AI safety",
         body="Canberra and Beijing keep talking on AI risks. (Reuters)",
         badge="AI TALKS", src="Reuters", scene="aitalks"),
]
MORE = [
    (14, "Kyiv: Zelensky warns Crimea bridge 'will not stay' (NBC)"),
    (15, "France arrests terror suspect linked to ex-spy plot (AFP)"),
    (16, "Measles: US loses elimination status as cases spread (CDC)"),
    (17, "Sydney police hunt car after Bondi shooting (ABC)"),
    (18, "Riyadh: Houthi warhead parts recovered from debris (SPA)"),
    (19, "UK judge okays Bayer's $7.25bn Roundup deal (Reuters)"),
    (20, "Zelensky and Rubio meet in Geneva on a peace plan (Reuters)"),
    (21, "Trump says $2,000 tariff dividend checks coming (NBC)"),
    (22, "Germany: 1 dead in stabbing at Berlin station (Bild)"),
    (23, "UK-EU sign biggest post-Brexit agreements (BBC)"),
    (24, "ICJ: Myanmar committed genocide against Rohingya (ICJ)"),
    (25, "FBI: hack exposed US police database NCIC (Reuters)"),
    (26, "Australia: 5 die in house fire; murder charges laid (ABC)"),
    (27, "Ukraine: drone hits Zaporizhzhia plant area (Kyiv Post)"),
    (28, "India: 15 die in fire at a Hyderabad chemical plant (NDTV)"),
    (29, "Markets: S&P 500 falls 3.7% in the AI rout (Reuters)"),
    (30, "Nvidia: shares slide ~14% after record run (Bloomberg)"),
    (31, "Gold: falls 4.62% to $3,515.4 an ounce (Bloomberg)"),
    (32, "Anthropic: shares dip 8.5% after its $2tn IPO debut (CNBC)"),
    (33, "COP31: island states demand fossil phase-out (AP)"),
    (34, "Poland: PM Tusk calls it a deliberate provocation (BBC)"),
    (35, "Turin: Sinner beats Alcaraz to reach the ATP final (AP)"),
    (36, "Argentina: country risk tops 1,000 (Reuters)"),
    (37, "Haiti: Salvadoran troops hit by explosives, 3 hurt (AP)"),
    (38, "Gen Z protests in 25 European countries (Euronews)"),
    (39, "CERN: first ultra-rare particle decay observed (CERN)"),
    (40, "US: Agriculture Dept hit in a cyberattack (Reuters)"),
    (41, "Australia: police search for a missing hiker (ABC)"),
    (42, "Space: Blue Origin launches its 6th crewed flight (Space.com)"),
    (43, "Gaza: aid trucks enter as ceasefire holds (Reuters)"),
]

# ---------------------------------------------------------------- scenes
def scene_cop(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (58, 130, 200), (24, 90, 170))
    cx, cy, r = x + w * 0.42, y + h * 0.56, h * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 160, 90))
    d.ellipse([cx - r * 0.55, cy - r * 0.6, cx - r * 0.1, cy - r * 0.15], fill=(30, 120, 66))
    d.ellipse([cx + r * 0.1, cy + r * 0.2, cx + r * 0.55, cy + r * 0.6], fill=(30, 120, 66))
    d.ellipse([cx - r * 0.2, cy + r * 0.35, cx + r * 0.2, cy + r * 0.62], fill=(30, 120, 66))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 230, 255), width=3 * SS)
    kx, ky, kr = x + w * 0.78, y + h * 0.42, h * 0.30
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(250, 250, 245), outline=(40, 40, 40), width=3 * SS)
    d.line([kx, ky, kx, ky - kr * 0.62], fill=(30, 30, 30), width=4 * SS)
    d.line([kx, ky, kx + kr * 0.55, ky + kr * 0.25], fill=(30, 30, 30), width=4 * SS)
    d.ellipse([kx - 5 * SS, ky - 5 * SS, kx + 5 * SS, ky + 5 * SS], fill=(178, 34, 34))
    d.rectangle([x, y + h - 12 * SS, x + w, y + h], fill=(120, 84, 40))

def scene_riyadh(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (14, 18, 48), (30, 34, 70))
    # skyline band with lit windows, then interceptor bursts above it
    for bx, bw, bh in ((0.02, 0.12, 0.30), (0.16, 0.09, 0.20), (0.28, 0.14, 0.36),
                       (0.46, 0.10, 0.24), (0.60, 0.13, 0.34), (0.76, 0.11, 0.22),
                       (0.89, 0.09, 0.30)):
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(58, 62, 96))
        for k in range(3):
            wx = x + w * (bx + 0.02 + k * 0.035)
            wy = y + h - h * bh * (0.65 if k % 2 else 0.4)
            d.rectangle([wx, wy, wx + 6 * SS, wy + 6 * SS], fill=(255, 220, 120))
    for i, fx in enumerate((0.24, 0.52, 0.80)):
        bx, by = x + w * fx, y + h * 0.30
        d.line([bx + w * 0.10, y + h * 0.88, bx, by], fill=(255, 210, 90), width=5 * SS)
        d.ellipse([bx - 16 * SS, by - 16 * SS, bx + 16 * SS, by + 16 * SS], fill=(255, 150, 40))
        d.ellipse([bx - 8 * SS, by - 8 * SS, bx + 8 * SS, by + 8 * SS], fill=(255, 220, 120))

def scene_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 248, 240))
    d.polygon([(x, y + h), (x + w * 0.22, y + h * 0.52), (x + w * 0.45, y + h),
               (x + w * 0.68, y + h * 0.58), (x + w, y + h)], fill=(122, 84, 48))
    d.polygon([(x + w * 0.45, y + h), (x + w * 0.68, y + h * 0.58), (x + w, y + h)], fill=(96, 64, 36))
    pts = [(x + 6 * SS, y + h * 0.42)]
    xs = [0.08, 0.16, 0.22, 0.30, 0.36, 0.44, 0.50, 0.58, 0.64, 0.72, 0.78, 0.86, 0.94]
    ys = [0.42, 0.38, 0.52, 0.30, 0.48, 0.36, 0.50, 0.34, 0.46, 0.38, 0.50, 0.36, 0.44]
    pts = [(x + w * a, y + h * b) for a, b in zip(xs, ys)]
    d.line(pts, fill=(178, 34, 34), width=5 * SS, joint="curve")

def scene_kyiv(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (16, 20, 52), (40, 44, 80))
    mx, my, mr = x + w * 0.72, y + h * 0.28, h * 0.22
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(255, 200, 90))
    for bx, bw, bh in ((0.04, 0.16, 0.55), (0.24, 0.13, 0.40), (0.42, 0.18, 0.62), (0.64, 0.14, 0.46), (0.82, 0.14, 0.58)):
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(22, 24, 44))
        for k in range(3):
            wx = x + w * (bx + 0.03 + k * 0.045)
            wy = y + h - h * bh * (0.7 if k % 2 else 0.45)
            d.rectangle([wx, wy, wx + 8 * SS, wy + 8 * SS], fill=(255, 220, 120) if k != 1 else (90, 150, 255))

def scene_jet(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (150, 205, 240), (210, 232, 248))
    d.ellipse([x + w * 0.08, y + h * 0.30, x + w * 0.92, y + h * 0.62], fill=(250, 250, 250))
    d.ellipse([x + w * 0.10, y + h * 0.34, x + w * 0.22, y + h * 0.50], fill=(40, 90, 160))
    d.polygon([(x + w * 0.82, y + h * 0.34), (x + w * 0.95, y + h * 0.10),
               (x + w * 0.97, y + h * 0.34)], fill=(220, 225, 230))
    d.polygon([(x + w * 0.45, y + h * 0.55), (x + w * 0.62, y + h * 0.92),
               (x + w * 0.72, y + h * 0.60)], fill=(210, 216, 222))
    d.rectangle([x, y + h - 10 * SS, x + w, y + h], fill=(50, 52, 58))

def scene_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 10, 28))
    for sx, sy in ((0.12, 0.18), (0.85, 0.14), (0.30, 0.10), (0.92, 0.55), (0.08, 0.62)):
        d.ellipse([x + w * sx - 3 * SS, y + h * sy - 3 * SS, x + w * sx + 3 * SS, y + h * sy + 3 * SS], fill=(255, 255, 255))
    cx, cy, r = x + w * 0.58, y + h * 0.55, h * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 120, 70))
    d.ellipse([cx - r * 0.45, cy - r * 0.35, cx - r * 0.05, cy + r * 0.05], fill=(140, 88, 48))
    d.ellipse([cx + r * 0.15, cy + r * 0.25, cx + r * 0.5, cy + r * 0.6], fill=(140, 88, 48))
    mx, my, mr = x + w * 0.16, y + h * 0.60, h * 0.14
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(200, 200, 200))

def scene_warsaw(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 242))
    d.rectangle([x + w * 0.06, y + h * 0.14, x + w * 0.44, y + h * 0.38], fill=(255, 255, 255))
    d.rectangle([x + w * 0.06, y + h * 0.38, x + w * 0.44, y + h * 0.62], fill=(220, 40, 40))
    d.rectangle([x + w * 0.52, y + h * 0.14, x + w * 0.94, y + h * 0.62], fill=(30, 60, 150))
    d.rectangle([x + w * 0.52, y + h * 0.38, x + w * 0.94, y + h * 0.62], fill=(200, 30, 30))
    d.rectangle([x + w * 0.30, y + h * 0.72, x + w * 0.70, y + h * 0.86], fill=(120, 122, 128))

def scene_vegas(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (18, 18, 40), (40, 30, 60))
    d.ellipse([x + w * 0.10, y + h * 0.14, x + w * 0.34, y + h * 0.62], fill=(220, 40, 40))
    d.rectangle([x + w * 0.44, y + h * 0.30, x + w * 0.80, y + h * 0.56], fill=(245, 245, 245))
    d.rectangle([x + w * 0.80, y + h * 0.22, x + w * 0.94, y + h * 0.56], fill=(220, 40, 40))
    d.rectangle([x + w * 0.44, y + h * 0.30, x + w * 0.80, y + h * 0.40], fill=(200, 200, 200))
    for wx in (0.50, 0.82):
        d.ellipse([x + w * wx - 12 * SS, y + h * 0.52, x + w * wx + 12 * SS, y + h * 0.52 + 24 * SS], fill=(15, 15, 15))
    d.rectangle([x, y + h - 8 * SS, x + w, y + h], fill=(255, 200, 60))

def scene_cricket(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (34, 150, 70), (24, 110, 52))
    d.ellipse([x + w * 0.14, y + h * 0.52, x + w * 0.86, y + h * 0.92], fill=(150, 100, 55))
    d.rectangle([x + w * 0.46, y + h * 0.10, x + w * 0.54, y + h * 0.42], fill=(240, 220, 170))
    d.rectangle([x + w * 0.42, y + h * 0.02, x + w * 0.58, y + h * 0.14], fill=(255, 255, 255))
    d.ellipse([x + w * 0.66 - 7 * SS, y + h * 0.30, x + w * 0.66 + 7 * SS, y + h * 0.30 + 14 * SS], fill=(255, 255, 255))

def scene_boat(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (140, 200, 240), (190, 225, 245))
    d.polygon([(x + w * 0.48, y + h * 0.10), (x + w * 0.48, y + h * 0.68),
               (x + w * 0.86, y + h * 0.68)], fill=(255, 255, 255))
    d.polygon([(x + w * 0.44, y + h * 0.16), (x + w * 0.44, y + h * 0.68),
               (x + w * 0.14, y + h * 0.68)], fill=(240, 240, 240))
    d.line([x + w * 0.46, y + h * 0.06, x + w * 0.46, y + h * 0.70], fill=(90, 60, 30), width=4 * SS)
    d.polygon([(x + w * 0.06, y + h * 0.68), (x + w * 0.94, y + h * 0.68),
               (x + w * 0.82, y + h * 0.92), (x + w * 0.18, y + h * 0.92)], fill=(140, 90, 40))
    d.rectangle([x, y + h - 8 * SS, x + w, y + h], fill=(60, 120, 180))

def scene_bitcoin(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (255, 200, 60), (245, 160, 20))
    pts = [(x + w * a, y + h * b) for a, b in
           ((0.04, 0.62), (0.20, 0.40), (0.34, 0.55), (0.50, 0.28), (0.66, 0.50), (0.82, 0.30), (0.96, 0.42))]
    d.line(pts, fill=(178, 34, 34), width=5 * SS, joint="curve")
    cx, cy, r = x + w * 0.50, y + h * 0.52, h * 0.40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 150, 30), outline=(200, 110, 10), width=3 * SS)
    d.text((cx - 12 * SS, cy - 24 * SS), "B", font=SERIF_B(44), fill=(255, 255, 255))

def scene_drone(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (170, 210, 235), (215, 232, 244))
    cx, cy = x + w * 0.50, y + h * 0.50
    for dx in (-0.26, 0.26):
        px = x + w * (0.50 + dx)
        d.ellipse([px - 16 * SS, cy - 16 * SS, px + 16 * SS, cy + 16 * SS], fill=(120, 122, 128))
        d.line([px, cy, cx, cy], fill=(90, 92, 98), width=4 * SS)
    d.rectangle([cx - 34 * SS, cy - 18 * SS, cx + 34 * SS, cy + 18 * SS], fill=(70, 72, 78))
    d.ellipse([cx - 12 * SS, cy - 12 * SS, cx + 12 * SS, cy + 12 * SS], fill=(240, 240, 240))

def scene_aitalks(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 58))
    for cx, cy, col, lab in ((0.30, 0.62, (140, 90, 210), "AI"), (0.70, 0.62, (40, 180, 120), "AU")):
        px, py, r = x + w * cx, y + h * cy, h * 0.30
        d.ellipse([px - r, py - r, px + r, py + r], fill=col)
        tw = d.textlength(lab, font=SANS_B(40))
        d.text((px - tw / 2, py - 28 * SS), lab, font=SANS_B(40), fill=(255, 255, 255))

SCENES = {"cop": scene_cop, "riyadh": scene_riyadh, "quake": scene_quake,
          "kyiv": scene_kyiv, "jet": scene_jet, "mercury": scene_mercury,
          "warsaw": scene_warsaw, "vegas": scene_vegas, "cricket": scene_cricket,
          "boat": scene_boat, "bitcoin": scene_bitcoin, "drone": scene_drone,
          "aitalks": scene_aitalks}

# ---------------------------------------------------------------- layout
MX = 16 * SS
CW = W - 2 * MX          # content width, 1984 at SS=2

# dotted world map: land = union of rectangles in a 44 x 22 grid
LAND = [
    (2, 2, 14, 7), (4, 7, 13, 9), (6, 9, 9, 11),      # N America
    (15, 2, 17, 4),                                     # Greenland
    (12, 12, 17, 14), (13, 14, 16, 18), (14, 18, 15, 21),  # S America
    (24, 3, 30, 5), (25, 5, 28, 7), (24, 6, 25, 7),    # Europe
    (25, 9, 32, 12), (26, 12, 31, 16), (27, 16, 30, 19),   # Africa
    (31, 2, 44, 5), (31, 5, 40, 8), (36, 8, 39, 11),    # Asia
    (40, 8, 44, 11), (40, 11, 44, 12),                  # E Asia + islands
    (43, 6, 44, 8),                                     # Japan sliver
    (40, 16, 44, 19),                                   # Australia
]
PINS = {1: (26, 6), 2: (28, 8), 3: (13, 12), 4: (26, 5), 5: (37, 10),
        7: (25, 5), 8: (8, 7), 9: (43, 16), 10: (23, 10), 12: (29, 8),
        13: (40, 15)}

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 236, 230))
    gx, gy = 44, 22
    dx, dy = w / gx, h / gy
    for r in range(gy):
        for c in range(gx):
            if any(x0 <= c < x1 and y0 <= r < y1 for x0, y0, x1, y1 in LAND):
                px, py = x + (c + 0.5) * dx, y + (r + 0.5) * dy
                d.ellipse([px - 4 * SS, py - 4 * SS, px + 4 * SS, py + 4 * SS],
                          fill=(168, 152, 110))
    for n, (c, r) in PINS.items():
        px, py = x + (c + 0.5) * dx, y + (r + 0.5) * dy
        d.ellipse([px - 13 * SS, py - 13 * SS, px + 13 * SS, py + 13 * SS],
                  fill=RED, outline=(255, 255, 255), width=2 * SS)
        t = str(n)
        d.text((px - d.textlength(t, font=SANS_B(11)) / 2, py - 10 * SS), t,
               font=SANS_B(11), fill=(255, 255, 255))

def draw_card(d, c, x, y, w, pic_h, head_f, body_f, tag_f, num, hero=False):
    card_frame(d, x, y, w, pic_h + (134 if hero else 122) * SS)
    SCENES[c["scene"]](d, x + 2 * SS, y + 2 * SS, w - 4 * SS, pic_h)
    banner(d, x + 10 * SS, y + 8 * SS, c["badge"], SANS_B(11))
    srcstrip(d, x + 2 * SS, y + pic_h - 12 * SS, w - 4 * SS, c["src"], SANS(10))
    ty = y + pic_h + 8 * SS
    d.ellipse([x + 4 * SS, ty, x + 26 * SS, ty + 22 * SS], fill=RED)
    nt = str(num)
    d.text((x + 15 * SS - d.textlength(nt, font=SANS_B(12)) / 2, ty + 2 * SS),
           nt, font=SANS_B(12), fill=(255, 255, 255))
    d.text((x + 32 * SS, ty + 2 * SS), c["place"] + " · " + c["tag"],
           font=tag_f, fill=RED)
    hy = ty + 26 * SS
    hl = wrap(d, c["head"], head_f, w - 16 * SS)
    for i, ln in enumerate(hl[:2]):
        d.text((x + 8 * SS, hy + i * (head_f.size // SS + 6) * SS), ln,
               font=head_f, fill=INK)
    by = hy + 2 * (head_f.size // SS + 6) * SS + 2 * SS
    bl = wrap(d, c["body"], body_f, w - 16 * SS)
    for i, ln in enumerate(bl[:2]):
        d.text((x + 8 * SS, by + i * (body_f.size // SS + 4) * SS), ln,
               font=body_f, fill=(60, 58, 52))
    return len(hl), len(bl)

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # header band
    d.rectangle([0, 0, W, 60], fill=NAVY)
    d.text((MX, 8), "THE WORLD IN ONE DAY", font=SANS_B(20), fill=(255, 255, 255))
    rt = "43 STORIES · 7 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((W - MX - d.textlength(rt, font=SANS_B(15)), 12), rt,
           font=SANS_B(15), fill=(200, 205, 220))
    # masthead
    mt = "Saturday 21 November 2026"
    d.text(((W - d.textlength(mt, font=SERIF_B(52))) / 2, 72), mt,
           font=SERIF_B(52), fill=INK)
    st = "COP31 overtime · Three missiles downed over Riyadh · M6.7 quake shakes Peru"
    d.text(((W - d.textlength(st, font=SERIF(15))) / 2, 180), st,
           font=SERIF(15), fill=RED)
    d.line([MX, 228, W - MX, 228], fill=RULE, width=2 * SS)
    # number strip
    cw = CW / 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx = MX + i * cw
        d.text((cx + (cw - d.textlength(num, font=SERIF_B(26))) / 2, 236), num,
               font=SERIF_B(26), fill=RED)
        d.text((cx + (cw - d.textlength(cap, font=SANS(10))) / 2, 288), cap,
               font=SANS(10), fill=GREY)
        if i:
            d.line([cx, 240, cx, 312], fill=(200, 192, 172), width=1 * SS)
    d.line([MX, 328, W - MX, 328], fill=RULE, width=2 * SS)
    # region bar
    bx, bw = MX, CW
    x = bx
    for label, col in REGIONS:
        seg = bw * (int(label.rsplit(" ", 1)[1]) / 43)
        d.rectangle([x, 336, x + seg, 372], fill=col)
        d.text((x + (seg - d.textlength(label, font=SANS_B(9))) / 2, 344),
               label, font=SANS_B(9), fill=(255, 255, 255))
        x += seg
    # heroes
    gap = 8 * SS
    hw = (CW - 2 * gap) / 3
    counts = []
    for i, c in enumerate(CARDS[:3]):
        counts.append(draw_card(d, c, MX + i * (hw + gap), 384, hw, 72 * SS,
                                SERIF_B(24), SANS(13), SANS_B(13), i + 1, hero=True))
    # mediums, two rows of five
    gap2 = 7 * SS
    mw = (CW - 4 * gap2) / 5
    for row in range(2):
        for j in range(5):
            k = 3 + row * 5 + j
            counts.append(draw_card(d, CARDS[k], MX + j * (mw + gap2),
                                    812 + row * 368, mw, 54 * SS,
                                    SERIF_B(17), SANS(11), SANS_B(12), k + 1))
    # bottom section
    d.text((MX, 1548), "WHERE IT HAPPENED", font=SANS_B(14), fill=GREY)
    draw_map(d, MX, 1584, 250 * SS, 135 * SS)
    d.text((MX, 1860), "PACIFIC", font=SANS(10), fill=GREY)
    d.text((MX + 250 * SS - d.textlength("ATLANTIC", font=SANS(10)), 1860),
           "ATLANTIC", font=SANS(10), fill=GREY)
    lx = MX + 270 * SS
    d.text((lx, 1548), "ALSO ON SATURDAY 21 NOVEMBER — 30 MORE STORIES",
           font=SANS_B(16), fill=INK)
    colw = (W - MX - lx - 20 * SS) / 2
    for i, (n, t) in enumerate(MORE):
        col = i // 15
        row = i % 15
        tx = lx + col * (colw + 20 * SS)
        ty = 1584 + row * 24
        d.text((tx, ty), str(n), font=SANS_B(11), fill=RED)
        d.text((tx + 26 * SS, ty), t, font=SANS(11), fill=(50, 48, 44))
    # date check box
    d.rectangle([MX, 1952, W - MX, 2010], outline=RED, width=2 * SS)
    d.text((MX + 10 * SS, 1958),
           "DATE CHECK — Wires read to 04:00 UTC, Saturday 21 November 2026. Every story was reported, or was still",
           font=SANS(11), fill=INK)
    d.text((MX + 10 * SS, 1984),
           "developing, in the Saturday news cycle. Left out as other days' news: the Anthropic debut and GTA VI launch (19 Nov).",
           font=SANS(11), fill=INK)
    # footer
    d.text((MX, 2018), "THE WORLD IN ONE DAY", font=SANS_B(11), fill=GREY)
    ft = "SATURDAY 21 NOVEMBER 2026 · ONE PAGE"
    d.text((W - MX - d.textlength(ft, font=SANS_B(11)), 2018), ft,
           font=SANS_B(11), fill=GREY)
    out = img.resize((1024, 1024), Image.LANCZOS)
    grain(out, amp=4)
    out.save("entry.png", format="PNG")
    print("wrap counts (head, body) per card:", counts)
    print("saved entry.png")

if __name__ == "__main__":
    build()
