#!/usr/bin/env python3
"""PreToolUse: hỏi xác nhận trước khi sửa file BA đã duyệt (có trong baselines.csv)."""
import csv
import hashlib
import json
import os
import sys


def latest_baseline(csv_path, rel):
    row = None
    with open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("path") == rel:
                row = r
    return row


def main():
    try:
        tool_input = json.load(sys.stdin).get("tool_input") or {}
    except ValueError:
        return
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not path:
        return
    path = os.path.realpath(path)
    d = os.path.dirname(path)
    while d != os.path.dirname(d):
        csv_path = os.path.join(d, "baselines.csv")
        if os.path.isfile(csv_path):
            break
        d = os.path.dirname(d)
    else:
        return
    rel = os.path.relpath(path, d)
    try:
        row = latest_baseline(csv_path, rel)
    except (OSError, csv.Error):
        return
    if not row:
        return
    drift = ""
    if os.path.isfile(path):
        with open(path, "rb") as f:
            if hashlib.sha256(f.read()).hexdigest() != row.get("sha256"):
                drift = " File đã lệch so với baseline từ trước."
    reason = (
        f"{rel} đã duyệt (v{row.get('version')}, {row.get('approved_by')}, {row.get('date')}).{drift} "
        "Chỉ sửa khi có CR (/ba-start impact) và phải duyệt lại để có baseline mới."
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }}, ensure_ascii=False))


if __name__ == "__main__":
    main()
