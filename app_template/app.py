"""Campus Lost & Found: Gemma 4 extracts item details; Python ranks matches.

Run from the repository root: python app_template/app.py
Each report makes one Gemma 4 request. Reports live only in this browser
session; uploaded photos and personal contact information are not saved.
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gradio as gr

import gemma_client

TITLE = "Campus Lost & Found"
MODEL = "gemma-4-26b-a4b-it"
SYSTEM_RULE = (
    "Extract observable details from a student's lost or found item report. "
    "If there is a photo, describe only the item visible; never identify a person. "
    "Do not invent details. Return exactly one JSON object with string fields: "
    "category, color, keywords, summary. Use an empty string when unknown. "
    "Keep summary under 25 words."
)
LOCATIONS = ["Library", "Cafeteria", "Main building", "Computer lab", "Sports ground", "Hostel", "Other / not sure"]
DEFAULT_WHEN = datetime.now().strftime("%Y-%m-%d %H:%M")


def _demo_time(days_ago, hours=12):
    return (datetime.now() - timedelta(days=days_ago)).replace(
        hour=hours, minute=0, second=0, microsecond=0
    ).isoformat(timespec="minutes")


# Synthetic demo reports; no real names, contact details, or photos.
DEMO_REPORTS = [
    {"id": "F-101", "type": "found", "category": "water bottle", "color": "blue", "keywords": "steel reusable bottle", "description": "Blue steel bottle found near the second-floor reading tables.", "location": "Library", "when": _demo_time(1), "held_at": "Library security desk"},
    {"id": "L-102", "type": "lost", "category": "wallet", "color": "brown", "keywords": "small wallet lunch counter", "description": "Small brown wallet, possibly left near the lunch counter.", "location": "Cafeteria", "when": _demo_time(2), "held_at": ""},
    {"id": "F-103", "type": "found", "category": "umbrella", "color": "black", "keywords": "folding umbrella entrance", "description": "Black folding umbrella found by the main building entrance.", "location": "Main building", "when": _demo_time(1, 15), "held_at": "Main building security desk"},
    {"id": "L-104", "type": "lost", "category": "water bottle", "color": "blue", "keywords": "reusable bottle studying", "description": "Blue reusable bottle missing after studying in the library.", "location": "Library", "when": _demo_time(1, 13), "held_at": ""},
    {"id": "F-105", "type": "found", "category": "notebook", "color": "red", "keywords": "spiral notebook desk", "description": "Red spiral notebook found on a desk in the computer lab.", "location": "Computer lab", "when": _demo_time(3), "held_at": "Computer lab office"},
    {"id": "L-106", "type": "lost", "category": "earbuds case", "color": "white", "keywords": "earbuds case sports ground", "description": "White earbuds case lost somewhere near the sports ground.", "location": "Sports ground", "when": _demo_time(1), "held_at": ""},
]

STOP_WORDS = {"a", "an", "the", "i", "my", "me", "it", "is", "was", "were", "near", "at", "in", "on", "of", "and", "or", "to", "for", "with", "found", "lost", "item"}
NEARBY = {
    frozenset(("Library", "Computer lab")),
    frozenset(("Cafeteria", "Main building")),
    frozenset(("Hostel", "Sports ground")),
}


def _parse_details(text):
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("Gemma's response was not in the expected format. Please try again.")
    data = json.loads(match.group(0))
    fields = ("category", "color", "keywords", "summary")
    return {field: str(data.get(field, "")).strip()[:160] for field in fields}


def _tokens(text):
    return {word for word in re.findall(r"[a-z0-9]+", text.lower()) if word not in STOP_WORDS}


def _attribute_score(new, old):
    """Gemma-extracted category/color agreement (0 to 1)."""
    category_a, category_b = new["category"].lower(), old["category"].lower()
    color_a, color_b = new["color"].lower(), old["color"].lower()
    category = 1.0 if category_a and category_b and (category_a in category_b or category_b in category_a) else 0.0
    color = 1.0 if color_a and color_b and color_a == color_b else 0.0
    known_weight = (0.75 if category_a and category_b else 0.0) + (0.25 if color_a and color_b else 0.0)
    if not known_weight:
        return 0.0
    return ((0.75 * category) + (0.25 * color)) / known_weight


def _text_score(new, old):
    a = _tokens(" ".join((new.get("keywords", ""), new.get("summary", ""))))
    b = _tokens(" ".join((old.get("keywords", ""), old.get("description", ""))))
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def _location_score(a, b):
    if not a or not b or a == "Other / not sure" or b == "Other / not sure":
        return 0.0
    if a == b:
        return 1.0
    return 0.5 if frozenset((a, b)) in NEARBY else 0.0


def _time_score(when_a, when_b):
    try:
        a = datetime.fromisoformat(when_a)
        b = datetime.fromisoformat(when_b)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, 1.0 - abs((a - b).total_seconds()) / (7 * 24 * 60 * 60))


def _rank_matches(new_report, reports):
    """Weighted prototype score: item details .40, text .30, location .15, time .15."""
    opposite = "found" if new_report["type"] == "lost" else "lost"
    weights = (0.40, 0.30, 0.15, 0.15)
    ranked = []
    for report in reports:
        if report["type"] != opposite:
            continue
        values = (
            _attribute_score(new_report, report),
            _text_score(new_report, report),
            _location_score(new_report["location"], report["location"]),
            _time_score(new_report["when"], report["when"]),
        )
        score = sum(value * weight for value, weight in zip(values, weights))
        if score > 0:
            ranked.append((score, report, values))
    ranked.sort(key=lambda item: item[0], reverse=True)
    labels = ("Gemma item details (40%)", "Text overlap (30%)", "Location proximity (15%)", "Time proximity (15%)")
    return [
        {
            "Report ID": report["id"],
            "Type": report["type"],
            "Match score (prototype, not a probability)": round(score * 100),
            "Description": report["description"],
            "Area": report["location"],
            "When": report["when"].replace("T", " "),
            "Currently kept at": report["held_at"] or "Not specified",
            "Score breakdown": {label: round(value * 100) for label, value in zip(labels, values)},
        }
        for score, report, values in ranked[:3]
    ]


def report_and_match(report_type, description, location, when, held_at, image_path, reports):
    """Extract report details with one Gemma call; score matches locally."""
    if not description.strip() and not image_path:
        return "Add a short description or item photo first.", None, reports
    try:
        parsed_when = datetime.strptime(when.strip(), "%Y-%m-%d %H:%M").isoformat(timespec="minutes")
    except (AttributeError, ValueError):
        return "Enter date and time as YYYY-MM-DD HH:MM, for example 2026-10-10 14:30.", None, reports
    prompt = (
        f"Report type: {report_type}. Area selected by user: {location}.\n"
        f"Description: {description.strip() or '(No text description; inspect the item photo.)'}\n"
        "Extract category, color, keywords, and a short summary for matching reports. "
        "Do not infer personal identity or invent missing details. Return the JSON object only."
    )
    try:
        if image_path:
            response = gemma_client.ask_with_image(image_path, prompt, system=SYSTEM_RULE)
        else:
            response = gemma_client.ask(prompt, system=SYSTEM_RULE)
        details = _parse_details(response)
    except Exception as error:
        return gemma_client.describe_error(error), None, reports

    updated = list(reports or DEMO_REPORTS)
    report = {
        "id": f"R-{len(updated) + 1:03d}",
        "type": report_type,
        **details,
        "description": description.strip() or details["summary"],
        "location": location,
        "when": parsed_when,
        "held_at": held_at.strip() if report_type == "found" else "",
    }
    matches = _rank_matches(report, updated)
    updated.append(report)
    result = {
        "Your report": {
            "Report ID": report["id"], "Type": report_type,
            "Gemma 4 extracted": details, "Area": location,
            "When": parsed_when.replace("T", " "),
            "Currently kept at": report["held_at"] or "Not applicable for lost-item reports",
        },
        "Top opposite-type matches": matches,
        "Score note": "Prototype heuristic, not a probability. Review details and verify ownership with campus staff.",
        "Session report count": len(updated) - len(DEMO_REPORTS),
    }
    return f"Report {report['id']} added to this session. Found {len(matches)} possible match(es).", result, updated


with gr.Blocks(title=TITLE) as demo:
    reports_state = gr.State(DEMO_REPORTS)
    gr.Markdown(
        "# Campus Lost & Found\n"
        "Report an item and compare it with opposite-type reports. Gemma 4 extracts item details; "
        "Python ranks candidates by item details, text, location, and time."
    )
    with gr.Row():
        report_type = gr.Radio(["lost", "found"], value="lost", label="Report type")
        location = gr.Dropdown(LOCATIONS, value="Library", label="Where was it lost / found?")
    description = gr.Textbox(
        label="Short description",
        placeholder="Example: Blue steel water bottle near the library reading tables.",
        lines=2,
    )
    with gr.Row():
        when = gr.Textbox(label="When? (YYYY-MM-DD HH:MM)", value=DEFAULT_WHEN)
        held_at = gr.Textbox(label="If found: where is it kept? (e.g. security desk)")
    photo = gr.Image(type="filepath", label="Item photo (optional)", height=220)
    submit = gr.Button("Submit report and find matches", variant="primary")
    status = gr.Markdown()
    results = gr.JSON(label="Report and ranked possible matches")
    gr.Markdown(
        "**Prototype:** reports reset when this page reloads; notifications and staff dashboard are not included. "
        "Scores are heuristic, not probabilities. Use synthetic data only. Photos are sent to Google for Gemma analysis "
        "but are not saved by this app. Never upload faces, ID cards, private messages, names, or contact details. "
        "Verify ownership with campus staff before returning an item."
    )
    submit.click(
        report_and_match,
        [report_type, description, location, when, held_at, photo, reports_state],
        [status, results, reports_state],
    )


if __name__ == "__main__":
    print("Starting Campus Lost & Found — open the local URL shown below")
    demo.launch(share=False)
