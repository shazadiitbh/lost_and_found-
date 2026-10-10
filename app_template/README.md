# Campus Lost & Found

A one-screen prototype for IIT Bhilai. Students submit a lost or found report with a short description, campus area, time, and optional item photo. **Gemma 4 (`gemma-4-26b-a4b-it`)** extracts category, color, keywords, and a summary. Local Python compares the report with the opposite type and returns up to three candidates.

## Matching score

- 40% Gemma-extracted item details (category and color)
- 30% text overlap
- 15% location proximity (same area or a small set of neighboring areas)
- 15% time proximity (score decreases across a seven-day window)

Scores are a transparent prototype heuristic, not probabilities or CLIP/sentence-transformer embeddings. Each submit makes one Gemma request; Python does the ranking locally.

## Run

From the repository root, activate `.venv`, make sure `.env` contains your private `GEMINI_API_KEY`, then run:

```cmd
python app_template/app.py
```

Open the local URL Gradio prints (port 7860 may already be occupied). Stop with Ctrl+C. The app uses `share=False`.

## Prototype limits and privacy

The app uses a tiny synthetic report list and session-only new reports. Reloading resets the session. It has no database, notifications, claim verification, OCR, or staff dashboard. Found-item reports can say where the item is kept. The app does not collect contact details; ownership should be verified with campus staff.

Use synthetic demo details only. Uploaded photos are sent to Google for Gemma analysis but are not saved by this app. Do not upload faces, ID cards, private messages, names, or contact details. Never commit `.env` or share your API key.

## Screenshot

After a successful launch, capture the running app with **Win+Shift+S** and save the screenshot as `app_template/screenshot.png`. Add it here before submission. Check that no key or private information is visible.
