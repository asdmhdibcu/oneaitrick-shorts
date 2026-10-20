"""Fetch Microsoft Fluent Emoji 3D PNGs (MIT licence) from GitHub.

Usage: python3 fetch_fluent.py OUTDIR [name1,name2,...]
Each entry: (local_name, folder, tone_or_None)
The optional second argument fetches only those local names (e.g. the new art for one short).
"""
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets"

ITEMS = [
    ("hospital", "Hospital", None),
    ("robot", "Robot", None),
    ("doc_default", "Health worker", "Default"),
    ("doc_light", "Health worker", "Light"),
    ("doc_mlight", "Health worker", "Medium-Light"),
    ("doc_medium", "Health worker", "Medium"),
    ("doc_mdark", "Health worker", "Medium-Dark"),
    ("doc_dark", "Health worker", "Dark"),
    ("mdoc_light", "Man health worker", "Light"),
    ("mdoc_medium", "Man health worker", "Medium"),
    ("mdoc_dark", "Man health worker", "Dark"),
    ("wdoc_mlight", "Woman health worker", "Medium-Light"),
    ("wdoc_mdark", "Woman health worker", "Medium-Dark"),
    ("wdoc_light", "Woman health worker", "Light"),
    ("walker", "Person walking", "Medium-Light"),
    ("bandage", "Adhesive bandage", None),
    ("crutch", "Crutch", None),
    ("heart", "Anatomical heart", None),
    ("tooth", "Tooth", None),
    ("eye", "Eye", None),
    ("foot", "Foot", "Medium-Light"),
    ("flushed", "Flushed face", None),
    ("scream", "Face screaming in fear", None),
    ("rofl", "Rolling on the floor laughing", None),
    ("thinking", "Thinking face", None),
    ("mindblown", "Exploding head", None),
    ("sunglasses", "Smiling face with sunglasses", None),
    ("engineer", "Construction worker", "Medium"),
    ("technologist", "Technologist", "Medium-Dark"),
    ("ruler", "Triangular ruler", None),
    ("bellhop", "Bellhop bell", None),
    ("speech", "Speech balloon", None),
    ("keyboard", "Keyboard", None),
    ("brain", "Brain", None),
    ("wheelchair", "Motorized wheelchair", None),
    ("dash", "Dashing away", None),
    ("zap", "High voltage", None),
    ("office", "Office building", None),
    ("door", "Door", None),
    ("scientist", "Scientist", "Medium-Light"),
    ("scientist2", "Woman scientist", "Dark"),
    ("bulb", "Light bulb", None),
    ("paper", "Page facing up", None),
    ("house", "House", None),
    ("housegarden", "House with garden", None),
    ("couch", "Couch and lamp", None),
    ("pager", "Pager", None),
    ("sleeping", "Sleeping face", None),
    ("zzz", "Zzz", None),
    ("phone", "Mobile phone", None),
    ("receiver", "Telephone receiver", None),
    ("crystal", "Crystal ball", None),
    ("bell", "Bell", None),
    ("desktop", "Desktop computer", None),
    ("thumbsup", "Thumbs up", "Default"),
    ("party", "Party popper", None),
    ("sparkles", "Sparkles", None),
    ("moon", "Crescent moon", None),
    ("stars", "Night with stars", None),
    ("coffee", "Hot beverage", None),
    ("warning", "Warning", None),
    ("running", "Person running", "Medium"),
    ("runner_w", "Woman running", "Dark"),
    ("runner_m", "Man running", "Light"),
    ("stethoscope", "Stethoscope", None),
    ("collision", "Collision", None),
    ("satellite", "Satellite antenna", None),
    ("magnify", "Magnifying glass tilted right", None),
    ("chip", "Electric plug", None),
    ("rocket", "Rocket", None),
    ("disk", "Computer disk", None),
    # Short #2 (Read, don't obey)
    ("envelope", "Envelope", None),
    ("envelope_in", "Incoming envelope", None),
    ("email", "E-mail", None),
    ("mailbox", "Open mailbox with raised flag", None),
    ("card", "Credit card", None),
    ("money_wings", "Money with wings", None),
    ("stranger", "Bust in silhouette", None),
    ("globe", "Globe with meridians", None),
    ("syringe", "Syringe", None),
    ("shield", "Shield", None),
    ("unlocked", "Unlocked", None),
    ("wastebasket", "Wastebasket", None),
    ("wink", "Winking face", None),
    ("question", "Red question mark", None),
    ("locked", "Locked", None),
    ("hourglass", "Hourglass done", None),
    # Long-form "Rogue Swarm"
    ("calendar", "Spiral calendar", None),
    ("flag", "Triangular flag", None),
    ("puzzle", "Puzzle piece", None),
    ("memo", "Memo", None),
    ("pencil", "Pencil", None),
    ("school", "School", None),
    ("key", "Key", None),
    ("brick", "Brick", None),
    ("laptop", "Laptop", None),
    ("folder", "File folder", None),
    ("postbox", "Postbox", None),
    ("thought", "Thought balloon", None),
    ("namebadge", "Name badge", None),
    ("busts", "Busts in silhouette", None),
    ("megaphone", "Megaphone", None),
    ("ninja", "Ninja", 'Default'),
    ("hamburger", "Hamburger", None),
    ("stopwatch", "Stopwatch", None),
    ("clipboard", "Clipboard", None),
    ("scale", "Balance scale", None),
    ("battery", "Battery", None),
    ("lowbattery", "Low battery", None),
    ("candle", "Candle", None),
    ("whiteflag", "White flag", None),
    ("antenna", "Antenna bars", None),
    ("wilted", "Wilted flower", None),
    ("clapper", "Clapper board", None),
    ("raisedhand", "Raised hand", 'Default'),
    ("stopsign", "Stop sign", None),
    ("noentry", "No entry", None),
    ("construction", "Construction", None),
    ("gift", "Wrapped gift", None),
    ("policelight", "Police car light", None),
    ("web", "Spider web", None),
    ("newspaper", "Newspaper", None),
    ("broom", "Broom", None),
    ("masks", "Performing arts", None),
    ("popcorn", "Popcorn", None),
    ("tools", "Hammer and wrench", None),
    ("ice", "Ice", None),
    ("classical", "Classical building", None),
    ("stopbutton", "Stop button", None),
    ("coin", "Coin", None),
    ("scroll", "Scroll", None),
    ("turtle", "Turtle", None),
    ("shrug", "Person shrugging", 'Default'),
    ("fog", "Fog", None),
    ("bow", "Bow and arrow", None),
    ("climber", "Person climbing", 'Default'),
    ("trophy", "Trophy", None),
    ("redheart", "Red heart", None),
    ("wave", "Waving hand", 'Default'),
    ("hugging", "Hugging face", None),
    ("gear", "Gear", None),
    ("film", "Film projector", None),
    ("tv", "Television", None),
    ("fire", "Fire", None),
    ("eyes", "Eyes", None),
    ("crossmark", "Cross mark", None),
    ("check", "Check mark button", None),
    ("ghostcam", "Video camera", None),
    ("alarm", "Alarm clock", None),
    ("lightning", "Cloud with lightning", None),
]


def slug(folder):
    return folder.lower().replace(" ", "_")


ONLY = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None

ok, missing = [], []
for local, folder, tone in ITEMS:
    if ONLY and local not in ONLY:
        continue
    s = slug(folder)
    if tone:
        rel = f"{folder}/{tone}/3D/{s}_3d_{tone.lower()}.png"
    else:
        rel = f"{folder}/3D/{s}_3d.png"
    url = f"{BASE}/{quote(rel)}"
    dest = OUT / f"{local}.png"
    r = subprocess.run(["curl", "-sS", "-m", "60", "-o", str(dest), "-w", "%{http_code}", url], capture_output=True, text=True)
    if r.stdout.strip() == "200":
        ok.append(local)
    else:
        missing.append((local, folder, tone, r.stdout.strip()))
        dest.unlink(missing_ok=True)
print("ok", len(ok))
for m in missing:
    print("MISSING", m)
