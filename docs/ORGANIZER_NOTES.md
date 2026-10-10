# Notes for the organiser

Fill in the placeholders first: search the repo for `[EVENT DATE]`, `[SUBMISSION DEADLINE]`, `[ORGANIZERHQ LINK]`, `[ORGANIZER NAME]` and `[HELP DESK LOCATION]`.

## Publish as a template

1. Push the repo to your GitHub account as a **public** repo.
2. On GitHub: Settings, then tick **Template repository**.
3. Participants click **Use this template** to get their own copy. Tell them to keep their copy public and keep the license.

## Share the repo three ways

- **By link:** put the GitHub link on a slide and in the event chat.
- **By ZIP:** **Code > Download ZIP**. Put the ZIP on a shared drive.
- **By USB:** copy the unzipped folder (plus the wheelhouse, below) to a few USB sticks for people without git or with bad Wi-Fi.

## Why everyone needs their own key and project

Google's free limits are counted per Google Cloud project, not per key. If people share a key, or make several keys in one shared project, they share one allowance and everybody gets "too many requests". Each person should sign in with their own Google account and make their own key at aistudio.google.com. Check the real limits in AI Studio before the event. The repo does not state any numbers on purpose.

## Offline package folder (wheelhouse)

If Wi-Fi may be overloaded: on one Windows, one Mac and one Linux computer, run `python tools/make_wheelhouse.py` (needs internet, do it at home). Each run makes a `wheelhouse/` folder for that operating system and Python version. Share it by USB or a network share. People install with:

```
pip install --no-index --find-links wheelhouse -r requirements.txt
```

## For mentors: the five most common problems

1. The virtual environment is not active (no `(.venv)` in the prompt), so `No module named google`. 2. The key is missing or pasted wrong: the file is `.env.txt`, or there are quotes and spaces. 3. PowerShell blocks the activate script: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`. 4. `429` too many requests: people share a key or ask too fast; each person needs their own key and project. 5. A key pushed to GitHub: delete it in AI Studio and make a new one. Also watch for AI coding tools that switch to another provider; `docs/AI_ASSISTANT_PROMPT.md` stops this.
