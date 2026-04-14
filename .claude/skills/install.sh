#!/usr/bin/env bash
# install.sh — Sync 2-zone skill library sang IDE khác (macOS/Linux/Git Bash)
# Usage:
#   ./install.sh --target antigravity
#   ./install.sh --target cursor --global
#   ./install.sh --target all --copy
#
# Supported targets: claude-code, antigravity, cursor, kilo, codex, opencode,
#                    windsurf, cline, github-copilot, all

set -euo pipefail

SKILLS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SKILLS_ROOT")")"

TARGET=""
GLOBAL=0
COPY=0
FORCE=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --target)  TARGET="$2"; shift 2 ;;
        --global)  GLOBAL=1; shift ;;
        --copy)    COPY=1; shift ;;
        --force)   FORCE=1; shift ;;
        -h|--help)
            sed -n '2,10p' "$0"
            exit 0
            ;;
        *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
done

[[ -z "$TARGET" ]] && { echo "ERROR: --target required" >&2; exit 1; }

# Map target -> skill folder path
declare -A TARGET_PATHS=(
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

install_zone() {
    local target_name="$1"
    local rel_path="$2"
    local base_dir

    if [[ $GLOBAL -eq 1 ]]; then
        base_dir="$HOME"
    else
        base_dir="$PROJECT_ROOT"
    fi

    local dest_root="$base_dir/$rel_path"
    mkdir -p "$dest_root"

    for zone in vci-cuongbx claudekit; do
        local src_path="$SKILLS_ROOT/$zone"
        local dest_path="$dest_root/$zone"

        if [[ -e "$dest_path" || -L "$dest_path" ]]; then
            if [[ $FORCE -eq 1 ]]; then
                rm -rf "$dest_path"
            else
                echo "SKIP: $dest_path exists (use --force)"
                continue
            fi
        fi

        if [[ $COPY -eq 1 ]]; then
            cp -r "$src_path" "$dest_path"
            echo "COPY: $zone -> $dest_path"
        else
            ln -s "$src_path" "$dest_path"
            echo "LINK: $zone -> $dest_path"
        fi
    done
}

if [[ "$TARGET" == "all" ]]; then
    targets=("${!TARGET_PATHS[@]}")
else
    if [[ -z "${TARGET_PATHS[$TARGET]:-}" ]]; then
        echo "ERROR: unknown target '$TARGET'" >&2
        echo "Valid: ${!TARGET_PATHS[*]} all" >&2
        exit 1
    fi
    targets=("$TARGET")
fi

for t in "${targets[@]}"; do
    echo ""
    echo "=== Installing to: $t ==="
    install_zone "$t" "${TARGET_PATHS[$t]}"
done

echo ""
echo "Done. Scope: $([[ $GLOBAL -eq 1 ]] && echo 'Global (user home)' || echo 'Project (cwd)')"
echo "Method: $([[ $COPY -eq 1 ]] && echo 'Copy' || echo 'Symlink')"
