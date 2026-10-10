# Agent skills: short notes

MLH says an agent skill "must comply with the Agent Skill Open Standard". This starter does not include a skill, and nothing here claims compliance. These notes only summarise the public spec so you know what to read.

Spec (read this, not these notes): https://agentskills.io/specification

In plain words:

- A skill is a folder. It must contain a file called `SKILL.md`. It may also have `scripts/`, `references/` and `assets/` folders.
- `SKILL.md` starts with a short settings block (called "frontmatter"), then instructions in Markdown.
- Two settings are required:
  - `name`: 1 to 64 characters, lowercase letters, numbers and hyphens only. It cannot start or end with a hyphen, cannot have two hyphens in a row, and must match the folder name.
  - `description`: 1 to 1024 characters. Say what the skill does and when to use it.
- Optional settings: `license`, `compatibility`, `metadata`, `allowed-tools`.
- The spec says to keep `SKILL.md` under 500 lines and to move long material into other files.
- The spec points to a checker called `skills-ref` (`skills-ref validate ./my-skill`).

If you build a skill, check it against the spec page on the day. The spec may change.
