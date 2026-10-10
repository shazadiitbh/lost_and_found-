# Prompt for your AI coding tool

Copy everything in the box below and paste it into your AI coding tool (Copilot, Cursor, Claude, ChatGPT, etc.) **before** it writes any code.

```
I am building a hackathon project with Gemma 4 through the Gemini API. Follow these rules.

1. Use the google-genai package (from google import genai) and the helper in gemma_client.py.
   Do not rewrite the helper. Call ask(), ask_with_image() and make_chat() from it.
2. The model is gemma-4-26b-a4b-it. Do not change it.
3. Never hard-code an API key. Read it from the environment (GEMINI_API_KEY, loaded from .env).
   Never print the key.
4. Keep the app to one screen and one Gemma call per click.
5. No database and no login.
6. Do not switch to other AI providers (no OpenAI, no Anthropic, no other Gemini models).
7. If you are not sure how the Gemma API works, read
   https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api instead of guessing.
8. Keep README.md updated: the model name, a "How to run" section, and a screenshot.
9. Keep the LICENSE file. Keep .env out of git.
10. Explain changes in plain English. I must be able to explain every line to the judges.
```

Why these rules? Judges need to see Gemma 4 used through the Gemini API, a working project, and a clean public repo. AI tools like to "improve" things by swapping the model or adding a database. These rules stop that.
