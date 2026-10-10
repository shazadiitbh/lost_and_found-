# Rules for AI coding tools

This is a hackathon project that uses Gemma 4 through the Gemini API. Follow these rules.

- Use the `google-genai` package (`from google import genai`) and the helper in `gemma_client.py`.
- The model is `gemma-4-26b-a4b-it`. Do not switch to another model or another AI provider.
- Never hard-code an API key. Read it from the environment (`GEMINI_API_KEY`, loaded from `.env`).
- Keep it to one screen and one Gemma call per click. No database, no login.
- If unsure about the Gemma API, read https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api. Do not guess.
- Keep `README.md` updated: the model name, how to run, and a screenshot.
- Keep the `LICENSE` file. Keep `.env` out of git.
- Do not add shell or network tools to the harness, and do not let tools touch files outside `notes/`.
