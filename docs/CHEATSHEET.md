# Gemma 4 cheat sheet

1. **Gemma 4 is an open model family from Google DeepMind.** "Open" means the model files are public, so anyone can download and study them.
2. **The Gemini API hosts two of them:** `gemma-4-26b-a4b-it` (our default) and `gemma-4-31b-it`.
3. **"-it" means the chat-ready version.** It is trained to follow instructions.
4. **Sizes:** E2B, E4B, 12B, 26B, 31B. The "E" means "effective": E2B and E4B are small enough for laptops and phones. (The Gemini API hosts the 26B and 31B.)
5. **The 26B model is a "mixture of experts".** It has about 26 billion parts in total, but uses only about 4 billion for each piece of text it writes (that is the "A4B" in the name). So it is quick for its size.
6. **It reads text and images, and writes text.** Some of the smaller sizes can also take audio and video, but we do not use that here.
7. **Thinking mode** lets the model work through a problem before it answers. In the API, `thinking_level="high"` turns it on. It is slower and uses more of your allowance. `gemma_client.ask(..., thinking=True)` does this for you.
8. **Context window:** 128K tokens for the small models and 256K for the larger ones. 128K is about the length of a long novel. (A token is a piece of a word.)

Source: https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api

## Free limits

Free limits are counted per Google Cloud project, not per key. Check your own numbers in Google AI Studio. Do not trust numbers from blog posts.
