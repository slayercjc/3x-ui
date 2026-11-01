#!/usr/bin/env python3
import csv
import json
import os
import re
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[1]
tsv = root / "translations.tsv"
api_key = os.environ.get("GOOGLE_TRANSLATE_API_KEY")
if not api_key:
    raise SystemExit("GOOGLE_TRANSLATE_API_KEY is not configured")

rows = []
known = set()
with tsv.open(encoding="utf-8") as f:
    for row in csv.reader((line for line in f if not line.startswith("#")), delimiter="\t"):
        if len(row) == 3:
            rows.append(row)
            known.add((row[0], row[1]))

def translate(text):
    request = urllib.request.Request(
        "https://translation.googleapis.com/language/translate/v2",
        data=json.dumps({"q": text, "source": "en", "target": "zh-CN", "format": "text"}).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    return data["data"]["translations"][0]["translatedText"]

for name in ("install.sh", "x-ui.sh"):
    text = (root / "dist" / f"upstream-{name}").read_text(encoding="utf-8")
    for line in text.splitlines():
        if not re.search(r"\b(echo|read|confirm)\b", line):
            continue
        # Only collect ordinary quoted display strings; skip URLs and shell substitutions.
        for match in re.findall(r'(?:(?:read|echo|confirm)[^\n]*?)?["\']([^"\']{8,})["\']', line):
            if "$" in match or "http" in match or "=" in match:
                continue
            if (name, match) not in known and re.search(r"[A-Za-z]{3,}", match):
                print(f"Translating new prompt in {name}: {match}")
                rows.append([name, match, translate(match)])
                known.add((name, match))

with tsv.open("w", encoding="utf-8", newline="") as f:
    f.write("# 文件名<TAB>原文<TAB>中文\n")
    writer = csv.writer(f, delimiter="\t", lineterminator="\n")
    writer.writerows(rows)
