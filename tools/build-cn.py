#!/usr/bin/env python3
import csv
import os
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
dist = root / "dist"
translations = {}
with (root / "translations.tsv").open(encoding="utf-8") as f:
    for row in csv.reader((line for line in f if not line.startswith("#")), delimiter="\t"):
        if len(row) == 3:
            translations[(row[0], row[1])] = row[2]

for name in ("install.sh", "x-ui.sh"):
    source = dist / f"upstream-{name}"
    target = dist / ("install-cn.sh" if name == "install.sh" else "x-ui-cn.sh")
    text = source.read_text(encoding="utf-8")
    for (file_name, original), chinese in translations.items():
        if file_name == name:
            text = text.replace(original, chinese)
    target.write_text(text, encoding="utf-8", newline="\n")
    os.chmod(target, 0o755)

# Guard against accidentally translating code identifiers or URLs.
for path in (dist / "install-cn.sh", dist / "x-ui-cn.sh"):
    text = path.read_text(encoding="utf-8")
    if "https://raw.githubusercontent.com/MHSanaei/3x-ui" not in text:
        raise SystemExit(f"upstream URL missing from {path}")
    if "#!/bin/bash" not in text:
        raise SystemExit(f"invalid shell script: {path}")
print("Chinese scripts generated successfully")
