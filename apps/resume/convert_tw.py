#!/usr/bin/env python3
"""Convert the resume builder from Simplified Chinese to Taiwanese Traditional Chinese.

OpenCC handles the character and vocabulary conversion. OVERRIDES then fixes the
terms where Taiwan's job-hunting vocabulary differs from OpenCC's generic output,
and applies the deliberate field rename from 政治面貌 to 狀態.

Idempotent: running it twice produces the same file.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from opencc import OpenCC

HERE = Path(__file__).parent
TARGET = HERE / "index.html"

# Applied after OpenCC. Order matters: longer phrases first.
OVERRIDES: list[tuple[str, str]] = [
    # 台灣求職用語：履歷，不是簡歷
    ("簡歷生成器", "履歷生成器"),
    ("簡歷", "履歷"),
    # 常見詞彙差異
    ("實時預覽", "即時預覽"),
    ("實時", "即時"),
    ("歷史記錄", "歷史紀錄"),
    ("資格證書與技能", "證照與技能"),
    ("資格證書", "證照"),
    ("愛好與特長", "興趣與專長"),
    ("愛好", "興趣"),
    ("特長", "專長"),
    ("本地快取版", "本機快取版"),
    ("本地", "本機"),
    ("網路連線", "網路"),
    # 刻意的欄位語意改名，不是轉換
    ("政治面貌", "狀態"),
]

# Values that must match the resume-composer output schema exactly.
REQUIRED_ENUMS = ["實習經歷", "實踐經歷", "校園經歷"]

# These must survive untouched; a broken one silently breaks storage or layout.
GUARDS = [
    "resume_history",
    "resume_photo_latest",
    "resume_draft",
    "html2pdf",
    "careertown",
]


def convert(text: str) -> str:
    out = OpenCC("s2twp").convert(text)
    for src, dst in OVERRIDES:
        out = out.replace(src, dst)
    return out


def main() -> int:
    original = TARGET.read_text(encoding="utf-8")
    converted = convert(original)

    problems: list[str] = []

    remaining = re.findall(r"[一-鿿]", converted)
    simplified_markers = set("简历导个网资讯经历实习践园历执业务爱标签")
    leftover = sorted(simplified_markers.intersection(remaining))
    if leftover:
        problems.append(f"simplified characters remain: {''.join(leftover)}")

    for enum in REQUIRED_ENUMS:
        if enum not in converted:
            problems.append(f"missing required category enum: {enum}")

    for guard in GUARDS:
        if original.count(guard) != converted.count(guard):
            problems.append(
                f"guard {guard!r} count changed: "
                f"{original.count(guard)} -> {converted.count(guard)}"
            )

    if converted.count("<") != original.count("<"):
        problems.append("tag count changed; conversion touched markup")

    if problems:
        print("REFUSED, file unchanged:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    if converted == original:
        print("already converted, no change")
        return 0

    TARGET.write_text(converted, encoding="utf-8")
    print(f"converted {TARGET} ({len(original)} -> {len(converted)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
