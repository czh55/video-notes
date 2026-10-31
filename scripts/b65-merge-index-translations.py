#!/usr/bin/env python3
"""合并 _work/b65/index-entries 与 translations-partial 到 docs/index.json 与 translations.json"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDX = ROOT / "docs" / "index.json"
TR = ROOT / "translations.json"
ENT = ROOT / "_work" / "b65" / "index-entries"
PART = ROOT / "_work" / "b65" / "translations-partial"

def main() -> None:
    idx = json.loads(IDX.read_text(encoding="utf-8"))
    by_slug = {it.get("slug"): i for i, it in enumerate(idx)}
    by_url = {it.get("url"): i for i, it in enumerate(idx)}
    added = updated = 0
    for p in sorted(ENT.glob("*.json")):
        ent = json.loads(p.read_text(encoding="utf-8"))
        slug, url = ent.get("slug"), ent.get("url")
        if url and url in by_url:
            idx[by_url[url]] = ent
            updated += 1
        elif slug and slug in by_slug:
            idx[by_slug[slug]] = ent
            updated += 1
        else:
            idx.insert(0, ent)
            added += 1
            by_slug = {it.get("slug"): i for i, it in enumerate(idx)}
            by_url = {it.get("url"): i for i, it in enumerate(idx)}
    IDX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    tr = json.loads(TR.read_text(encoding="utf-8"))
    t_add = 0
    for p in sorted(PART.glob("*.json")):
        part = json.loads(p.read_text(encoding="utf-8"))
        for k, v in part.items():
            if k not in tr:
                tr[k] = v
                t_add += 1
            elif not tr[k] and v:
                tr[k] = v
                t_add += 1
    TR.write_text(json.dumps(tr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"index +{added} ~{updated}; translations keys touched ~{t_add}; index len={len(idx)}")

if __name__ == "__main__":
    main()
