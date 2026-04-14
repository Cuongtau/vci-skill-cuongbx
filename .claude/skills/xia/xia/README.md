# `/xia` — Feature Heist Skill

> **Xỉa** (Vietnamese) = *chôm* / pinch / steal.
> Joke từ 谢谢 (xièxie — "thank you" in Chinese). Tức là cảm ơn repo chủ vì cho "xỉa" feature.

## TL;DR

Port tính năng từ external GitHub repo về project local **có suy nghĩ + an toàn** — không copy mù.

```bash
/xia --compare  <repo>  # chỉ so sánh, 0 file thay đổi
/xia --copy     <repo>  # paste + min-fix để chạy
/xia --improve  <repo>  # ⭐ copy + refactor theo local codebase
/xia --port     <repo>  # rewrite hoàn toàn cho local stack (cross-language)
```

## Tại sao `/xia`?

Developers thường port feature giữa repos bằng cách:
- 🤦 **Copy-paste mù** — hoạt động 50% trường hợp, break 50% còn lại
- 😵 **Manual porting 2-4 giờ** — re-invent, nhàm chán, dễ sai
- 🙈 **Vendored forever** — copy xong quên update, drift theo thời gian

`/xia` fix cả 3 vấn đề:
1. **Challenge-driven** — bắt user face hidden assumptions (license, deps, async model, state)
2. **Attribution tự động** — header + NOTICE file + manifest
3. **Idempotency + re-sync** — manifest track what's ported from where

## 6-step Workflow

```
Recon → Map → Analyze → Challenge → Plan → Deliver
```

| Step | Compose với | Output |
|---|---|---|
| **1. Recon** | `ck:repomix`, `ck:docs-seeker` | Source meta, license verdict, cost estimate |
| **2. Map** | `ck:scout`, `spec-to-code-compliance` | 7-layer decomp + dependency matrix |
| **3. Analyze** | `ck:sequential-thinking`, `ck:security` | Execution flow, config surface, security scan |
| **4. Challenge** | `ck:plan --red-team` | 6-category decision matrix + user decisions |
| **5. Plan** | `ck:plan --hard` | Phased roadmap in `plans/{timestamp}/` |
| **6. Deliver** | `ck:cook`, `test-automator`, `code-review` | Attributed code + manifest + git branch |

## 4 modes — Khi nào dùng?

| Mode | Use case | Time | Risk |
|---|---|---|---|
| `--compare` | Research, learning, architecture review | ~10 min | None |
| `--copy` | Same-stack, simple util, quick POC | ~20 min | Medium |
| `--improve` ⭐ | Same-stack, production use | ~40 min | Low |
| `--port` | Cross-stack (TS→Python), rewrite required | ~2 hrs | Low |

## Structure

```
xia/
├── SKILL.md                     # Main skill definition
├── README.md                    # This file
├── phases/                      # 6 phase detail files
│   ├── phase1-recon.md
│   ├── phase2-map.md
│   ├── phase3-analyze.md
│   ├── phase4-challenge.md
│   ├── phase5-plan.md
│   └── phase6-deliver.md
├── resources/
│   ├── license-compatibility-matrix.md
│   ├── type-mappings.md         # Cross-stack type bridging
│   ├── challenge-templates.md   # 6 categories × 3 templates
│   ├── manifest-schema.md       # .xia-manifest.json spec
│   ├── cross-stack-gotchas.md
│   └── security-checklist.md
├── examples/
│   ├── example-compare-auth.md
│   ├── example-port-ts-to-python.md
│   └── example-error-recovery.md
└── scripts/
    ├── check-license-compat.py
    ├── fingerprint-manifest.py
    └── generate-attribution-header.py
```

## Prerequisites

- `ck` CLI (`npm install -g claudekit-cli`)
- Python 3.9+ (for scripts)
- `gh` CLI (GitHub auth for private repos)
- Git (checkpoint commits + rollback)

## Quick start

```bash
# Verify skill loaded
ck skills --list --installed | grep xia

# Test on public MIT repo
/xia --compare https://github.com/sindresorhus/p-retry

# Port a real feature
/xia --improve https://github.com/tj/node-ratelimiter rate-limiter
```

## Manifest example

After port, project root có `.xia-manifest.json`:

```json
{
  "version": "1.0",
  "ports": [{
    "id": "port_001",
    "feature_name": "Rate Limiter",
    "source": {
      "repo": "https://github.com/tj/node-ratelimiter",
      "commit": "a1b2c3d",
      "license": "MIT"
    },
    "port": {"mode": "improve", "date": "2026-04-14"},
    "status": "active"
  }]
}
```

Verify: `python scripts/fingerprint-manifest.py --action verify`

## Hard constraints

- 🚫 **KHÔNG execute** fetched code (prompt injection, supply chain)
- 🚫 **KHÔNG auto-install deps** (typosquatting risk)
- 🚫 **KHÔNG copy secret values** từ `.env` files
- 🚫 **KHÔNG skip Challenge** kể cả `--yes` mode
- 🚫 **KHÔNG port** khi local có uncommitted changes >10 files
- 🚫 **KHÔNG port** khi detect eval + network + obfuscation

## Philosophy

> *"Xỉa không phải là script kiddie copy-paste.
> Xỉa là architecture-level decision-making với due diligence."*

`/xia` ép user đối mặt 6 câu hỏi:
1. **Environment** — version compat
2. **Dependencies** — conflicts, weight
3. **Async** — concurrency model
4. **State** — store paradigm
5. **License** — legal compat
6. **Observability** — logs, metrics

Mỗi câu có Source answer · Local answer · Risk → user chọn `proceed` / `adjust` / `abort`.

## Integration với team (vci-skill-cuongbx)

Sau khi port xong, optional trigger:
- **Mode 5 Dev Guide** — `vci-skill-cuongbx` sinh `dev_guide.md` cho feature mới
- **Mode 6 Test Gen** — supplement tests (BDD scenarios, security cases)

## Troubleshooting

| Issue | Solution |
|---|---|
| `ck repomix` timeout | Narrow với `--include "src/feature/**"` |
| Private repo 404 | `gh auth login` + retry |
| License BLOCK | Review matrix, user override với `--ack-license-risk` |
| Challenge `c` (abort) | Review `.xia/cache/` + adjust upstream or scope |
| Mid-port failure | `/xia rollback port_XXX` |

## Roadmap

- **v1.0** (current) — 4 modes, 6 steps, manifest, attribution
- **v1.1+** — mid-port resume, drift detection (`xia sync`), secret heuristics

---

<!-- Generated by Skill Creator Ultra v1.0 -->
