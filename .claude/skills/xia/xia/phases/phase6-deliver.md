# Phase 6: 🚀 Deliver — Execute port

**Goal:** Execute plan với checkpoint commits, attribution, manifest updates. Verify trước khi hand-off user review.

## Compose skills

| Skill | Vai trò |
|---|---|
| **`ck:cook`** | Execute phases từ Plan (default `--parallel` nếu phases independent) |
| `test-automator` | Run ported tests + generate missing |
| `code-review` | Final adversarial review trước khi commit |
| `ck:security` | Pre-commit security scan trên changes |

## Steps

### 6.1. Pre-flight checks

```bash
# Local must be clean (or stashed)
git status --porcelain | wc -l  # must be 0
if [[ uncommitted_count > 0 ]]; then
  REFUSE "local has uncommitted changes — stash hoặc commit trước"
fi

# Create feature branch
BRANCH="xia/port-$(echo $FEATURE | tr ' ' '-')-$(date +%y%m%d-%H%M)"
git checkout -b "$BRANCH"
```

### 6.2. Execute plan qua ck:cook

```bash
ck cook \
  --plan plans/260414-1430-xia-port-rate-limiter/ \
  --parallel \  # nếu phases independent
  --no-auto-commit  # xia sẽ commit manually ở 6.3
```

`ck:cook` spawns subagents cho:
- research (nếu plan có gap)
- scout (locate target files)
- implementation (per phase)
- testing
- review
- finalization

### 6.3. Checkpoint commits per phase

Sau mỗi phase ck:cook complete:

```bash
# Add attribution header vào files mới
python .claude/skills/xia/xia/scripts/generate-attribution-header.py \
  --files "$PHASE_FILES" \
  --source "$SOURCE_REPO@$SOURCE_SHA" \
  --license "$SOURCE_LICENSE" \
  --mode "$MODE"

# Commit checkpoint
git add {phase_files}
git commit -m "xia(port): phase {N} — {phase_name}

Source: {source_repo}@{sha}
License: {source_license}
Mode: {mode}

[checkpoint for /xia rollback]"
```

Lưu commit SHA vào `.xia/cache/checkpoints.json` để rollback.

### 6.4. Update `.xia-manifest.json`

```bash
python .claude/skills/xia/xia/scripts/fingerprint-manifest.py \
  --action add \
  --manifest .xia-manifest.json \
  --entry "$(build_entry_from_context)"
```

Entry structure:

```json
{
  "id": "port_003",
  "feature_name": "rate-limiter",
  "source_repo": "https://github.com/tj/node-ratelimiter",
  "source_commit": "a1b2c3d",
  "source_license": "MIT",
  "port_date": "2026-04-14",
  "port_mode": "improve",
  "files_ported": ["src/middleware/rateLimit.ts", "src/lib/tokenBucket.ts"],
  "files_modified": ["src/app.ts", "package.json"],
  "dependencies_added": ["ioredis@5.3"],
  "challenges_passed": ["env", "deps", "async", "state", "license", "observability"],
  "rollback_commit": "d4e5f6g",
  "attribution_header_added": true,
  "ported_by": "/xia v1.0",
  "ported_user": "cuongbx@email"  // git user.email
}
```

### 6.5. Final verification

```bash
# Security scan trên changes
ck security --scan-diff HEAD~N..HEAD --fail-on high

# Code review adversarial trên ported code
ck code-review --adversarial --target "{ported_files}"

# Run tests
npm test  # hoặc pytest, go test, cargo test per stack
```

Nếu bất kỳ check fail → **DO NOT merge** → present report + rollback option.

### 6.6. Optional: trigger vci-skill-cuongbx

Nếu user muốn:
- **Mode 5 Dev Guide** — generate `dev_guide.md` cho feature mới
- **Mode 6 Test Gen** — supplement tests (BDD, security scenarios)

Ask: *"Muốn sinh Dev Guide + Test Cases cho feature mới không?"*

### 6.7. Hand-off user

Output summary:

```
✅ Port complete: rate-limiter
   Mode: --improve
   Branch: xia/port-rate-limiter-260414-1430
   Files ported: 2 created, 2 modified
   Tests: 8/8 passing
   Security: 0 red, 1 yellow (rate limit not applied to /health — by design)
   Manifest: .xia-manifest.json updated

Next steps:
  git diff main...HEAD     # review full changes
  gh pr create             # open PR
  /xia rollback port_003   # nếu cần revert
```

## Error recovery mid-deliver

| Issue | Action |
|---|---|
| Phase N fails | Stop at last good checkpoint, present error + rollback suggestion |
| Test failure | Retry 1x, nếu vẫn fail → delegate `ck:debug` |
| Security scan fail | REFUSE merge, present issues, user triage |
| Merge conflict với main | Pause, ask user resolve, resume |

## Rollback protocol

```bash
# Full rollback (abandon port)
git reset --hard main
git branch -D xia/port-{feature}-{timestamp}

# Partial rollback (back to phase N)
CHECKPOINT_SHA=$(jq -r ".phases[\"$N\"]" .xia/cache/checkpoints.json)
git reset --hard "$CHECKPOINT_SHA"

# Remove manifest entry
python scripts/fingerprint-manifest.py --action remove --id port_003
```
