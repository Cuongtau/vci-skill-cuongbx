#!/usr/bin/env python3
"""
check-mode-prerequisites.py — Verify precondition trước khi chạy Mode của vci-skill-cuongbx.

Usage:
    python check-mode-prerequisites.py --mode 10 --spec docs/specs/auth/IMS_AUTH_01_login/spec.md
    python check-mode-prerequisites.py --mode 5A --spec docs/specs/.../spec.md
    python check-mode-prerequisites.py --mode 1 --feature-id IMS_NK_01 --module inventory

Exit codes:
    0 — OK, có thể proceed
    1 — WARN (prerequisite thiếu nhưng có thể override)
    2 — FAIL (hard refuse, yêu cầu fix trước)
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

# Force UTF-8 output on Windows (avoid cp1252 crash on Vietnamese characters)
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def read_spec(path: Path) -> str | None:
    """Read spec file. Return content or None if missing."""
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def extract_frontmatter(content: str) -> dict:
    """Extract simple YAML frontmatter as flat dict (no nested support)."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm


def check_mode_1(args) -> tuple[int, str]:
    """Mode 1 Generate — check Feature ID not already exists."""
    if not args.feature_id or not args.module:
        return 1, "WARN: cần --feature-id + --module để check duplicate"
    docs_dir = Path("docs/specs") / args.module
    if not docs_dir.exists():
        return 0, f"OK: module '{args.module}' mới, feature ID an toàn"
    for subdir in docs_dir.iterdir():
        if subdir.is_dir() and subdir.name.startswith(args.feature_id):
            return 2, (
                f"FAIL: Feature ID '{args.feature_id}' đã tồn tại ở {subdir}. "
                f"Dùng Mode 3 Update hoặc đổi Feature ID."
            )
    return 0, "OK: Feature ID mới, sẵn sàng Generate"


def check_mode_3(args) -> tuple[int, str]:
    """Mode 3 Update — check if spec is APPROVED (triggers CR flow)."""
    content = read_spec(args.spec)
    if content is None:
        return 2, f"FAIL: spec không tồn tại tại {args.spec}"
    fm = extract_frontmatter(content)
    status = fm.get("status", "DRAFT")
    if status == "APPROVED":
        return 1, (
            "WARN: spec status=APPROVED → Mode 3 sẽ tự động tạo Change Request. "
            "Sửa trực tiếp không được phép."
        )
    if status == "FROZEN":
        return 2, "FAIL: spec status=FROZEN (release week) — chỉ hotfix CR"
    return 0, f"OK: status={status}, có thể update"


def check_mode_4(args) -> tuple[int, str]:
    """Mode 4 Audit — check spec exists + optionally source code."""
    content = read_spec(args.spec)
    if content is None:
        return 2, f"FAIL: spec không tồn tại tại {args.spec}"
    # Full audit cần source code
    if args.code_path and not Path(args.code_path).exists():
        return 2, f"FAIL: source code path không tồn tại: {args.code_path}"
    if not args.code_path:
        return 1, "WARN: thiếu --code-path → chỉ audit Gap Detection, không audit spec↔code"
    return 0, "OK: spec + code present, sẵn sàng full audit"


def check_mode_5(args) -> tuple[int, str]:
    """Mode 5A/5B Dev Guide — check spec APPROVED."""
    content = read_spec(args.spec)
    if content is None:
        return 2, f"FAIL: spec không tồn tại tại {args.spec}"
    fm = extract_frontmatter(content)
    status = fm.get("status", "DRAFT")
    if status in ("DRAFT", "IN_REVIEW"):
        return 1, (
            f"WARN: spec status={status} — Dev guide có thể stale khi spec đổi. "
            "Khuyến nghị wait cho APPROVED."
        )
    return 0, f"OK: status={status}"


def check_mode_6(args) -> tuple[int, str]:
    """Mode 6 Test Gen — check spec has AC section."""
    content = read_spec(args.spec)
    if content is None:
        return 2, f"FAIL: spec không tồn tại tại {args.spec}"
    # Check có AC section (flexible: AC, Acceptance Criteria, Tiêu chí chấp nhận)
    ac_patterns = [r"##\s+AC\b", r"Acceptance Criteria", r"Tiêu chí chấp nhận"]
    if not any(re.search(p, content, re.IGNORECASE) for p in ac_patterns):
        return 2, "FAIL: spec thiếu AC/Acceptance Criteria section → Mode 6 không trace được"
    return 0, "OK: spec có AC, sẵn sàng Test Gen"


def check_mode_10(args) -> tuple[int, str]:
    """Mode 10 Mockup — check spec has Level 4 + UI Spec."""
    content = read_spec(args.spec)
    if content is None:
        return 2, f"FAIL: spec không tồn tại tại {args.spec}"
    # Check Level 4 section
    if not re.search(r"##?\s*Level\s*4", content, re.IGNORECASE):
        return 2, (
            "FAIL: spec thiếu Level 4 section. Mode 10 cần UI Spec + Button Matrix. "
            "Chạy Mode 1 (Generate) hoặc Mode 3 (Update) để bổ sung trước."
        )
    # Check UI Spec + Button Matrix
    missing = []
    if not re.search(r"UI\s*Spec|Giao\s*diện", content, re.IGNORECASE):
        missing.append("UI Spec")
    if not re.search(r"Button\s*Matrix|Ma\s*trận\s*nút", content, re.IGNORECASE):
        missing.append("Button Matrix")
    if missing:
        return 1, f"WARN: thiếu sections: {', '.join(missing)} — mockup có thể không đầy đủ"
    return 0, "OK: Level 4 + UI Spec + Button Matrix, sẵn sàng Mockup"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", required=True, choices=["1", "2", "3", "4", "5A", "5B", "6", "7", "8", "9", "10"])
    p.add_argument("--spec", type=Path, help="Path tới spec.md")
    p.add_argument("--feature-id", help="Feature ID (cho Mode 1 duplicate check)")
    p.add_argument("--module", help="Module folder (cho Mode 1)")
    p.add_argument("--code-path", help="Source code path (cho Mode 4 full audit)")
    args = p.parse_args()

    dispatch = {
        "1": check_mode_1,
        "3": check_mode_3,
        "4": check_mode_4,
        "5A": check_mode_5,
        "5B": check_mode_5,
        "6": check_mode_6,
        "10": check_mode_10,
    }

    if args.mode not in dispatch:
        print(f"INFO: Mode {args.mode} không có prerequisite check")
        sys.exit(0)

    code, msg = dispatch[args.mode](args)
    prefix = {0: "[OK]", 1: "[WARN]", 2: "[FAIL]"}[code]
    print(f"{prefix} {msg}")
    sys.exit(code)


if __name__ == "__main__":
    main()
