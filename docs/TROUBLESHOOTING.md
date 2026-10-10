# Troubleshooting

Run `python 00_check_setup.py` first. It tells you what is wrong.

| Error | What it means | Fix |
|---|---|---|
| `No module named google` (or `gradio`, `dotenv`) | The packages are not installed, or your virtual environment is off. | Activate the environment (`.venv\Scripts\Activate.ps1` on Windows, `source .venv/bin/activate` on Mac/Linux), then `pip install -r requirements.txt`. |
| "No API key found" | The key is not set. | Best: copy `.env.example` to `.env` and paste the key after `GEMINI_API_KEY=`. Windows notepad may save it as `.env.txt`: choose "All files" when saving. Or in PowerShell: `$env:GEMINI_API_KEY="your-key"`. On Mac/Linux: `export GEMINI_API_KEY="your-key"`. |
| `429` / "too many requests" / `RESOURCE_EXHAUSTED` | You are asking too fast, or you used your free allowance. | Wait a minute. Do not share one key between people. Check your limits in Google AI Studio. The helper already retries by itself. |
| Timeout or "connection" errors | Slow or blocked network. | Try again. Try a phone hotspot. |
| `404` / "model not found" | The model name is wrong. | Use `gemma-4-26b-a4b-it` or `gemma-4-31b-it`. Check `GEMMA_MODEL` in `.env`. |
| `py : The term 'py' is not recognized` | This computer has no `py` launcher (common with Anaconda or Microsoft Store Python). | Use `python -m venv .venv` instead. |
| `.venv\Scripts\Activate.ps1 : The module '.venv' could not be loaded` | The virtual environment was never created (the step before failed). | Run `python -m venv .venv` again and check it finishes with no error. |
| Packages went into the wrong environment | Another environment was already active when you ran `pip install`. | Type `deactivate`, make this repo's own `.venv`, activate it, and install again. |
| `running scripts is disabled on this system` (PowerShell) | Windows blocks the activate script. | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. Or use Command Prompt: `.venv\Scripts\activate.bat`. |
| Gradio: "port 7860 is busy" | Another app (maybe an old copy of yours) is using it. | Close the old one (Ctrl+C in its terminal), or set `GRADIO_SERVER_PORT=7861` and run again. |
| "Google did not accept your key" | The key is wrong, has extra characters, or was deleted. | Make a fresh key in Google AI Studio. Paste it with no quotes or spaces. |
| You pushed your key to GitHub | Anyone can see and use it now. | Delete that key in Google AI Studio right away and make a new one. Removing the file from GitHub is not enough. |
| `pip install` is very slow or fails | Event Wi-Fi is overloaded. | Ask a mentor for the offline folder (wheelhouse), then: `pip install --no-index --find-links wheelhouse -r requirements.txt`. |

Still stuck? Set `GEMMA_DEBUG=1` to see the full technical error, then ask a mentor at [HELP DESK LOCATION].
