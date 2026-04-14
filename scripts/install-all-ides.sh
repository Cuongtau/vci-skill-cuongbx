#!/usr/bin/env bash
# install-all-ides.sh — Cài skills sang nhiều IDE locations
# Usage:
#   ./scripts/install-all-ides.sh                       # install to all IDEs
#   ./scripts/install-all-ides.sh --target claude-code  # specific IDE
#   ./scripts/install-all-ides.sh --global              # to ~/<ide-path>
#   ./scripts/install-all-ides.sh --copy                # copy thay vì symlink

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET=""
GLOBAL=0
COPY=0
FORCE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="$2"; shift 2 ;;
    --global) GLOBAL=1; shift ;;
    --copy) COPY=1; shift ;;
    --force) FORCE=1; shift ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

declare -A IDE_PATHS=(
  [claude-code]=".claude/skills"
  [antigravity]=".gemini/skills"
  [cursor]=".cursor/skills"
  [kilo]=".kilo/skills"
  [codex]=".codex/skills"
  [opencode]=".opencode/skills"
  [windsurf]=".windsurf/skills"
  [cline]=".cline/skills"
  [github-copilot]=".github/copilot/skills"
)

install_to_ide() {
  local ide="$1"
  local rel_path="$2"
  local base
  if [[ $GLOBAL -eq 1 ]]; then
    base="$HOME"
  else
    base="$PWD"
  fi
  local dest_root="$base/$rel_path"

  echo ""
  echo "=== Install to: $ide ($dest_root) ==="
  mkdir -p "$dest_root"

  for zone in vci claudekit xia others; do
    local src="$PROJECT_ROOT/.claude/skills/$zone"
    [[ -d "$src" ]] || { echo "  SKIP zone $zone (not present)"; continue; }

    local dest="$dest_root/$zone"
    if [[ -e "$dest" || -L "$dest" ]]; then
      if [[ $FORCE -eq 1 ]]; then
        rm -rf "$dest"
      else
        echo "  SKIP: $dest exists (use --force)"
        continue
      fi
    fi

    if [[ $COPY -eq 1 ]]; then
      cp -r "$src" "$dest"
      echo "  COPY: $zone → $dest"
    else
      ln -s "$src" "$dest"
      echo "  LINK: $zone → $dest"
    fi
  done
}

echo "=========================================="
echo "Install skills to IDE(s)"
echo "  Scope: $([[ $GLOBAL -eq 1 ]] && echo "Global (~)" || echo "Project (cwd)")"
echo "  Method: $([[ $COPY -eq 1 ]] && echo "Copy" || echo "Symlink")"
echo "=========================================="

if [[ -z "$TARGET" || "$TARGET" == "all" ]]; then
  for ide in "${!IDE_PATHS[@]}"; do
    install_to_ide "$ide" "${IDE_PATHS[$ide]}"
  done
else
  if [[ -z "${IDE_PATHS[$TARGET]:-}" ]]; then
    echo "ERROR: unknown IDE '$TARGET'" >&2
    echo "Valid: ${!IDE_PATHS[*]} all" >&2
    exit 1
  fi
  install_to_ide "$TARGET" "${IDE_PATHS[$TARGET]}"
fi

echo ""
echo "=========================================="
echo "Done."
