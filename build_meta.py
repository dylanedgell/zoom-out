"""Generate share/branding assets: favicon, apple-touch-icon, and an Open Graph
preview card (1200x630) from the Milky Way sky face. Run after build_sky.py.

Usage: python3 build_meta.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(__file__)


def load_font(size):
    for p in [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def pale_blue_dot(size):
    """Black square with a soft glowing pale-blue dot — the motif of the app."""
    img = Image.new("RGB", (size, size), (0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = size * 0.5, size * 0.5
    r = size * 0.16
    # glow
    glow = Image.new("RGB", (size, size), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - r * 2.2, cy - r * 2.2, cx + r * 2.2, cy + r * 2.2], fill=(40, 70, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(size * 0.06))
    img = Image.blend(img, glow, 0.9)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 190, 235))
    d.ellipse([cx - r * 0.5, cy - r * 0.6, cx + r * 0.2, cy + r * 0.1], fill=(210, 228, 250))
    return img


def og_card():
    W, H = 1200, 630
    sky = Image.open(os.path.join(HERE, "sky", "pz.jpg")).convert("RGB")
    # cover-crop the 1024x1024 sky to 1200x630
    scale = max(W / sky.width, H / sky.height)
    sky = sky.resize((int(sky.width * scale), int(sky.height * scale)))
    left = (sky.width - W) // 2
    top = (sky.height - H) // 2
    card = sky.crop((left, top, left + W, top + H))
    # darken for text legibility
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    card = Image.blend(card, dark, 0.35)
    d = ImageDraw.Draw(card)
    title = load_font(96)
    sub = load_font(34)
    d.text((80, 250), "Zoom Out", font=title, fill=(238, 241, 246))
    d.text((84, 372), "From your ZIP code to the edge of space, and back.",
           font=sub, fill=(180, 195, 220))
    card.save(os.path.join(HERE, "og-image.jpg"), quality=88)
    print("wrote og-image.jpg 1200x630")


def main():
    pale_blue_dot(64).save(os.path.join(HERE, "favicon.png"))
    pale_blue_dot(180).save(os.path.join(HERE, "apple-touch-icon.png"))
    print("wrote favicon.png 64, apple-touch-icon.png 180")
    og_card()


if __name__ == "__main__":
    main()
