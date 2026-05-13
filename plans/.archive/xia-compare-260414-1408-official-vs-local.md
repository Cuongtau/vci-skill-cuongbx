# Feature Comparison: `xia` skill — Official claudekit vs Local build

**Date:** 2026-04-14 | **Mode:** `--compare` (no code changes) | **Applied skill:** vci xia

## Source

- **Repo path:** `C:/Users/ASUS/Downloads/claudekit-engineer/.opencode/skills/xia`
- **Name:** `ck:xia` v1.0.0
- **Author:** claudekit
- **Category:** dev-tools
- **Size:** 12KB, 2 files (SKILL.md + challenge-framework.md)

## Local

- **Path:** `.claude/skills/xia/xia/`
- **Name:** `xia` v1.0.0
- **Author:** cuongbx
- **Size:** 152KB, 21 files

## Head-to-Head

| Aspect | Source (ck:xia) | Local (xia) | Recommendation |
|---|---|---|---|
| **Philosophy** | "Front door, not orchestration stack" | Self-contained with phases/ | **Adopt source** — avoid duplicating ck:plan/ck:cook logic |
| **SKILL.md length** | 196 lines (lean) | 227 lines | Source more focused |
| **Modes** | 4 (compare/copy/improve/port) | 4 (same) | Match ✅ |
| **Speed flags** | `--fast` + `--auto` | None | **Adopt source** — valuable UX for automation |
| **Intent detection** | Keyword map (compare→--compare, etc.) | Decision tree ASCII | **Adopt source** — simpler |
| **Challenge framework** | Universal (5) + Architecture (5) + Risk scoring matrix | 6 categories × 3 templates | **Hybrid** — source's structure + local's specificity |
| **Scope constraint** | Explicit "Not for: full clone, file copy, package install" | Missing | **Adopt source** |
| **Anti-invoke note** | "Don't call /ck:brainstorm from xia — phase ownership" | Missing | **Adopt source** — prevents workflow confusion |
| **Phases detail** | Inline brief (3-10 lines per step) | 6 separate `.md` files | **Source's approach** — phases 5-6 = one-line handoff to ck:plan/ck:cook |
| **Scripts (Python)** | None | 3 scripts: license-compat, manifest, attribution | **Keep local** — unique value, not in official |
| **Examples** | None in SKILL.md | 3 example files | **Reduce to 1-2 inline** |
| **Resources** | 1 (challenge-framework.md) | 6 files (license/type/challenge/manifest/gotchas/security) | **Keep subset** — license-matrix + security useful |
| **Name** | `ck:xia` (prefixed) | `xia` | **Keep `xia`** — anh đã chọn, không có ck ecosystem dependency |

## Recommendation

### Option A ⭐ — Replace with official + keep local enhancements

**Copy from official:**
- New SKILL.md structure (lean, delegate to ck:plan/ck:cook)
- `--fast` / `--auto` speed flags
- Intent detection keyword table
- "Front door" scope constraint
- Anti-invoke note về ck:brainstorm
- Concise challenge framework (Universal + Architecture + Risk scoring)

**Keep from local (as enhancements):**
- `scripts/check-license-compat.py`
- `scripts/fingerprint-manifest.py`
- `scripts/generate-attribution-header.py`
- `resources/license-compatibility-matrix.md` (data for script)
- 1-2 concrete examples (port-ts-to-python + error-recovery)

**Drop from local:**
- `phases/*.md` (6 files) — redundant với ck:plan/ck:cook
- `resources/cross-stack-gotchas.md` — quá specific
- `resources/type-mappings.md` — quá specific (better as link to external doc)
- Examples 1 (compare-auth) — verbose, không add value

**Result:** ~5-6 files, ~30KB (giữa 12KB official và 152KB local). Best of both worlds.

### Option B — Keep local as-is

Giữ nguyên 152KB. Giá trị: standalone không cần ck ecosystem, có scripts working. Nhược điểm: bloat, trùng logic với ck:plan/ck:cook.

### Option C — Replace fully với official

Copy official 12KB, drop mọi local enhancements. Lean nhất nhưng mất scripts hữu ích.

## Risk Analysis

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| Phase ownership confusion (xia re-invent planning) | Medium | High (without source's note) | Adopt "front door" constraint |
| Speed vs safety tradeoff missing | Low | Medium | Add `--fast`/`--auto` flags |
| Scripts orphan nếu migrate sang official | Medium | Low | Keep trong scripts/ như opt-in |
| Challenge framework too verbose | Low | Medium | Simplify theo source model |
| Missing ck ecosystem deps | High | Low | Document prerequisites rõ |

**Aggregate risk:** 🟡 MEDIUM — Option A clear winner với risk tối thiểu

## Unresolved Questions

1. User có sẵn `ck:plan`, `ck:cook`, `ck:repomix`, `ck:scout` trong môi trường?
2. `ck:xia` prefix có dùng cho future expansion không, hay keep `xia`?
3. Scripts (license/manifest/attribution) có giá trị enterprise — có muốn build thành separate `xia-enterprise` skill?
4. Challenge framework detail level: 6 categories (local) hay 5+5 (source)?
5. Examples: keep inline trong SKILL.md hay files riêng?

## Next Action

Chờ user quyết option. Default recommendation: **Option A** (hybrid merge).

Nếu Option A: chạy `/xia --improve C:/Users/ASUS/Downloads/.../xia xia-skill` để port adoption của lean structure + giữ local scripts.
