# Skills Library — vci-skill-cuongbx

Thư viện skill của project, tổ chức thành **3 vùng** (zone) rõ ràng theo mục đích:

```
.claude/skills/
├── vci-cuongbx/        🟦 11 skills  — hỗ trợ phát triển sản phẩm theo team (tracked in git)
├── claudekit/          🟩 179 skills — full ClaudeKit Engineer catalog (325MB, .gitignored)
└── xia/                🟣 1 skill    — feature heist (port/copy/adapt từ external repo)
```

Tổng cộng **191 skills**, tương thích đa IDE (Claude Code, Antigravity, Cursor, Kilo, Codex, OpenCode, Windsurf, Cline…).

> **Note:** `claudekit/` chứa full 179 skills của ClaudeKit Engineer (~325MB) — physically trên disk để dùng, nhưng **không commit vào git** (đã add vào `.gitignore`). Trên máy khác cần chạy `./.claude/skills/restore-claudekit.sh` để clone lại từ `~/.claude/skills/`.

> Skills là folder chứa instructions, scripts và resources mà AI load động để handle task chuyên biệt. Xem chi tiết: [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)

---

## 🟦 Zone `vci-cuongbx/` — Product Dev Team

Skills phục vụ SDLC end-to-end: BA → Dev → QA → PM. Xem [vci-cuongbx/README.md](./vci-cuongbx/README.md).

| Skill | Vai trò | Dùng ở mode nào |
|---|---|---|
| `skill-creator-ultra` | Meta — tạo/improve skill | Bảo trì skill `vci-skill-cuongbx` |
| `business-analyst` | BA | Mode 1, 2, 3 (Generate, Structure, Update PRD) |
| `product-manager-toolkit` | PM | Mode 7, 8, 9 (Summary, Track, Report) |
| `plan-writing` | Plan | Plans/, implementation roadmap |
| `api-documentation-generator` | Dev | Mode 5A (Backend API docs) |
| `docs-architect` | Docs | Cấu trúc tổng thể `docs/` |
| `mermaid-expert` | Diagram | Mode 1 (State Machine, ERD, Flow) |
| `acceptance-orchestrator` | QA | Mode 6 (AC + test flows) |
| `spec-to-code-compliance` | Tech Lead | Mode 4 (Audit — spec ↔ code) |
| `test-automator` | QA | Mode 6 (Playwright, k6 skeleton) |
| `brainstorming` | BA/PM | Phase 1 ideation |

## 🟩 Zone `claudekit/` — Core Dev Tools

Skills từ ClaudeKit Engineer — dùng chung cho mọi task dev. Xem [claudekit/README.md](./claudekit/README.md).

| Skill | Mục đích |
|---|---|
| `ck-plan` | Planning workflow (research → plan → phases) |
| `ck-debug` | Systematic debugging |
| `ck-loop` | Autonomous loop (long-running tasks) |
| `code-review` | Comprehensive code review |
| `code-reviewer` | Lightweight review |
| `docs` | Docs management (init/update/summarize) |
| `docs-seeker` | Fetch external docs (Context7) |
| `research` | Deep research |
| `scout` | External/internal scouting |
| `repomix` | Repo packaging |
| `template-skill` | Skill scaffold template |
| `commit` | Conventional commits + PR flow |
| `simplify-code` | Code simplification |
| `debugger` | Debug agent |
| `systematic-debugging` | Debug methodology |
| `test-driven-development` | TDD workflow |

---

## 🟣 Zone `xia/` — Feature Heist Tools

Skills port/copy/adapt feature từ external GitHub repo về project local. Xem [xia/README.md](./xia/README.md).

| Skill | Mục đích |
|---|---|
| `xia` | 4 modes (`--compare` / `--copy` / `--improve` / `--port`) + 6-step workflow (Recon → Map → Analyze → Challenge → Plan → Deliver) với license check, attribution tự động, manifest tracking |

---

## Cài đặt / Sync sang IDE khác

Skill format (`SKILL.md` + frontmatter `name:` + `description:`) đã chuẩn Anthropic → **hoạt động trực tiếp** ở:

| IDE / Tool | Đường dẫn install |
|---|---|
| Claude Code | `.claude/skills/` (đã có) hoặc `~/.claude/skills/` |
| Antigravity (Gemini) | `.gemini/skills/` hoặc `~/.gemini/antigravity/skills/` |
| Cursor | `.cursor/skills/` (hoặc convert sang `.cursor/rules/`) |
| Kilo Code | `.kilo/skills/` |
| Codex CLI | `.codex/skills/` |
| OpenCode | `.opencode/skills/` |
| Windsurf | `.windsurf/skills/` |
| Cline | `.cline/skills/` |
| GitHub Copilot | `.github/copilot/skills/` |

### Sync tự động

Dùng script ở `.claude/skills/`:

```bash
# Windows PowerShell
./.claude/skills/install.ps1 -Target antigravity
./.claude/skills/install.ps1 -Target cursor -Global

# macOS/Linux
./.claude/skills/install.sh --target kilo
./.claude/skills/install.sh --target antigravity --global
```

Script dùng **symlink/junction** — sửa 1 chỗ, sync mọi IDE. Xem `install.ps1`/`install.sh` cho options đầy đủ.

### Manual copy (fallback nếu không muốn symlink)

```bash
# Copy toàn bộ 2 zones sang IDE khác
cp -r .claude/skills/vci-cuongbx  ~/.cursor/skills/
cp -r .claude/skills/claudekit    ~/.cursor/skills/
```

---

## Auto-activation

Claude/Gemini tự kích hoạt skill dựa trên `description:` field trong frontmatter SKILL.md. Để skill trigger đúng:

1. Description phải "pushy" — cover nhiều cách user hỏi
2. Name kebab-case, không có "and" (atomic logic)
3. 4 core sections: Goal / Instructions / Examples / Constraints

Dùng `skill-creator-ultra` (trong zone vci-cuongbx) để audit + improve các skill.

---

## Versioning

| Version | Date | Changes |
|---|---|---|
| 2.1.0 | 2026-04-14 | Tách 2 zones (vci-cuongbx + claudekit), thêm 16 skills |
| 2.0.0 | 2026-04-13 | Merge 10 modes PRD/Spec |

<!-- Generated by Skill Creator Ultra v1.0 -->
