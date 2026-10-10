"""
What this teaches:
    Chat memory. A normal call forgets everything. A chat remembers earlier messages,
    so you can ask follow-up questions like "which of those...".

How to run it:
    python 03_chat.py

What you should see:
    A first answer about castles in Japan, then a second answer that clearly refers to the first
    (the second question never says "castle"). Then you can keep chatting. Type quit to leave.
"""

import gemma_client

# make_chat() starts a chat that keeps the history for us.
chat = gemma_client.make_chat(system="You are a friendly travel guide. Keep answers short.")

print("You: What are the three most famous castles in Japan?")
print("Gemma:", chat.send_message("What are the three most famous castles in Japan?"))

# This question only makes sense if the chat remembers the first one.
print("\nYou: Which of those is the oldest?")
print("Gemma:", chat.send_message("Which of those is the oldest?"))

# Optional: keep chatting. Press Enter on an empty line, or type quit, to stop.
print("\nYour turn! Type a message, or quit to leave.")
while True:
    try:
        message = input("You: ").strip()
    except EOFError:
        break
    if message.lower() in ("", "quit"):
        break
    print("Gemma:", chat.send_message(message))
