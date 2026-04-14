#!/usr/bin/env bash
# restore-claudekit.sh — Restore full claudekit zone (179 skills, ~325MB) from global
# Usage: ./restore-claudekit.sh
#
# Copy toàn bộ ~/.claude/skills/* vào .claude/skills/claudekit/
# Dùng khi: (a) clone repo mới, (b) reset claudekit zone, (c) update từ global
#
# Prerequisite: ~/.claude/skills/ phải có sẵn (cài qua `ck skills` hoặc `npm install -g claudekit-cli`)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HOME/.claude/skills"
DST="$SCRIPT_DIR/claudekit"

if [[ ! -d "$SRC" ]]; then
    echo "ERROR: $SRC not found." >&2
    echo "Install ClaudeKit first:" >&2
    echo "  npm install -g claudekit-cli" >&2
    echo "  ck skills --list   # populate ~/.claude/skills/" >&2
    exit 1
fi

mkdir -p "$DST"
echo "Source: $SRC"
echo "Dest:   $DST"
echo ""
echo "Copying ~179 skills (~325MB)..."
start=$(date +%s)

count=0
for skill in "$SRC"/*/; do
    name=$(basename "$skill")
    if [[ ! -d "$DST/$name" ]]; then
        cp -r "$skill" "$DST/"
        count=$((count+1))
    fi
done

end=$(date +%s)
echo ""
echo "Done. Copied $count new skills in $((end-start))s"
echo "Total in claudekit/: $(ls "$DST" | wc -l) items"
echo "Size: $(du -sh "$DST" | cut -f1)"
