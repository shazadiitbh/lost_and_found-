# The two challenges

One project can enter both. In MLH's OrganizerHQ, tick both challenges when you submit.

## Side by side

| | Best Use of Gemma 4 | Best Open-Source AI Project |
|---|---|---|
| **What it asks** | See how much you can build with a lightweight, open model reached through the Gemini API. | Build an original project where open-source or open-weight AI is an important part of how it works. |
| **What judges check** | That the project uses a Gemma model through the Gemini API. Running Gemma only on your own computer does not count. | That open-source or open-weight AI is important to the project, the GitHub repo is public with an open-source license, and the work is original. |
| **What you must show** | The model name in your README, and the integration in your code or in your demo. | A public GitHub repo with an open-source license. For an agent skill: it follows the Agent Skill Open Standard. For a harness: an original implementation or meaningful changes to an existing open-source one. |

## MLH's own words

**Best Use of Gemma 4:** "It's time to see how much you can build with a lightweight, open model. Gemma 4 packs multimodal intelligence into an open-weights model that you can access through the Gemini API. What can Gemma 4 bring to your project? Multimodal Experience: work with text and images to create an assistant that understands more of what users share. Focused AI Tools: build a focused AI tool for learning, creativity, productivity, or your community. Rapid Prototyping: experiment with an open model while using the Gemini API to move quickly from an idea to a working prototype."

**Best Open-Source AI Project:** "Build an original project that uses open-source or open-weight AI as an important part of how it works. Teams could create an agent skill, build with an open-weight large or small language model, or build or adapt an open-source model harness. These are examples within one challenge, and teams may combine them. Open-source or open-weight AI must be an important part of the project. The project must be published in a public GitHub repository and use an open-source license. An agent skill must comply with the Agent Skill Open Standard. A model-harness entry must include an original implementation or meaningful changes to an existing open-source harness."

If you are unsure about anything here, read the rules page on the day.

## How one project enters both

Gemma 4 is an open-weight model. So a project that calls Gemma 4 through the Gemini API, is built today, and sits in a public GitHub repo with an open-source license can fit both challenges. This starter already gives you the MIT license and the Gemini API call.

## Combined checklist

- [ ] Gemma 4 is called through the Gemini API (not only run locally).
- [ ] Your README names the model (for example `gemma-4-26b-a4b-it`) and shows the line of code that calls it.
- [ ] Gemma is an important part of how your project works, not a small extra.
- [ ] The work is original, and built today.
- [ ] The GitHub repo is public and has an open-source license (keep `LICENSE`).
- [ ] If you built a harness: you can explain what you added or changed (see `harness/README.md`).
- [ ] If you built an agent skill: it follows the Agent Skill Open Standard (see `docs/AGENT_SKILL_NOTES.md`; this starter does not include a skill).
- [ ] `python tools/check_submission.py` has no FAIL.
- [ ] Submitted in OrganizerHQ with both challenges ticked.
