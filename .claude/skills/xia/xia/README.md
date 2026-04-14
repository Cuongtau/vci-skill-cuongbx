# `/xia` — Skill Xỉa Feature

> **Xỉa** (tiếng Việt) = *chôm / pinch / steal*.
> Chơi chữ từ 谢谢 (xièxie — "cảm ơn" tiếng Trung). Tức là *cảm ơn repo chủ vì cho "xỉa" feature*.

## TL;DR

Port tính năng từ external GitHub repo về project local **có suy nghĩ + an toàn** — không copy mù.

```bash
/xia --compare  <repo>  # chỉ so sánh, 0 file thay đổi
/xia --copy     <repo>  # paste + min-fix để chạy
/xia --improve  <repo>  # ⭐ copy + refactor theo local codebase
/xia --port     <repo>  # rewrite hoàn toàn cho local stack (cross-language)
```

Speed flags:
- `--fast` — bỏ qua research + challenge, auto-approve (quick experiment)
- `--auto` — giữ full workflow nhưng auto-approve gates (CI/batch)
- default — full workflow + user approve mỗi gate (production port)

## Tại sao `/xia`?

Developers thường port feature giữa repos bằng cách:
- 🤦 **Copy-paste mù** — chạy được 50% trường hợp, break 50% còn lại
- 😵 **Manual porting 2-4 giờ** — reinvent, nhàm chán, dễ sai
- 🙈 **Vendored forever** — copy xong quên update, drift theo thời gian

`/xia` fix cả 3 vấn đề:
1. **Challenge-driven** — ép user đối mặt hidden assumptions (license, deps, async model, state)
2. **Attribution tự động** — header comment + NOTICE file + manifest
3. **Idempotent + re-sync** — manifest track đã port gì từ đâu

## Triết lý

> **Hiểu trước khi copy · Chất vấn trước khi implement · Adapt, đừng transplant**

`/xia` là **front door**, không phải orchestration stack. Planning + delivery giao cho `ck:plan` + `ck:cook`. Không reinvent.

## 6-step Workflow

```
Recon → Map → Analyze → Challenge → Plan → Deliver
```

| Step | Compose với | Output |
|---|---|---|
| **1. Recon** | `ck:repomix`, `ck:docs-seeker`, `researcher` | Source meta, license verdict, cost estimate |
| **2. Map** | `ck:scout` | 7-layer decomp + dependency matrix |
| **3. Analyze** | `ck:sequential-thinking`, `ck:security` | Execution flow, config surface, security scan |
| **4. Challenge** | `brainstormer` (nếu cần) | Decision matrix + user decisions |
| **5. Plan** | **`ck:plan --hard`** (delegate) | Phased plan trong `plans/` |
| **6. Deliver** | **`ck:cook`** (delegate) | Code changes + tests + git commit |

## 4 modes — Khi nào dùng?

| Mode | Use case | Thời gian | Risk |
|---|---|---|---|
| `--compare` | Research, learning, architecture review | ~10 min | Không |
| `--copy` | Same-stack, util đơn giản, quick POC | ~20 min | Medium |
| `--improve` ⭐ | Same-stack, production use | ~40 min | Low |
| `--port` | Cross-stack (TS→Python), cần rewrite | ~2 hrs | Low |

## Cấu trúc

```
xia/
├── SKILL.md                     # Main skill definition
├── README.md                    # File này
├── references/
│   ├── challenge-framework.md   # Universal + Architecture + Risk scoring
│   ├── license-compatibility-matrix.md
│   ├── manifest-schema.md       # .xia-manifest.json spec
│   └── security-checklist.md
├── examples/
│   ├── example-port-ts-to-python.md
│   └── example-error-recovery.md
└── scripts/
    ├── check-license-compat.py
    ├── fingerprint-manifest.py
    └── generate-attribution-header.py
```

## Prerequisites

- `ck` CLI (`npm install -g claudekit-cli`)
- Python 3.9+ (chạy scripts)
- `gh` CLI (auth GitHub cho private repo)
- Git (checkpoint commits + rollback)

## Quick start

```bash
# Verify skill loaded
ck skills --list --installed | grep xia

# Test on public MIT repo
/xia --compare https://github.com/sindresorhus/p-retry

# Port real feature
/xia --improve https://github.com/tj/node-ratelimiter rate-limiter

# Quick experiment (skip challenges)
/xia --port --fast https://github.com/some/lib feature

# Batch mode (CI)
/xia --improve --auto https://github.com/some/lib feature
```

## Manifest example

Sau port, project root sẽ có `.xia-manifest.json`:

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
- 🚫 **KHÔNG skip Challenge** trừ khi dùng `--fast` mode (với risk)
- 🚫 **KHÔNG invoke `/ck:brainstorm`** từ xia (phase ownership confusion)
- 🚫 **KHÔNG reinvent** planning/delivery — giao `ck:plan`/`ck:cook`

## Challenge philosophy

`/xia` ép user đối mặt ≥5 câu hỏi (6 categories):
1. **Environment** — version compat
2. **Dependencies** — conflicts, weight, CVE
3. **Async** — concurrency model mismatch
4. **State** — store paradigm
5. **License** — legal compat + attribution
6. **Observability** — logs, metrics, error handling

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
| Challenge `c` (abort) | Review `.xia/cache/` + adjust upstream hoặc scope |
| Mid-port failure | `/xia rollback port_XXX` |

## Roadmap

- **v2.0** (current) — Lean front-door pattern, việt hóa, --fast/--auto flags
- **v2.1+** — Mid-port resume, drift detection (`xia sync`), secret heuristics

---

<!-- Generated by Skill Creator Ultra v1.0 -->
