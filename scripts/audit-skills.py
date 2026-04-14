#!/usr/bin/env python3
"""
audit-skills.py — Audit skill library của main repo + detect companion zones.

Usage:
    python scripts/audit-skills.py
    python scripts/audit-skills.py --json
"""

from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = PROJECT_ROOT / "scripts" / "manifest.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def count_skills(zone_path: Path) -> tuple[int, list[str]]:
    if not zone_path.exists():
        return 0, []
    skills = [p.name for p in zone_path.iterdir() if p.is_dir() and (p / "SKILL.md").exists()]
    return len(skills), sorted(skills)


def audit_main_skill() -> dict:
    skill_md = PROJECT_ROOT / "SKILL.md"
    exists = skill_md.exists()
    return {
        "name": "vci-skill-cuongbx (main)",
        "exists": exists,
        "path": str(skill_md),
        "size_lines": len(skill_md.read_text(encoding="utf-8").splitlines()) if exists else 0,
    }


def audit_local_zone(zone_name: str, zone_cfg: dict) -> dict:
    path = PROJECT_ROOT / zone_cfg["path"]
    count, skills = count_skills(path)
    return {
        "zone": zone_name,
        "description": zone_cfg["description"],
        "path": str(path),
        "count": count,
        "skills": skills[:5] + (["..."] if len(skills) > 5 else []),
        "status": "OK" if count > 0 else "EMPTY",
    }


def audit_companion(name: str, cfg: dict) -> dict:
    dest = PROJECT_ROOT / cfg["install_to"]
    count, skills = count_skills(dest)
    return {
        "companion": name,
        "description": cfg["description"],
        "url": cfg["url"],
        "install_to": cfg["install_to"],
        "installed": dest.exists(),
        "count": count,
        "status": "INSTALLED" if count > 0 else "NOT INSTALLED",
    }


def print_human(main: dict, local: list[dict], companions: list[dict]):
    print("=" * 60)
    print(f"Audit: {PROJECT_ROOT.name}")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    print(f"\n[MAIN] {main['name']}")
    print(f"  SKILL.md: {'OK' if main['exists'] else 'MISSING'} ({main['size_lines']} lines)")

    print("\n[LOCAL ZONES]")
    for z in local:
        icon = "[OK]" if z["status"] == "OK" else "[--]"
        print(f"  {icon} {z['zone']:12s} {z['count']} skills — {z['description']}")
        if z["skills"]:
            print(f"      {', '.join(z['skills'])}")

    print("\n[COMPANION REPOS]")
    for c in companions:
        icon = "[INSTALLED]" if c["installed"] else "[NOT INSTALLED]"
        print(f"  {icon} {c['companion']:12s} {c['count']} skills")
        print(f"      URL: {c['url']}")
        if not c["installed"]:
            print(f"      Install: bash scripts/install-companion.sh {c['companion']}")

    print("\n" + "=" * 60)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    mf = load_manifest()
    main_skill = audit_main_skill()
    local = [audit_local_zone(n, c) for n, c in mf["local_zones"].items()]
    companions = [audit_companion(n, c) for n, c in mf["companion_repos"].items()]

    if args.json:
        print(json.dumps({"main": main_skill, "local_zones": local, "companions": companions}, indent=2, ensure_ascii=False))
    else:
        print_human(main_skill, local, companions)


if __name__ == "__main__":
    main()
