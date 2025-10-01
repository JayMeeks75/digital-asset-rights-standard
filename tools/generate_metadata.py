
import os, json
from PIL import Image, ImageDraw, ImageFont

TOTAL = int(os.getenv("TOTAL", "500"))
OUT = os.getenv("OUT", "./out")
BASE_IMAGE = os.getenv("BASE_IMAGE", None)
BASE_URI = os.getenv("BASE_URI", "ipfs://YOUR_CID/")
NAME_PREFIX = os.getenv("NAME_PREFIX", "DARS Founding Partner")
START_ID = int(os.getenv("START_ID", "1"))

os.makedirs(OUT, exist_ok=True)

template = None
font = None
if BASE_IMAGE and os.path.exists(BASE_IMAGE):
    template = Image.open(BASE_IMAGE).convert("RGBA")
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 56)
    except:
        font = ImageFont.load_default()

for i in range(START_ID, START_ID + TOTAL):
    serial = f"{i:03d}/{TOTAL}"
    image_filename = f"{i}.png"
    meta_filename = f"{i}.json"

    if template:
        card = template.copy()
        d = ImageDraw.Draw(card)
        W, H = card.size
        text_w, text_h = d.textsize(serial, font=font)
        d.text(((W-text_w)//2, int(H*0.78)), serial, fill=(212,175,55), font=font)
        card.save(os.path.join(OUT, image_filename))

    metadata = {
        "name": f"{NAME_PREFIX} #{i}",
        "description": "Digital Asset Rights Standard (DARS) certificate representing verified rights and licensing.",
        "image": f"{BASE_URI}{image_filename}",
        "attributes": [
            {"trait_type": "Series", "value": "Founding Partner"},
            {"trait_type": "Serial", "value": serial}
        ]
    }
    with open(os.path.join(OUT, meta_filename), "w") as f:
        json.dump(metadata, f, indent=2)

print(f"Generated {TOTAL} metadata files in {OUT}")
