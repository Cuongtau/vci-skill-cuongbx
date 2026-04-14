#!/usr/bin/env bash
# sync-to-global.sh — Push local zone customizations lên global locations
# Usage:
#   ./scripts/sync-to-global.sh                    # push all bidirectional zones
#   ./scripts/sync-to-global.sh --zone vci         # push 1 zone
#   ./scripts/sync-to-global.sh --dry-run

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
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

push_zone() {
  local name="$1"
  local local_path="$2"
  local global_path="$3"

  echo ""
  echo "=== Push Zone: $name ==="
  echo "  Local:  $local_path"
  echo "  Global: $global_path"

  if [[ ! -d "$local_path" ]]; then
    echo "  SKIP: local zone không tồn tại"
    return
  fi

  mkdir -p "$global_path"
  local count=0
  for skill in "$local_path"/*/; do
    [[ -d "$skill" ]] || continue
    local skill_name=$(basename "$skill")
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "  [DRY] would push $skill_name → $global_path/$skill_name"
    else
      cp -r "$skill" "$global_path/$skill_name/" 2>/dev/null || cp -r "$skill" "$global_path/" 2>/dev/null
    fi
    count=$((count+1))
  done
  echo "  → Pushed $count skills"
}

CK_GLOBAL="${HOME}/.claude/skills"

echo "=========================================="
echo "Push LOCAL → GLOBAL (bidirectional zones only)"
[[ $DRY_RUN -eq 1 ]] && echo "[DRY-RUN MODE]"
echo "=========================================="

# vci zone → ~/.claude/skills/<each-skill>/
if [[ -z "$ZONE" || "$ZONE" == "vci" ]]; then
  push_zone "vci" \
    "$PROJECT_ROOT/.claude/skills/vci" \
    "$CK_GLOBAL"
fi

# xia zone → ~/.claude/skills/xia/
if [[ -z "$ZONE" || "$ZONE" == "xia" ]]; then
  push_zone "xia" \
    "$PROJECT_ROOT/.claude/skills/xia" \
    "$CK_GLOBAL"
fi

# claudekit + others = pull-only, không push
if [[ "$ZONE" == "claudekit" || "$ZONE" == "others" ]]; then
  echo ""
  echo "❌ Zone '$ZONE' là pull-only — không push được."
  echo "   Sửa skills source upstream nếu muốn update."
  exit 1
fi

echo ""
echo "=========================================="
echo "Done."
[[ $DRY_RUN -eq 0 ]] && date -u +"%Y-%m-%dT%H:%M:%SZ" > "$PROJECT_ROOT/scripts/.last-push.txt"
