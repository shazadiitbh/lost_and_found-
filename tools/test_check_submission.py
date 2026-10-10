"""Tests for check_submission.py. They build small fake projects in temporary folders.

Run from the repo root:  python -m pytest tools
"""

import check_submission as cs

MIT = "MIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\n"
FAKE_KEY = "AIza" + "x" * 35  # built in pieces so this file never contains a real-looking key
GOOD_README = "# App\nUses gemma-4-26b-a4b-it.\n## How to run\nRun it.\n![screenshot](shot.png)\n"


def make_project(tmp_path, **overrides):
    files = {
        "LICENSE": MIT,
        "README.md": GOOD_README,
        ".gitignore": ".env\n",
        "shot.png": "x",
        "app.py": "from google import genai\nMODEL = 'gemma-4-26b-a4b-it'\n",
    }
    files.update(overrides)
    for name, content in files.items():
        if content is not None:
            (tmp_path / name).write_text(content)
    return tmp_path


def statuses(root):
    return {name: status for name, status, *_ in cs.run_checks(root)}


def test_good_project_has_no_fail(tmp_path):
    result = statuses(make_project(tmp_path))
    assert "FAIL" not in result.values()
    assert result["License"] == "PASS"


def test_missing_license_fails(tmp_path):
    assert statuses(make_project(tmp_path, LICENSE=None))["License"] == "FAIL"


def test_unknown_license_fails(tmp_path):
    assert statuses(make_project(tmp_path, LICENSE="All rights reserved."))["License"] == "FAIL"


def test_other_licenses_are_recognised(tmp_path):
    for text in ("Apache License\nVersion 2.0, January 2004", "GNU GENERAL PUBLIC LICENSE", "Mozilla Public License"):
        assert statuses(make_project(tmp_path, LICENSE=text))["License"] == "PASS"


def test_readme_without_model_fails(tmp_path):
    result = statuses(make_project(tmp_path, **{"README.md": "# App\n## How to run\n![s](shot.png)\n"}))
    assert result["README model"] == "FAIL"


def test_ollama_only_code_warns(tmp_path):
    result = statuses(make_project(tmp_path, **{"app.py": "url = 'http://localhost:11434'\nm = 'gemma-4-26b-a4b-it'\n"}))
    assert result["Gemini API"] == "WARN"


def test_code_without_gemma_fails(tmp_path):
    assert statuses(make_project(tmp_path, **{"app.py": "print('hi')\n"}))["Gemini API"] == "FAIL"


def test_api_key_in_file_fails_and_is_masked(tmp_path):
    root = make_project(tmp_path, notes_file=f"key = {FAKE_KEY}\n")
    _, status, message, _ = next(r for r in cs.run_checks(root) if r[0] == "API key safety")
    assert status == "FAIL"
    assert "notes_file:1" in message
    assert FAKE_KEY not in message and "xxxx" not in message


def test_env_file_itself_is_not_scanned(tmp_path):
    root = make_project(tmp_path, **{".env": f"GEMINI_API_KEY={FAKE_KEY}\n"})
    assert statuses(root)["API key safety"] != "FAIL"


def test_gitignore_must_list_env(tmp_path):
    assert statuses(make_project(tmp_path, **{".gitignore": "__pycache__/\n"}))[".gitignore"] == "FAIL"


def test_readme_needs_run_section_and_screenshot(tmp_path):
    assert statuses(make_project(tmp_path, **{"README.md": "gemma-4-26b-a4b-it\n"}))["README sections"] == "FAIL"
    assert statuses(make_project(tmp_path, **{"README.md": GOOD_README.replace("shot.png", "nope.png")}))["README sections"] == "FAIL"


def test_screenshot_link_from_the_web_is_accepted(tmp_path):
    readme = "gemma-4-26b-a4b-it\n## How to run\n![s](https://example.com/s.png)\n"
    assert statuses(make_project(tmp_path, **{"README.md": readme}))["README sections"] == "PASS"


def test_main_exit_code(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["check_submission.py", str(make_project(tmp_path))])
    assert cs.main() == 0
    (tmp_path / "LICENSE").unlink()
    assert cs.main() == 1
