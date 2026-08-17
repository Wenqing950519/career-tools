#!/usr/bin/env python3
"""Validate one Career Town skill response with Python standard library only."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


RULES = {
    "direction-explorer": {"type": "direction", "min": 2, "max": 4},
    "experience-curator": {"type": "experience", "min": 0, "max": 1},
    "skill-gap": {"type": "skill", "min": 0, "max": None},
    "opportunity-review": {"type": "opportunity", "min": 0, "max": 1},
    "resume-composer": {"type": "resume_draft", "min": 0, "max": 1},
    "interview-story": {"type": "interview_story", "min": 0, "max": 1},
}

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
CHAT_SOURCE = re.compile(r"chat-[1-9]\d*")


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def extract(text: str) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    matches = list(re.finditer(r"```careertown\s*(\{.*?\})\s*```", text, re.S))
    if len(matches) != 1:
        return None, [f"expected exactly one careertown block, found {len(matches)}"]
    if text[matches[0].end():].strip():
        errors.append("careertown block must be the final response content")
    try:
        return json.loads(matches[0].group(1)), errors
    except json.JSONDecodeError as exc:
        return None, errors + [f"invalid JSON: {exc}"]


def validate(skill: str, payload: Any, context: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["envelope must be an object"]
    expected = {"schema_version", "skill", "generated_at", "records", "unknowns"}
    if set(payload) != expected:
        errors.append("envelope keys must be exactly: " + ", ".join(sorted(expected)))
    if payload.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    if payload.get("skill") != skill:
        errors.append(f"skill must equal {skill}")
    if not DATETIME.fullmatch(str(payload.get("generated_at", ""))):
        errors.append("generated_at must be an RFC3339 UTC timestamp")
    records = payload.get("records")
    unknowns = payload.get("unknowns")
    if not isinstance(records, list):
        return errors + ["records must be an array"]
    if not isinstance(unknowns, list) or any(not nonempty(x) for x in unknowns):
        errors.append("unknowns must be an array of non-empty strings")
    elif len(unknowns) != len(set(unknowns)):
        errors.append("unknowns must be unique")
    rule = RULES[skill]
    if len(records) < rule["min"] or (rule["max"] is not None and len(records) > rule["max"]):
        errors.append(f"records count must be {rule['min']}..{rule['max'] if rule['max'] is not None else 'unbounded'}")
    for i, record in enumerate(records):
        path = f"records[{i}]"
        if not isinstance(record, dict) or set(record) != {"type", "status", "data"}:
            errors.append(f"{path} must contain exactly type, status, data")
            continue
        if record.get("type") != rule["type"]:
            errors.append(f"{path}.type must equal {rule['type']}")
        if record.get("status") != "pending":
            errors.append(f"{path}.status must equal pending")
        data = record.get("data")
        if not isinstance(data, dict):
            errors.append(f"{path}.data must be an object")
            continue
        if "confirmation_status" in data and data["confirmation_status"] != "pending":
            errors.append(f"{path}.data.confirmation_status must equal pending")
        validate_data(skill, data, path + ".data", errors)
        validate_identity(skill, data, i, path + ".data", errors, context or {})
    record_ids = [record.get("data", {}).get("id") for record in records if isinstance(record, dict) and isinstance(record.get("data"), dict)]
    if len(record_ids) != len(set(record_ids)):
        errors.append("record data IDs must be unique")
    if skill == "direction-explorer" and records:
        attentions = [r.get("data", {}).get("attention") for r in records if isinstance(r, dict)]
        if not all(isinstance(x, int) and not isinstance(x, bool) for x in attentions) or sum(attentions) != 100:
            errors.append("direction attention values must be integers totaling 100")
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    if re.search(r'"(?:fit_score|recommendation_score|total_score|personality_type)"\s*:', serialized):
        errors.append("forbidden score or classification field detected")
    return errors


def validate_data(skill: str, data: dict[str, Any], path: str, errors: list[str]) -> None:
    def require(*fields: str) -> None:
        for field in fields:
            if field not in data:
                errors.append(f"{path}.{field} is required")

    if skill == "direction-explorer":
        require("id", "title", "status", "attention", "reasons", "related_skills", "related_experiences", "recent_change", "updated_at")
        if data.get("status") != "observing": errors.append(f"{path}.status must equal observing")
        if not nonempty(data.get("id")) or not nonempty(data.get("title")): errors.append(f"{path} requires non-empty id and title")
        if not isinstance(data.get("reasons"), list) or len(data.get("reasons", [])) < 2: errors.append(f"{path}.reasons requires at least two items")
        if not nonempty(data.get("recent_change")): errors.append(f"{path}.recent_change must be non-empty")
    elif skill in {"experience-curator", "interview-story"}:
        require("id", "title", "raw_text", "summary", "skills", "resume_text", "confirmation_status", "created_at", "sections")
        for field in ("id", "title", "raw_text", "summary", "resume_text"):
            if not nonempty(data.get(field)): errors.append(f"{path}.{field} must be non-empty")
        sections = data.get("sections")
        if not isinstance(sections, dict) or set(sections) != {"background", "actions", "results", "contribution", "unknowns"}:
            errors.append(f"{path}.sections has invalid shape")
        if skill == "interview-story" and not nonempty(data.get("source")):
            errors.append(f"{path}.source must be a confirmed experience ID")
    elif skill == "skill-gap":
        require("id", "title", "level", "learning_feeling", "related_directions", "assessment_note", "next_practice", "updated_at")
        if not isinstance(data.get("level"), int) or not 1 <= data["level"] <= 4: errors.append(f"{path}.level must be 1..4")
        for field in ("id", "title", "learning_feeling", "assessment_note", "next_practice"):
            if not nonempty(data.get(field)): errors.append(f"{path}.{field} must be non-empty")
    elif skill == "opportunity-review":
        require("id", "title", "organization", "bucket", "deadline", "summary", "directions", "source_url", "confirmation_status")
        for field in ("id", "title", "organization", "summary"):
            if not nonempty(data.get(field)): errors.append(f"{path}.{field} must be non-empty")
        if isinstance(data.get("summary"), str) and len(data["summary"]) < 40: errors.append(f"{path}.summary must contain at least 40 characters")
        if data.get("deadline") is not None and not DATE.fullmatch(str(data["deadline"])): errors.append(f"{path}.deadline must be YYYY-MM-DD or null")
    elif skill == "resume-composer":
        require("photo", "name", "birthDate", "phone", "politicalStatus", "email", "city", "certifications", "skills", "hobbies", "education", "experiences")
        experiences = data.get("experiences")
        if not isinstance(experiences, list) or not experiences: errors.append(f"{path}.experiences requires at least one entry")
        else:
            for j, item in enumerate(experiences):
                if not isinstance(item, dict) or not nonempty(item.get("sourceId")): errors.append(f"{path}.experiences[{j}].sourceId must be non-empty")
            chat_ids = [m.group(0) for item in experiences if isinstance(item, dict)
                        for m in [CHAT_SOURCE.fullmatch(str(item.get("sourceId", "")))] if m]
            if chat_ids:
                expected = [f"chat-{n}" for n in range(1, len(chat_ids) + 1)]
                if sorted(chat_ids, key=lambda s: int(s.split("-")[1])) != expected:
                    errors.append(f"{path}.experiences standalone sourceIds must be chat-1..chat-N without gaps or duplicates")


def validate_identity(
    skill: str,
    data: dict[str, Any],
    index: int,
    path: str,
    errors: list[str],
    context: dict[str, Any],
) -> None:
    """Enforce deterministic fallback IDs and optional invocation provenance."""
    injected_ids = context.get("injected_ids", [])
    if not isinstance(injected_ids, list) or any(not nonempty(x) for x in injected_ids):
        errors.append("context.injected_ids must be an array of non-empty strings")
        injected_ids = []

    expected: str | None = None
    if skill == "direction-explorer":
        expected = f"direction:{index + 1}"
    elif skill == "experience-curator":
        expected = "experience:1"
    elif skill == "skill-gap" and nonempty(data.get("title")):
        expected = f"skill:{data['title']}"
    elif skill == "opportunity-review" and nonempty(data.get("organization")) and nonempty(data.get("title")):
        expected = f"opportunity:{data['organization']}:{data['title']}"
    elif skill == "interview-story" and nonempty(data.get("source")):
        question_type = context.get("question_type")
        if question_type is not None and not nonempty(question_type):
            errors.append("context.question_type must be a non-empty string")
        if nonempty(question_type):
            expected = f"story:{data['source']}:{question_type}"
        elif not str(data.get("id", "")).startswith(f"story:{data['source']}:"):
            errors.append(f"{path}.id must use story:<source>:<question type>; pass --context to verify the exact question type")

    if injected_ids:
        if data.get("id") not in injected_ids:
            errors.append(f"{path}.id must reuse an ID declared in context.injected_ids")
    elif expected is not None and data.get("id") != expected:
        errors.append(f"{path}.id must equal deterministic fallback {expected!r}")

    confirmed_ids = context.get("confirmed_source_ids")
    if confirmed_ids is not None:
        if not isinstance(confirmed_ids, list) or any(not nonempty(x) for x in confirmed_ids):
            errors.append("context.confirmed_source_ids must be an array of non-empty strings")
            return
        if skill == "resume-composer":
            for j, item in enumerate(data.get("experiences", [])):
                if isinstance(item, dict) and item.get("sourceId") not in confirmed_ids:
                    errors.append(f"{path}.experiences[{j}].sourceId is not in context.confirmed_source_ids")
        elif skill == "interview-story" and data.get("source") not in confirmed_ids:
            errors.append(f"{path}.source is not in context.confirmed_source_ids")


def semantic_value(value: Any) -> Any:
    """Remove generation timestamps recursively for repeat-run comparison."""
    if isinstance(value, dict):
        return {key: semantic_value(item) for key, item in value.items() if key not in {"generated_at", "created_at", "updated_at"}}
    if isinstance(value, list):
        return [semantic_value(item) for item in value]
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("response", type=Path)
    parser.add_argument("--skill", choices=sorted(RULES))
    parser.add_argument("--context", type=Path, help="optional invocation context JSON with injected_ids, confirmed_source_ids, and question_type")
    args = parser.parse_args()
    skill = args.skill or Path(__file__).resolve().parents[1].name
    if skill not in RULES:
        print(f"ERROR: unsupported skill {skill}", file=sys.stderr)
        return 2
    text = args.response.read_text(encoding="utf-8")
    payload, errors = extract(text)
    context: dict[str, Any] | None = None
    if args.context:
        try:
            loaded = json.loads(args.context.read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                errors.append("context must be a JSON object")
            else:
                context = loaded
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid context JSON: {exc}")
    if payload is not None:
        errors.extend(validate(skill, payload, context))
    if errors:
        for error in errors: print("ERROR:", error, file=sys.stderr)
        return 1
    canonical = semantic_value({"skill": payload["skill"], "records": payload["records"], "unknowns": payload["unknowns"]})
    fingerprint = hashlib.sha256(json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    print(f"OK: {skill} response valid ({fingerprint})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
