#!/usr/bin/env bash
# install-companion.sh — Clone companion skill repos vào .claude/skills/
#
# Usage:
#   ./scripts/install-companion.sh claudekit
#   ./scripts/install-companion.sh xia
#   ./scripts/install-companion.sh others
#   ./scripts/install-companion.sh all
#   ./scripts/install-companion.sh --global claudekit   # clone vào ~/.claude/skills/
#
# Edit URLs below to match your actual companion repo URLs.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# EDIT these URLs when companion repos are pushed to GitHub
declare -A REPO_URLS=(
  [claudekit]="https://github.com/cuongbx/skills-claudekit.git"
  [xia]="https://github.com/cuongbx/skills-xia.git"
  [others]="https://github.com/cuongbx/skills-others.git"
)

# Local path mapping (target folder name inside .claude/skills/)
declare -A LOCAL_PATHS=(
  [claudekit]="claudekit"
  [xia]="xia"
  [others]="others"
)

GLOBAL=0
TARGETS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global) GLOBAL=1; shift ;;
    all) TARGETS=(claudekit xia others); shift ;;
    claudekit|xia|others) TARGETS+=("$1"); shift ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) echo "Unknown: $1" >&2; exit 1 ;;
  esac
done

[[ ${#TARGETS[@]} -eq 0 ]] && { echo "ERROR: Specify a target (claudekit / xia / others / all)" >&2; exit 1; }

BASE_DIR="$PROJECT_ROOT/.claude/skills"
[[ $GLOBAL -eq 1 ]] && BASE_DIR="$HOME/.claude/skills"

mkdir -p "$BASE_DIR"

for target in "${TARGETS[@]}"; do
  url="${REPO_URLS[$target]}"
  dest="$BASE_DIR/${LOCAL_PATHS[$target]}"

  echo ""
  echo "=== Install: $target ==="
  echo "  Repo: $url"
  echo "  Dest: $dest"

  if [[ -d "$dest" ]]; then
    echo "  EXISTS — pulling latest..."
    (cd "$dest" && git pull --ff-only)
  else
    git clone --depth 1 "$url" "$dest"
  fi
  echo "  OK"
done

echo ""
echo "Done. Scope: $([[ $GLOBAL -eq 1 ]] && echo 'Global (~/.claude/skills)' || echo 'Project (.claude/skills)')"
