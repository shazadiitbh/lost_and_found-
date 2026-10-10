"""Tests for the harness. They use a fake model, so they need no key and no internet.

Run from the repo root:  python -m pytest harness
"""

from types import SimpleNamespace

import pytest
from google.genai import types

from harness import Agent, tools


def tool_request(name, args):
    """A fake model reply that asks for a tool."""
    call = SimpleNamespace(name=name, args=args, id=None)
    content = types.Content(role="model", parts=[types.Part(text="(tool request)")])
    return SimpleNamespace(function_calls=[call], text=None, candidates=[SimpleNamespace(content=content)])


def final_answer(text):
    """A fake model reply with a plain answer."""
    return SimpleNamespace(function_calls=None, text=text, candidates=[])


def fake_model(replies):
    """Return a stand-in for the model that gives the replies one by one."""
    queue = list(replies)
    sent = []

    def generate(contents, config):
        sent.append(len(contents))
        return queue.pop(0)

    generate.sent = sent
    return generate


def test_loop_runs_tool_then_returns_answer():
    model = fake_model([tool_request("calculator", {"expression": "17 * 23"}), final_answer("It is 391.")])
    agent = Agent(generate=model)
    assert agent.run("What is 17 * 23?") == "It is 391."
    assert [s["kind"] for s in agent.steps] == ["tool_call", "tool_result", "answer"]
    assert "391" in agent.steps[1]["text"]
    assert model.sent == [1, 3]  # second call carries: question, tool request, tool result


def test_no_tool_request_returns_answer_straight_away():
    agent = Agent(generate=fake_model([final_answer("Hello!")]))
    assert agent.run("Hi") == "Hello!"
    assert len(agent.steps) == 1


def test_step_limit_stops_the_loop():
    forever = [tool_request("get_time", {}) for _ in range(10)]
    agent = Agent(max_steps=3, generate=fake_model(forever))
    assert "Stopped after 3 steps" in agent.run("What time is it?")
    assert agent.steps[-1]["kind"] == "stopped"


def test_unknown_tool_does_not_crash():
    model = fake_model([tool_request("delete_everything", {}), final_answer("Sorry.")])
    agent = Agent(generate=model)
    assert agent.run("Do it") == "Sorry."
    assert "no tool called" in agent.steps[1]["text"]


def test_calculator_works():
    assert tools.run_tool("calculator", {"expression": "(12 + 8) * 3"}) == "60"
    assert tools.run_tool("calculator", {"expression": "2 ** 10 % 1000"}) == "24"
    assert tools.run_tool("calculator", {"expression": "-5 + 2.5"}) == "-2.5"


@pytest.mark.parametrize(
    "bad",
    [
        "__import__('os').system('echo hi')",
        "open('secret.txt')",
        "().__class__",
        "1 if True else 2",
        "[1, 2][0]",
        "abs(-1)",
        "'a' * 3",
        "True + 1",
        "9 ** 9 ** 9",
        "1 / 0",
        "2 +",
        "x + 1",
    ],
)
def test_calculator_rejects_anything_unsafe(bad):
    assert tools.run_tool("calculator", {"expression": bad}).startswith("Error")


def test_save_note_only_writes_to_notes_file(tmp_path, monkeypatch):
    notes = tmp_path / "notes" / "notes.txt"
    monkeypatch.setattr(tools, "NOTES_FILE", notes)
    tools.run_tool("save_note", {"text": "buy milk\n../../evil"})
    assert notes.read_text() == "buy milk ../../evil\n"
    assert [p.name for p in tmp_path.iterdir()] == ["notes"]


def test_declarations_come_from_type_hints():
    @tools.tool
    def demo(name: str, count: int, loud: bool = False):
        """Say hello.

        name: who to greet
        """

    declaration = tools.TOOLS["demo"]["declaration"]
    del tools.TOOLS["demo"]
    assert declaration["description"] == "Say hello."
    assert declaration["parameters"]["properties"]["count"]["type"] == "integer"
    assert declaration["parameters"]["properties"]["name"]["description"] == "who to greet"
    assert declaration["parameters"]["required"] == ["name", "count"]
