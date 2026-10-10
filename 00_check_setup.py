"""
What this teaches:
    Whether your computer is ready. It checks Python, the packages, your key,
    and makes one tiny call to Gemma 4.

How to run it:
    python 00_check_setup.py

What you should see:
    One line per step, each starting with PASS or FAIL. A FAIL line tells you what to do next.
    If every step says PASS, you are ready for the next script.
"""

import importlib.util
import os
import sys

failed = False


def report(ok, step, next_action=""):
    """Print PASS or FAIL for one step."""
    global failed
    if ok:
        print(f"PASS  {step}")
    else:
        failed = True
        print(f"FAIL  {step}\n      Next: {next_action}")


# Step 1: Python version. The Google package needs Python 3.10 or newer.
report(
    sys.version_info >= (3, 10),
    f"Python version is {sys.version_info.major}.{sys.version_info.minor}",
    "Install Python 3.10 or newer from python.org, then make a new virtual environment.",
)

# Step 2: the packages are installed.
for module, package in [("google.genai", "google-genai"), ("gradio", "gradio")]:
    try:
        installed = importlib.util.find_spec(module) is not None
    except ModuleNotFoundError:
        installed = False
    report(installed, f"{package} is installed",
           "Activate your virtual environment, then run: pip install -r requirements.txt")

# Step 3: the key. We only say "found". We never print any part of it.
import gemma_client  # this also reads your .env file

key = os.environ.get("GEMINI_API_KEY", "").strip()
key_found = bool(key) and key != "paste-your-key-here"
report(key_found, "API key found",
       "Copy .env.example to .env, then paste your key after GEMINI_API_KEY= (get one at aistudio.google.com).")

# Step 4: one tiny call to Gemma 4.
if key_found and not failed:
    try:
        answer = gemma_client.ask("Say hello in five words.")
        report(bool(answer.strip()), f"Gemma call worked (model: {gemma_client.MODEL})",
               "The model sent back nothing. Run this script again.")
    except Exception as error:
        report(False, "Gemma call worked", gemma_client.describe_error(error))
else:
    print("SKIP  Gemma call (fix the steps above first)")

print("\nAll good. Next: python 01_hello.py" if not failed else "\nFix the FAIL lines above, then run this script again.")
sys.exit(1 if failed else 0)
