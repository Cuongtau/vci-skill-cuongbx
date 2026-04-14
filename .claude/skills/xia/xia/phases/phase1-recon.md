# Phase 1: 🔍 Recon — Hiểu source repo

**Goal:** Nắm purpose, scope, license, deps của source trước khi đụng 1 dòng code.

## Compose skills

| Skill | Mục đích |
|---|---|
| `ck:repomix` | Pack remote repo vào AI-friendly format (sandbox mode) |
| `ck:docs-seeker` | Fetch llms.txt / README nếu có |
| `ck:research` | Hiểu purpose + trade-offs (nếu user mô tả mơ hồ) |

## Steps

### 1.1. Fetch source

```bash
# Primary: repomix
ck repomix --remote https://github.com/{owner}/{repo} \
  --output .xia/cache/{repo}-{sha}.xml \
  --include "src/**,package.json,README.md,LICENSE" \
  --compress

# Fallback nếu repomix fail
gh repo view {owner}/{repo} --json description,license,languages
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d
```

**Security sandbox:**
- Output vào `.xia/cache/` (gitignored)
- KHÔNG execute bất cứ file nào từ fetched content
- KHÔNG chạy `npm ci` / `pip install -r` từ source manifest
- Log mọi fetch operation vào `.xia/audit.log`

### 1.2. Locate feature

Từ user input xác định:
- Exact path (`src/auth/login.ts`) — ưu tiên
- Folder (`src/auth/`) — ok
- Feature name — dùng `ck:scout --target "{name}" --within .xia/cache/`

Nếu không tìm được → ask-back: *"Feature chính xác ở path nào? Hoặc share description chi tiết?"*

### 1.3. Read meta

Parse các file sau:

| File | Extract |
|---|---|
| `README.md` | Purpose, usage, dependencies list |
| `LICENSE` / `LICENSE.md` | License identifier (MIT, Apache-2.0, GPL-3.0, ...) |
| `package.json` / `requirements.txt` / `Cargo.toml` | Runtime deps |
| `tsconfig.json` / `setup.py` | Stack version requirements |
| `.github/workflows/` | CI patterns (optional) |

### 1.4. License compat check

```bash
python .claude/skills/xia/xia/scripts/check-license-compat.py \
  --source-license MIT \
  --target-license {local_license_from_project_LICENSE}
```

Output: `MATCH` / `WARN` / `BLOCK` + explanation.

**Policy:** WARN (không hard-block) — user sẽ decide trong Phase 4 Challenge.

### 1.5. Cost estimation

Output formula:
```
estimated_hours = (loc / 500) × layer_count × stack_diff_factor
```

Factors:
- `stack_diff_factor`: 1.0 (same stack), 1.5 (same family TS↔JS), 3.0 (cross-language)
- `layer_count`: từ Map step nhưng ước lượng sơ bộ ở đây

### 1.6. Output Recon summary

```yaml
repo: owner/name
sha: abc1234
license: MIT
feature: src/auth/
loc: 2340
layers_estimated: 5
deps:
  - bcrypt@5.1
  - jsonwebtoken@9.0
license_verdict: MATCH  # với local proprietary — MIT OK
estimated_hours: 2.5
security_flags: []  # no eval/curl/obfuscation detected
```

Present tóm tắt cho user → proceed to Phase 2 (Map) hoặc abort.

## Fallback paths

| Issue | Fallback |
|---|---|
| Repo 404 / private | `gh auth login` hoặc fork trước |
| Repo too large >10k LOC | `--include` pattern để narrow |
| Repomix timeout | Direct `gh api` fetch từng file |
| README thiếu | Infer từ code + dep analysis |

## Unresolved

- Nếu user chỉ có blog post / StackOverflow, không có repo → dùng `ck:research` tìm repo phù hợp, rồi quay lại step 1.1
- Multi-repo feature (code span 2+ repos) → port từng repo riêng, gộp ở Deliver
