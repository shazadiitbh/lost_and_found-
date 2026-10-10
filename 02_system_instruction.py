"""
What this teaches:
    A "system instruction" is a rule you give the model before the question.
    It changes how the model answers, without changing the question.

How to run it:
    python 02_system_instruction.py

What you should see:
    The same question answered twice. First with no rule, then with a rule.
    The second answer should follow the rule (style and length).
"""

import gemma_client

question = "Why is the sky blue?"

# The rule. Try changing it: "Answer like a pirate", "Answer in one sentence", and so on.
rule = "You are a kind teacher for 10-year-old children. Use simple words. Answer in at most three sentences."

print("--- Without a rule ---")
print(gemma_client.ask(question))

print()
print("--- With a rule ---")
# The only difference: we pass the rule as `system`.
print(gemma_client.ask(question, system=rule))
