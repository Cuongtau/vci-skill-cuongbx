#!/usr/bin/env python3
"""
audit-skills.py — Audit skill library: count, diff, missing, outdated.

Usage:
    python scripts/audit-skills.py                  # full audit
    python scripts/audit-skills.py --zone vci       # specific zone
    python scripts/audit-skills.py --diff-global    # compare with global
    python scripts/audit-skills.py --json           # machine-readable
"""

from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 for Vietnamese chars on Windows
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = PROJECT_ROOT / "scripts" / "manifest.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def expand_path(p: str) -> Path:
    return Path(p.replace("~", str(Path.home())))


def count_skills(zone_path: Path) -> tuple[int, list[str]]:
    """Count direct subfolders that have SKILL.md."""
    if not zone_path.exists():
        return 0, []
    skills = []
    for item in zone_path.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append(item.name)
    return len(skills), sorted(skills)


def hash_skill(skill_path: Path) -> str:
    """Compute hash of skill folder content (just SKILL.md for speed)."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return ""
    return hashlib.sha256(skill_md.read_bytes()).hexdigest()[:12]


def audit_zone(zone_name: str, zone_config: dict, diff_global: bool = False) -> dict:
    local_path = PROJECT_ROOT / zone_config["path"]
    local_count, local_skills = count_skills(local_path)

    result = {
        "zone": zone_name,
        "description": zone_config["description"],
        "local_path": str(local_path),
        "local_count": local_count,
        "expected_count": zone_config["skills_count"],
        "git_tracked": zone_config["git_tracked"],
        "sync_direction": zone_config["sync_direction"],
        "skills": local_skills[:5] + (["..."] if len(local_skills) > 5 else []),
        "status": "OK" if local_count > 0 else "EMPTY",
    }

    if diff_global and zone_config.get("global_path"):
        global_path = expand_path(zone_config["global_path"])
        global_count, global_skills = count_skills(global_path)
        excluded = zone_config.get("exclude_patterns", [])
        global_skills_filtered = [s for s in global_skills if s not in excluded]

        only_local = sorted(set(local_skills) - set(global_skills_filtered))
        only_global = sorted(set(global_skills_filtered) - set(local_skills))

        result["global_count"] = len(global_skills_filtered)
        result["only_local"] = only_local[:10]
        result["only_global"] = only_global[:10]
        result["in_sync"] = len(only_local) == 0 and len(only_global) == 0

    return result


def print_human(audits: list[dict]):
    print("=" * 60)
    print("Skill Library Audit Report")
    print(f"Project: {PROJECT_ROOT.name}")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    total_local = 0
    for a in audits:
        emoji = {"vci": "[VCI]", "claudekit": "[CK]", "xia": "[XIA]", "others": "[OTH]"}.get(a["zone"], "[??]")
        status_icon = "[OK]" if a["status"] == "OK" else "[!!]"
        tracked = "git-tracked" if a["git_tracked"] else "gitignored"
        print(f"\n{emoji} Zone: {a['zone']:12s} {status_icon} ({tracked})")
        print(f"  {a['description']}")
        print(f"  Local count: {a['local_count']} (expected ~{a['expected_count']})")
        if a["local_count"] != a["expected_count"]:
            delta = a["local_count"] - a["expected_count"]
            print(f"  Delta: {'+' if delta > 0 else ''}{delta}")
        if a["skills"]:
            print(f"  Skills: {', '.join(a['skills'])}")

        if "global_count" in a:
            sync_icon = "OK" if a["in_sync"] else "DRIFT"
            print(f"  Global count: {a['global_count']} | Status: {sync_icon}")
            if a["only_local"]:
                print(f"  Only local: {', '.join(a['only_local'])}")
            if a["only_global"]:
                print(f"  Only global: {', '.join(a['only_global'])}")

        total_local += a["local_count"]

    print("\n" + "=" * 60)
    print(f"TOTAL: {total_local} skills across {len(audits)} zones")
    print("=" * 60)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zone", help="Audit specific zone only")
    p.add_argument("--diff-global", action="store_true", help="Compare with global locations")
    p.add_argument("--json", action="store_true", help="JSON output")
    args = p.parse_args()

    manifest = load_manifest()
    zones = manifest["zones"]

    if args.zone:
        if args.zone not in zones:
            print(f"ERROR: unknown zone '{args.zone}'. Valid: {list(zones.keys())}")
            sys.exit(1)
        audits = [audit_zone(args.zone, zones[args.zone], args.diff_global)]
    else:
        audits = [audit_zone(name, cfg, args.diff_global) for name, cfg in zones.items()]

    if args.json:
        print(json.dumps(audits, indent=2, ensure_ascii=False))
    else:
        print_human(audits)

    # Save audit timestamp
    (PROJECT_ROOT / "scripts" / ".last-audit.txt").write_text(
        datetime.now(timezone.utc).isoformat(), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
