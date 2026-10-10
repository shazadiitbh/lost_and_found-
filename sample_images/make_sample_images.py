"""Draws the three sample pictures in this folder. Everything in them is made up.

Run:  python sample_images/make_sample_images.py     (needs Pillow: pip install -r requirements-dev.txt)
The pictures are plain on purpose. They have no real names, logos or places.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent


def font(size):
    return ImageFont.load_default(size=size)  # Pillow's built-in font, same on every computer


def draw_lines(draw, lines, x, y, size, gap):
    for line in lines:
        draw.text((x, y), line, fill="black", font=font(size))
        y += size + gap
    return y


def make_notice():
    image = Image.new("RGB", (900, 600), "#fff8e1")
    draw = ImageDraw.Draw(image)
    draw.rectangle([20, 20, 880, 580], outline="#b71c1c", width=6)
    draw.text((60, 60), "NOTICE", fill="#b71c1c", font=font(60))
    draw.text((60, 150), "Example College Tech Fest", fill="black", font=font(48))
    draw_lines(draw, ["Date: 14 March 2027", "Time: 10:00 AM to 4:00 PM", "Venue: Main Seminar Hall, Block B"], 60, 260, 40, 24)
    draw.text((60, 520), "(Fictional notice, made for a demo)", fill="gray", font=font(24))
    image.save(HERE / "notice.png")


def make_receipt():
    image = Image.new("RGB", (600, 800), "white")
    draw = ImageDraw.Draw(image)
    draw.text((120, 30), "EXAMPLE SHOP", fill="black", font=font(44))
    draw.text((150, 90), "Sample receipt", fill="gray", font=font(26))
    items = [("Notebook", "45.00"), ("Pen pack", "30.00"), ("Water bottle", "120.00"), ("Tea", "15.00"), ("Sticky notes", "25.00")]
    y = 170
    for name, price in items:
        draw.text((50, y), name, fill="black", font=font(32))
        draw.text((400, y), price, fill="black", font=font(32))
        y += 60
    draw.line([50, y + 10, 550, y + 10], fill="black", width=3)
    draw.text((50, y + 30), "TOTAL", fill="black", font=font(36))
    draw.text((400, y + 30), "235.00", fill="black", font=font(36))
    draw.text((50, 720), "(Fictional receipt, made for a demo)", fill="gray", font=font(22))
    image.save(HERE / "receipt.png")


def make_problem():
    image = Image.new("RGB", (900, 400), "white")
    draw = ImageDraw.Draw(image)
    draw.text((40, 30), "Maths problem", fill="black", font=font(40))
    draw_lines(draw, ["A train travels 120 km in 2 hours.", "How far will it go in 5 hours", "at the same speed?"], 40, 120, 36, 22)
    draw.text((40, 340), "(Fictional problem, made for a demo)", fill="gray", font=font(22))
    image.save(HERE / "problem.png")


if __name__ == "__main__":
    make_notice()
    make_receipt()
    make_problem()
    print("Made notice.png, receipt.png and problem.png in", HERE)
