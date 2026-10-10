# Optional: run Gemma 4 on your own computer

**This is optional. You do not need it for either prize.** The Gemma challenge needs the Gemini API, so a project that only runs Gemma locally does not qualify for it. Use this only to experiment.

Do the download at home. Never on the event Wi-Fi: the files are several gigabytes.

You need Ollama 0.20.0 or newer (https://ollama.com). Then:

| Command | Model | Approx. download |
|---|---|---|
| `ollama pull gemma4:e2b` | E2B (smallest) | 4.6 to 7.5 GB |
| `ollama pull gemma4` | E4B (the default) | 6.6 to 9.5 GB |
| `ollama pull gemma4:12b` | 12B | 7.7 to 8 GB |
| `ollama pull gemma4:26b` | 26B | 16 to 19 GB |
| `ollama pull gemma4:31b` | 31B | 19 to 20 GB |

Sizes and names can change. Check https://ollama.com/library/gemma4 before you download.

Then `ollama run gemma4` starts a chat in your terminal.
