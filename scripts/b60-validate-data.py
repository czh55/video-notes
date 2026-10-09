#!/usr/bin/env python3
"""校验 b60 DATA / shots 完整性。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

mp = json.loads((SCRIPTS / "b60-slug-map.json").read_text(encoding="utf-8"))
expected = {v["slug"]: k for k, v in mp.items()}

data: dict = {}
for name in (
    "b60_data_part1",
    "b60_data_part2",
    "b60_data_part3",
    "b60_data_part4",
    "b60_data_part5",
):
    try:
        mod = __import__(name)
        data.update(getattr(mod, "DATA", {}))
    except ImportError as e:
        print(f"import fail {name}: {e}")

missing = [s for s in expected if s not in data]
extra = [s for s in data if s not in expected]
print(f"DATA {len(data)}/{len(expected)} missing={len(missing)} extra={len(extra)}")
if missing[:10]:
    print(" missing sample:", missing[:10])

shot_ok = 0
shot_bad = []
for slug, key in expected.items():
    p = ROOT / f"shots-{slug}.json"
    if not p.exists():
        shot_bad.append(f"{slug}: no shots file")
        continue
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        shots = d.get("shots") or []
        if not shots:
            shot_bad.append(f"{slug}: empty shots")
            continue
        for s in shots:
            t = s.get("time", "")
            parts = t.split(":")
            if len(parts) != 2 or not (0 <= int(parts[1]) <= 59):
                shot_bad.append(f"{slug}: bad time {t}")
                break
        else:
            shot_ok += 1
    except Exception as e:
        shot_bad.append(f"{slug}: {e}")

print(f"shots ok {shot_ok}/{len(expected)} bad={len(shot_bad)}")
for b in shot_bad[:20]:
    print(" ", b)

# chapter quality spot-check
bad_titles = []
for slug, d in data.items():
    for c in d.get("chapters") or []:
        title = c.get("title") or ""
        if any(x in title for x in ("核心内容", "相关技巧", "操作演示", "要点详解")):
            bad_titles.append(f"{slug}: {title}")
print(f"generic titles: {len(bad_titles)}")
for b in bad_titles[:10]:
    print(" ", b)
