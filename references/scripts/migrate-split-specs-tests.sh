#!/usr/bin/env bash
# migrate-split-specs-tests.sh
#
# Tách structure cũ `docs/features/{zone}/{module}/` → structure mới:
#   docs/specs/{zone}/{module}/   <- spec files (IMS_*.md, README.md, dev_guide.md)
#   docs/tests/{zone}/{module}/   <- test files (test_cases*, test_mapping*, gap_detection_report_*, *_screenshoot/)
#
# Usage:
#   ./migrate-split-specs-tests.sh <project_root>
#   ./migrate-split-specs-tests.sh --dry-run <project_root>
#
# Yêu cầu: chạy trong git repo (để `git mv` preserve history). Không có git sẽ dùng `mv` thường.

set -e

DRY_RUN=0
if [ "$1" = "--dry-run" ]; then
  DRY_RUN=1
  shift
fi

ROOT="${1:-.}"
SRC="$ROOT/docs/features"
SPEC_DST="$ROOT/docs/specs"
TEST_DST="$ROOT/docs/tests"

if [ ! -d "$SRC" ]; then
  echo "❌ Không tìm thấy $SRC"
  exit 1
fi

# Detect git
USE_GIT=0
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  USE_GIT=1
fi

mv_cmd() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ $DRY_RUN -eq 1 ]; then
    echo "  [dry] $src → $dst"
    return
  fi
  if [ $USE_GIT -eq 1 ]; then
    git -C "$ROOT" mv "${src#$ROOT/}" "${dst#$ROOT/}" 2>/dev/null || mv "$src" "$dst"
  else
    mv "$src" "$dst"
  fi
}

is_test_file() {
  local name="$(basename "$1")"
  case "$name" in
    test_cases*|test_mapping*|test_execution*|gap_detection_report_*|Test_Report*|*_screenshoot|*_screenshot)
      return 0 ;;
  esac
  return 1
}

# Walk top-level zones (master_data, transactions, transfer, reports)
find "$SRC" -maxdepth 1 -mindepth 1 -type d | while read zone_dir; do
  zone="$(basename "$zone_dir")"
  # Skip hidden/special zones
  case "$zone" in .*|bug_retest_plan|*_screenshoot|*_screenshot) continue ;; esac

  echo "📂 Zone: $zone"
  find "$zone_dir" -maxdepth 1 -mindepth 1 -type d | while read mod_dir; do
    mod="$(basename "$mod_dir")"
    case "$mod" in .*|*_screenshoot|*_screenshot) continue ;; esac

    echo "  📁 Module: $zone/$mod"

    # Move every file/folder
    find "$mod_dir" -maxdepth 1 -mindepth 1 | while read item; do
      if is_test_file "$item"; then
        mv_cmd "$item" "$TEST_DST/$zone/$mod/$(basename "$item")"
      else
        mv_cmd "$item" "$SPEC_DST/$zone/$mod/$(basename "$item")"
      fi
    done
  done

  # Handle direct files in zone (e.g. reports/IMS_RPT_*.md)
  find "$zone_dir" -maxdepth 1 -mindepth 1 -type f | while read f; do
    if is_test_file "$f"; then
      mv_cmd "$f" "$TEST_DST/$zone/$(basename "$f")"
    else
      mv_cmd "$f" "$SPEC_DST/$zone/$(basename "$f")"
    fi
  done
done

# Move zone-level README / orphan files at docs/features root into specs/
find "$SRC" -maxdepth 1 -mindepth 1 -type f | while read f; do
  if is_test_file "$f"; then
    mv_cmd "$f" "$TEST_DST/$(basename "$f")"
  else
    mv_cmd "$f" "$SPEC_DST/$(basename "$f")"
  fi
done

echo ""
echo "✅ Done. Kiểm tra thủ công:"
echo "   - $SPEC_DST (specs)"
echo "   - $TEST_DST (tests)"
echo "   - Old $SRC có thể xóa nếu empty: rmdir \$(find $SRC -type d -empty)"
