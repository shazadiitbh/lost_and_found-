"""Downloads every package from requirements.txt into a wheelhouse/ folder, for no-internet installs.

For organisers. Run it once on each type of computer (Windows, Mac, Linux), because the files
depend on your operating system and Python version. Then share the folder by USB or a local
network share if the event Wi-Fi is overloaded.

Run from the repo root:  python tools/make_wheelhouse.py
"""

import platform
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
folder = root / "wheelhouse"

print(f"Downloading packages for {platform.system()}, Python {platform.python_version()}...")
done = subprocess.run([sys.executable, "-m", "pip", "download", "-r", str(root / "requirements.txt"), "-d", str(folder)])
if done.returncode != 0:
    sys.exit("The download failed. Check your internet connection and try again.")

print(f"\nDone. The packages are in: {folder}")
print("This folder only works on the same operating system and Python version (e.g. Windows + Python 3.12).")
print("\nOn a computer with no internet, from the repo folder, run:")
print("    pip install --no-index --find-links wheelhouse -r requirements.txt")
