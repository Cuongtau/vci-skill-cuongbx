# Skills Library — vci-skill-cuongbx

Repo chính chứa **main skill** `vci-skill-cuongbx` + **1 local zone** (companion helpers).

```
.claude/skills/
└── vci/         🟦 11 skills — support skills tightly coupled với main skill
```

## Zone `vci/` — SDLC Support Skills

11 skills hỗ trợ main skill (10 modes PRD/Spec):

| Skill | Vai trò | Mode liên quan |
|---|---|---|
| `skill-creator-ultra` | Meta — audit/improve skills | Maintenance |
| `business-analyst` | BA | Mode 1, 2, 3 |
| `product-manager-toolkit` | PM | Mode 7, 8, 9 |
| `plan-writing` | Planning | Plans + roadmap |
| `api-documentation-generator` | Dev | Mode 5A |
| `docs-architect` | Docs | Cấu trúc `docs/` |
| `mermaid-expert` | Diagram | Mode 1 |
| `acceptance-orchestrator` | QA | Mode 6 |
| `spec-to-code-compliance` | Tech Lead | Mode 4 |
| `test-automator` | QA | Mode 6 |
| `brainstorming` | BA/PM | Phase 1 ideation |

## Companion Zones (cài riêng)

Các zone khác tách thành **repo riêng biệt** — user cài theo nhu cầu:

| Zone | Skills | Repo | Install |
|---|---|---|---|
| 🟩 **claudekit** | ~1389 core dev | `skills-claudekit` | `bash scripts/install-companion.sh claudekit` |
| 🟣 **xia** | 1 feature heist | `skills-xia` | `bash scripts/install-companion.sh xia` |
| 🟠 **others** | 9 UI/design | `skills-others` | `bash scripts/install-companion.sh others` |

Install all: `bash scripts/install-companion.sh all`

Windows: dùng `.ps1` thay `.sh`.

Sau khi cài, companion skills xuất hiện tại `.claude/skills/{claudekit,xia,others}/` — tự động kích hoạt qua description frontmatter.

## Audit

```bash
python scripts/audit-skills.py            # human-readable
python scripts/audit-skills.py --json     # machine-readable
```
