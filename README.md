# Gemma 4 Starter

## Hackathon project: Campus Lost & Found

One-screen prototype using **Gemma 4 (`gemma-4-26b-a4b-it`)** to extract item details from a lost/found report or optional photo. Each report is compared with opposite-type reports using a visible weighted heuristic: item details 40%, text overlap 30%, location proximity 15%, and time proximity 15%. Matching runs locally in Python after one Gemma request. Scores are not probabilities. Reports are session-only synthetic demo data; ownership should be verified with campus staff.

The three-hour demo does not include persistent storage, notifications, claim verification, ID-card OCR, or a staff dashboard. These are future work, not working features.

### Run the app

From the repository root, activate `.venv`, make sure your private API key is saved in `.env`, then run:

```cmd
python app_template/app.py
```

Open http://127.0.0.1:7860. The app runs with `share=False`. For a presentation screenshot, launch the app and use **Win+Shift+S** to capture the page; save the image in `app_template/` and add it below before submitting. Do not include a real API key, personal reports, faces, IDs, or private messages in the screenshot.

See [app_template/README.md](app_template/README.md) for the feature walkthrough. The original setup guide and numbered learning scripts remain below.

Build with **Gemma 4** (model `gemma-4-26b-a4b-it`), an open model from Google, using a free key. This repo has two jobs:

1. **Learn:** run the numbered scripts in order. Each one adds one idea.
2. **Build:** copy `app_template/` and `harness/` as the start of your hackathon project.

Event: MLH Hack Day, IIT Bhilai. Date: [EVENT DATE]. Help desk: [HELP DESK LOCATION].

## How to run it (5 steps)

**1. Get a free key.** Go to [aistudio.google.com](https://aistudio.google.com), sign in, and create an API key. Use your own key. Do not share it.

**2. Get this repo.** Click **Use this template** on GitHub, or click **Code > Download ZIP** and unzip it. Open a terminal in the folder.

**3. Make a virtual environment and install.** (A virtual environment is a private box for this project's packages.)

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
If `python` is not found, try `py -m venv .venv` instead. If your prompt already starts with another name like `(.venv)` before you begin, type `deactivate` first, or you will install into the wrong environment. After the activate line, your prompt should start with `(.venv)`.

If PowerShell says "running scripts is disabled", run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and try the activate line again. It only affects this window.

Mac / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**4. Add your key.** Copy `.env.example` to `.env`, open it, and paste your key after `GEMINI_API_KEY=`.

Windows: `Copy-Item .env.example .env` then `notepad .env`. Mac / Linux: `cp .env.example .env`.

Never commit `.env`. It is already in `.gitignore`.

**5. Check it works.**
```
python 00_check_setup.py
```
Every line should say PASS. If not, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## The scripts

| Script | What it teaches |
|---|---|
| `00_check_setup.py` | Is your computer ready? One tiny test call. |
| `01_hello.py` | Your first call to Gemma 4. |
| `02_system_instruction.py` | Give the model a rule. Same question, different answer. |
| `03_chat.py` | Chat memory: follow-up questions that work. |
| `04_image.py` | Send a picture and get text back. |
| `05_function_calling.py` | The model asks your code to run a function. |

## Next

- **Build your own:** copy [app_template/](app_template/README.md) (a one-screen app).
- **Add a tool:** see [harness/](harness/README.md) (the loop that lets the model use tools).
- **Two challenges:** [docs/TWO_CHALLENGES.md](docs/TWO_CHALLENGES.md). One project can enter both.
- **Submitting:** [docs/SUBMISSION_CHECKLIST.md](docs/SUBMISSION_CHECKLIST.md). Run `python tools/check_submission.py` before you submit.
- **Stuck?** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md), [docs/CHEATSHEET.md](docs/CHEATSHEET.md), [docs/IDEAS.md](docs/IDEAS.md).
- **Using an AI coding tool?** Paste [docs/AI_ASSISTANT_PROMPT.md](docs/AI_ASSISTANT_PROMPT.md) into it first.

## License

MIT. See [LICENSE](LICENSE). Keep this file in your project.
