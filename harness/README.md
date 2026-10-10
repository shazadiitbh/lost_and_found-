# The harness

A harness is the loop that lets the model use small tools.

## How the loop works

1. You send the question and a list of tools the model may ask for.
2. The model either answers, or replies "please run this tool with these inputs".
3. If it asked for a tool, your code runs it.
4. You send the tool's result back to the model.
5. This repeats until the model answers without asking for a tool (or `max_steps` is reached).

The code is in `agent.py`. Try it:

```python
from harness import Agent

agent = Agent(system="You are a helpful assistant.", verbose=True)
print(agent.run("What is 17 * 23, and what time is it?"))
```

`agent.steps` holds every step, so a screen can show them (the app template does this).

## Add a tool (5 lines)

Open `harness/tools.py` and add:

```python
@tool
def word_count(text: str):
    """Count the words in some text.

    text: the text to count
    """
    return len(text.split())
```

That is all. The description comes from the docstring. The inputs come from the type hints (`str`, `int`, `float`, `bool`). Tests: `python -m pytest harness`.

## Safety

The tools are small on purpose. There is no shell tool, no network tool, and `save_note` can only write to `notes/notes.txt`. The calculator never uses `eval`. If you add a tool, ask: "what is the worst thing the model could do with this?" Do not add tools that run commands, delete files or send messages for real.

## Entering the open-source challenge with a harness

MLH's rule for harness entries: "A model-harness entry must include an original implementation or meaningful changes to an existing open-source harness." Examples of meaningful changes:

- New tools that fit your idea (for example, a tool that looks up your college's timetable data).
- A memory of earlier steps, so the agent can use what it learned before.
- A limit on how big a tool result can be, so one long result does not flood the model.
- A step log shown to the user, so they can see what the agent did and why.

This is guidance, not a ruling. Read the rules page on the day. Your team must be able to explain what you changed and why.
