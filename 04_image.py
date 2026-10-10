"""
What this teaches:
    Gemma 4 can read pictures. You send an image and a question, and get text back.
    We also ask for a fixed format, so the answer is easy to use in a program.

How to run it:
    python 04_image.py
    python 04_image.py path\\to\\your_photo.png     (use your own picture)

What you should see:
    Four lines: Event, Date, Time and Venue, read from the picture.
    The sample picture is a made-up notice for a fictional college tech fest.
"""

import sys
from pathlib import Path

import gemma_client

# Use the picture given on the command line, or the sample notice.
image_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("sample_images/notice.png")
if not image_path.exists():
    sys.exit(f"I cannot find the picture '{image_path}'. Run this from the repo folder, or check the path.")

# Asking for an exact format makes the answer predictable.
prompt = (
    "Read this notice. Reply with exactly four lines and nothing else:\n"
    "Event: ...\nDate: ...\nTime: ...\nVenue: ..."
)

# ask_with_image() uploads the picture and asks the question about it.
print(gemma_client.ask_with_image(image_path, prompt))
