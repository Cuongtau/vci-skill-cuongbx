# `.xia-manifest.json` — Schema v1.0

File ở project root. Track mọi port đã làm. Visible, git-committed (audit trail).

## Full schema

```json
{
  "$schema": "https://raw.githubusercontent.com/.../xia-manifest-v1.json",
  "version": "1.0",
  "project": {
    "name": "string",
    "license": "MIT | Apache-2.0 | ..."
  },
  "ports": [
    {
      "id": "port_001",
      "feature_name": "Rate Limiter",
      "source": {
        "repo": "https://github.com/tj/node-ratelimiter",
        "commit": "a1b2c3d4e5f6",
        "license": "MIT",
        "license_verdict": "MATCH | WARN | BLOCK_OVERRIDDEN",
        "original_path": "lib/limiter.js"
      },
      "port": {
        "date": "2026-04-14",
        "user": "cuongbx@example.com",
        "mode": "compare | copy | improve | port",
        "xia_version": "1.0.0"
      },
      "impact": {
        "files_created": ["src/middleware/rateLimit.ts"],
        "files_modified": ["src/app.ts", "package.json"],
        "files_replaced": [],
        "dependencies_added": ["ioredis@5.3"],
        "dependencies_removed": [],
        "loc_added": 234,
        "loc_removed": 12
      },
      "challenges": {
        "total": 7,
        "passed": 5,
        "accepted_risk": 2,
        "aborted": 0,
        "categories_covered": ["env", "deps", "async", "state", "license", "observability"],
        "log_path": ".xia/cache/challenge-log-port_001.md"
      },
      "git": {
        "branch": "xia/port-rate-limiter-260414-1430",
        "checkpoint_commits": [
          { "phase": "01-deps", "sha": "aaa111" },
          { "phase": "02-core", "sha": "bbb222" },
          { "phase": "03-tests", "sha": "ccc333" }
        ],
        "final_commit": "ddd444",
        "merged_to_main": false,
        "merge_sha": null
      },
      "verification": {
        "security_scan": "pass | pass_with_warn | fail",
        "security_flags": [
          {"level": "yellow", "finding": "No rate limit on /health"}
        ],
        "tests_run": true,
        "tests_passed": 8,
        "tests_failed": 0,
        "code_review_grade": "A"
      },
      "attribution": {
        "header_added": true,
        "header_files": ["src/middleware/rateLimit.ts", "src/lib/tokenBucket.ts"],
        "notice_updated": true
      },
      "status": "active | rolled_back | deprecated",
      "rollback_reason": null
    }
  ],
  "stats": {
    "total_ports": 3,
    "active_ports": 2,
    "rolled_back": 1,
    "last_updated": "2026-04-14T14:35:00Z"
  }
}
```

## Usage scenarios

### Add entry (after successful Deliver)
```bash
python scripts/fingerprint-manifest.py --action add --entry entry.json
```

### Check idempotency (before new port)
```bash
python scripts/fingerprint-manifest.py --action check \
  --source-repo "https://github.com/..." --feature "rate-limiter"
# → match | no_match | partial_match
```

If `match` → ask user: re-port / update / skip.

### Mark rollback
```bash
python scripts/fingerprint-manifest.py --action rollback --id port_001 \
  --reason "tests failing after dep upgrade"
```

### Audit report
```bash
python scripts/fingerprint-manifest.py --action audit
# Output:
# - Which external code is in project?
# - Licenses present
# - Age of each port (detect drift)
# - Active vs rolled-back
```

## Fingerprinting

Để idempotency, fingerprint = hash of:
- `source.repo` + `source.commit` + `source.original_path`
- `port.mode`
- `impact.files_created` (sorted)

Cùng fingerprint = same port attempt → skip hoặc ask.

## Integration với tools

### Git hooks

Pre-commit: verify `.xia-manifest.json` syntax valid + attribution headers present.

```bash
# .git/hooks/pre-commit
python .claude/skills/xia/xia/scripts/fingerprint-manifest.py --action verify
```

### CI check

GitHub Actions workflow sample:
```yaml
- name: Verify xia manifest
  run: python .claude/skills/xia/xia/scripts/fingerprint-manifest.py --action verify
```

### License audit

Dùng cho compliance reports:
```bash
python scripts/fingerprint-manifest.py --action license-report \
  --output docs/third-party-licenses.md
```

## Drift detection (future v1.1+)

Periodic check: upstream repo updated → current port stale?
```bash
xia sync  # detect upstream changes since port commit
```

## Privacy

- `port.user` = git user.email (có thể override với `--anonymous`)
- Manifest visible trong repo — **KHÔNG store tokens, secrets, credentials**
- External audit tools có thể parse JSON

## Versioning

- `version: "1.0"` — current
- Future migration: `scripts/migrate-manifest.py --from 1.0 --to 1.1`
- Breaking changes increment major
