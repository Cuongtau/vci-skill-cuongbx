# Skills Library — vci-skill-cuongbx

Thư viện skill của project, tổ chức thành **4 vùng** (zone) rõ ràng theo mục đích:

```
.claude/skills/
├── vci/         🟦 11  skills  — SDLC (BA/Dev/QA/PM/design)
├── claudekit/   🟩 ~1389 skills — full ClaudeKit Engineer catalog
├── xia/         🟣 1   skill   — feature heist (port từ external repo)
└── others/      🟠 9   skills  — Antigravity UI/design skills
```

Tổng cộng **~1410 skills**, **TẤT CẢ tracked in git** — clone về là dùng ngay, không cần sync. Tương thích đa IDE (Claude Code, Antigravity, Cursor, Kilo, Codex, OpenCode, Windsurf, Cline, GitHub Copilot).

> **Repo size:** ~345MB. Clone lần đầu hơi lâu (3-10 min tùy mạng), nhưng sau đó dùng offline thoải mái. Sync scripts chỉ dùng khi muốn **update từ upstream** (pull bản mới của claudekit/others).

> Skills là folder chứa instructions, scripts và resources mà AI load động để handle task chuyên biệt. Xem [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills).

---

## Sync direction matrix

| Zone | Direction | Git tracked | Source upstream |
|---|---|---|---|
| **vci** | bidirectional | ✅ yes | `~/.claude/skills/<each-skill>/` |
| **claudekit** | pull-only | ✅ yes | `~/.claude/skills/` (full catalog) |
| **xia** | bidirectional | ✅ yes | `~/.claude/skills/xia/` |
| **others** | pull-only | ✅ yes | `~/.gemini/antigravity/skills/` |

- **bidirectional**: Sửa local → push lên global qua `sync-to-global.sh` để mọi project dùng bản mới.
- **pull-only**: Source-of-truth ở upstream — chỉ pull về (khi upstream cập nhật), không push.

---

## 🟦 Zone `vci/` — Product Dev Team (SDLC)

Skills phục vụ SDLC end-to-end: BA → Dev → QA → PM. Xem [vci/README.md](./vci/README.md).

| Skill | Vai trò | Mode liên quan |
|---|---|---|
| `skill-creator-ultra` | Meta — tạo/improve skill | Maintenance |
| `business-analyst` | BA | Mode 1, 2, 3 |
| `product-manager-toolkit` | PM | Mode 7, 8, 9 |
| `plan-writing` | Plan | Plans + roadmap |
| `api-documentation-generator` | Dev | Mode 5A |
| `docs-architect` | Docs | Cấu trúc `docs/` |
| `mermaid-expert` | Diagram | Mode 1 |
| `acceptance-orchestrator` | QA | Mode 6 |
| `spec-to-code-compliance` | Tech Lead | Mode 4 |
| `test-automator` | QA | Mode 6 |
| `brainstorming` | BA/PM | Phase 1 ideation |

## 🟩 Zone `claudekit/` — Core Dev Tools

Catalog đầy đủ của ClaudeKit Engineer (~1389 skills). Truy cập qua `/claudekit <skill-name>` slash command. Xem `.claude/commands/claudekit.md`.

Notable: `ck-plan`, `ck-debug`, `ck-loop`, `code-review`, `commit`, `simplify-code`, `tdd-workflow`, `docs-seeker`, `repomix`...

## 🟣 Zone `xia/` — Feature Heist

Single skill `xia` với 4 modes (`--compare` / `--copy` / `--improve` / `--port`) + 6-step workflow. Xem [xia/README.md](./xia/README.md).

## 🟠 Zone `others/` — UI/Design (Antigravity)

10 skills về UI/UX design, frontend, design systems từ Antigravity:

`design-orchestration`, `design-spells`, `frontend-design`, `radix-ui-design-system`, `react-ui-patterns`, `superpowers`, `ui-skills`, `ui-ux-designer`, `ui-ux-pro-max-skill`, `web-design-guidelines`.

---

## 🔗 Cross-zone composition

Skills **không tự invoke skill khác** — user phải gọi explicit. Bảng dưới gợi ý compose:

```
🟦 vci (SDLC)    🟩 claudekit (core)    🟣 xia (heist)    🟠 others (UI)
   │                  │                      │                 │
   │  Mode 1  ──► mermaid-expert (vci)                          │
   │            brainstorming (vci)                             │
   │            ck:plan (ck) ── if complex                      │
   │  Mode 4  ──► code-review (ck)                              │
   │            ck:security (ck)                                │
   │  Mode 5A ──► api-documentation-gen (vci)                   │
   │            xia --port (xia) ─ port lib                     │
   │  Mode 5B ──► frontend-design (others)                      │
   │            ui-ux-designer (others)                         │
   │  Mode 6  ──► test-automator (vci)                          │
   │            tdd-workflow (ck)                               │
   │  Mode 10 ──► radix-ui-design-system (others)               │
   │            react-ui-patterns (others)                      │
   │                                                              │
   └── After all: code-review → simplify-code → commit (ck) ────┘
```

📚 **Full cross-zone map:** [../../references/cross-zone-suggestions.md](../../references/cross-zone-suggestions.md)

### Anti-duplication

- ❌ Gọi `/ck:brainstorm` từ trong `/xia` — phá phase ownership
- ❌ Mode 1 + `business-analyst` cùng feature — Mode 1 đã include BA
- ❌ `xia --compare` + Mode 4 cùng feature — khác scope
- ❌ Mode 10 Mockup khi spec chưa có Level 4

📚 **Chi tiết:** [../../references/anti-duplication-guards.md](../../references/anti-duplication-guards.md)

---

## Cài đặt / Sync sang IDE khác

Skill format chuẩn Anthropic → hoạt động trực tiếp ở:

| IDE | Đường dẫn install |
|---|---|
| Claude Code | `.claude/skills/` hoặc `~/.claude/skills/` |
| Antigravity | `.gemini/skills/` hoặc `~/.gemini/antigravity/skills/` |
| Cursor | `.cursor/skills/` |
| Kilo Code | `.kilo/skills/` |
| Codex CLI | `.codex/skills/` |
| OpenCode | `.opencode/skills/` |
| Windsurf | `.windsurf/skills/` |
| Cline | `.cline/skills/` |
| GitHub Copilot | `.github/copilot/skills/` |

### Sync scripts

```bash
# Pull from global locations into project zones
bash scripts/sync-from-global.sh                    # all
bash scripts/sync-from-global.sh --zone claudekit   # specific

# Push bidirectional zones (vci, xia) → global
bash scripts/sync-to-global.sh --dry-run

# Install skills to other IDEs (symlink/junction)
bash scripts/install-all-ides.sh                    # all IDEs
bash scripts/install-all-ides.sh --target cursor    # specific

# Audit zones — count, diff with global
python scripts/audit-skills.py
python scripts/audit-skills.py --diff-global
```

Windows: dùng `.ps1` thay vì `.sh`.

---

## Auto-activation

Claude/Gemini tự kích hoạt skill dựa trên `description:` field trong frontmatter SKILL.md. Để skill trigger đúng:

1. Description phải "pushy" — cover nhiều cách user hỏi
2. Name kebab-case, atomic logic (không có "and")
3. 4 core sections: Goal / Instructions / Examples / Constraints

Dùng `skill-creator-ultra` (zone `vci`) để audit + improve các skill.

---

## Versioning

| Version | Date | Changes |
|---|---|---|
| 2.5.0 | 2026-04-14 | 4 zones (vci + claudekit + xia + others), unified manifest + sync scripts, cross-IDE installer |
| 2.4.0 | 2026-04-14 | Anti-duplication guards + enterprise workflow |
| 2.1.0 | 2026-04-14 | 2 zones split |
| 2.0.0 | 2026-04-13 | Merge 10 modes PRD/Spec |

<!-- Generated by Skill Creator Ultra v1.0 -->
