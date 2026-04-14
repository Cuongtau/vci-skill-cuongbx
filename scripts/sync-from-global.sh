#!/usr/bin/env bash
# sync-from-global.sh — Pull skills từ global locations (~/.claude/skills, ~/.gemini/antigravity/skills) → project zones
# Usage:
#   ./scripts/sync-from-global.sh                    # sync all zones
#   ./scripts/sync-from-global.sh --zone claudekit   # sync 1 zone
#   ./scripts/sync-from-global.sh --dry-run          # preview only

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$PROJECT_ROOT/scripts/manifest.json"
DRY_RUN=0
ZONE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --zone) ZONE="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

# Expand ~ in paths
expand_path() {
  echo "${1/#\~/$HOME}"
}

sync_zone() {
  local name="$1"
  local local_path="$2"
  local global_path="$3"
  local exclude="$4"   # comma-separated skill names to skip

  echo ""
  echo "=== Zone: $name ==="
  echo "  Source: $global_path"
  echo "  Dest:   $local_path"

  if [[ ! -d "$global_path" ]]; then
    echo "  SKIP: global path không tồn tại"
    return
  fi

  mkdir -p "$local_path"
  local count=0 skipped=0

  for skill_dir in "$global_path"/*/; do
    [[ -d "$skill_dir" ]] || continue
    local skill_name=$(basename "$skill_dir")

    # Check exclude list
    if [[ ",$exclude," == *",$skill_name,"* ]]; then
      skipped=$((skipped+1))
      continue
    fi

    if [[ $DRY_RUN -eq 1 ]]; then
      echo "  [DRY] would copy $skill_name"
    else
      cp -r "$skill_dir" "$local_path/" 2>/dev/null || true
    fi
    count=$((count+1))
  done

  echo "  → Synced $count skills (excluded $skipped)"
}

echo "=========================================="
echo "Sync FROM GLOBAL → PROJECT"
[[ $DRY_RUN -eq 1 ]] && echo "[DRY-RUN MODE — no changes]"
echo "=========================================="

CK_GLOBAL=$(expand_path "~/.claude/skills")
AG_GLOBAL=$(expand_path "~/.gemini/antigravity/skills")

# claudekit zone (pull-only)
if [[ -z "$ZONE" || "$ZONE" == "claudekit" ]]; then
  # Sync ALL skills from ~/.claude/skills/ EXCEPT vci-cuongbx + xia (those are in their own zones)
  sync_zone "claudekit" \
    "$PROJECT_ROOT/.claude/skills/claudekit" \
    "$CK_GLOBAL" \
    "vci-skill-cuongbx,xia,vci-cuongbx"
fi

# others zone (pull-only)
if [[ -z "$ZONE" || "$ZONE" == "others" ]]; then
  sync_zone "others" \
    "$PROJECT_ROOT/.claude/skills/others" \
    "$AG_GLOBAL" \
    "antigravity-awesome-skills,skill-creator-ultra,vci-skill-cuongbx"
fi

# vci zone (bidirectional - check if global has updates)
if [[ -z "$ZONE" || "$ZONE" == "vci" ]]; then
  echo ""
  echo "=== Zone: vci (bidirectional check) ==="
  echo "  Local: $PROJECT_ROOT/.claude/skills/vci"
  echo "  Global: $CK_GLOBAL/<skill> (per-skill)"
  echo "  Note: bidirectional zones không auto-overwrite."
  echo "  Use 'sync-to-global.sh' để push local changes."
fi

# xia zone (bidirectional)
if [[ -z "$ZONE" || "$ZONE" == "xia" ]]; then
  echo ""
  echo "=== Zone: xia (bidirectional check) ==="
  echo "  Local: $PROJECT_ROOT/.claude/skills/xia"
  echo "  Global: $CK_GLOBAL/xia (chưa exist — push first)"
fi

echo ""
echo "=========================================="
echo "Done. Update manifest timestamp..."
[[ $DRY_RUN -eq 0 ]] && date -u +"%Y-%m-%dT%H:%M:%SZ" > "$PROJECT_ROOT/scripts/.last-sync.txt"
echo "Sync state: $PROJECT_ROOT/scripts/.last-sync.txt"
