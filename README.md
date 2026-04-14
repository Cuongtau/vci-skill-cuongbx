# vci-skill-cuongbx

> **AI Skill sinh tài liệu PRD/Spec chuẩn `.md`** — phục vụ toàn bộ team SDLC (BA, Dev, QA, PM, Tech Lead). 10 modes chia 5 zones theo vai trò. Hỗ trợ enterprise multi-role collaboration, anti-duplication guards, cross-zone compositions.

**Version:** 2.4.0 · **License:** MIT · **Language:** Vietnamese-first (technical English OK)

---

## 🎯 Mục tiêu

Sinh tài liệu PRD/Spec chuẩn trong **10 phút** (thay vì 2-3 giờ) — từ BA viết spec → Dev implement → QA test → PM track → báo cáo PMO.

Đảm bảo **mọi vai trò đều đọc hiểu + sử dụng được** cùng 1 bộ artifact.

---

## 🚀 Cài đặt

### Option 1: Install qua `ck` CLI (recommended)

```bash
# Cài ck CLI
npm install -g claudekit-cli

# Install skill này vào Claude Code global
cd /path/to/vci-skill-cuongbx
ck skills --install --source . --agent claude-code --global
```

Skill sẽ được copy vào `~/.claude/skills/vci-skill-cuongbx/`.

### Option 2: Install manual

```bash
# Claude Code
cp -r . ~/.claude/skills/vci-skill-cuongbx/

# Antigravity (Gemini)
cp -r . ~/.gemini/antigravity/skills/vci-skill-cuongbx/

# Cursor
cp -r . ~/.cursor/skills/vci-skill-cuongbx/
```

### Option 3: Install qua script cross-IDE (nếu clone repo)

```bash
./.claude/skills/install.sh --target claude-code --global
```

---

## 👤 Đối tượng sử dụng

| Vai trò | Modes | Mô tả |
|---------|-------|-------|
| **BA** | 1, 2, 3, 4, 10 | Tạo & quản lý spec đầy đủ 4 level |
| **Backend Dev** | 5A | Implement guide: schema, API, BR, state guards |
| **Frontend Dev** | 5B, 10 | Component tree, validation UX, mockup |
| **Tech Lead** | 4 | Audit spec ↔ code, architecture review |
| **QA / Tester** | 6 | BDD tests, security, performance, automation |
| **PM** | 7, 8, 9 | Summary, dashboard, PMO report |

---

## 📋 10 Modes

```
🟦 Zone BA:      Mode 1 Generate · Mode 2 Structure · Mode 3 Update · Mode 4 Audit
🟩 Zone Dev:     Mode 5A Backend · Mode 5B Frontend
🟨 Zone QA:      Mode 6 Test Gen
🟧 Zone PM:      Mode 7 Summary · Mode 8 Track · Mode 9 Report
🟪 Zone Shared:  Mode 10 Mockup
```

### Quick Start 30 giây

| Câu mở đầu | → Mode |
|---|---|
| *"Tạo spec cho tính năng nhập kho vật tư"* | Mode 1 |
| *"Có meeting notes, cấu trúc giúp em"* | Mode 2 |
| *"Cập nhật spec IMS_NK_01, thêm BR_005"* | Mode 3 |
| *"Audit feature X — spec và code khớp không?"* | Mode 4 |
| *"Dev guide backend cho IMS_NK_01"* | Mode 5A |
| *"Dev guide frontend cho login"* | Mode 5B |
| *"Sinh test cases cho IMS_NK_01"* | Mode 6 |
| *"Tóm tắt feature X cho họp sáng mai"* | Mode 7 |
| *"Ai đang làm gì?"* · *"Tiến độ thế nào?"* | Mode 8 |
| *"Tạo sprint report cho PMO"* | Mode 9 |
| *"Tạo mockup màn đăng nhập"* | Mode 10 |

📚 **Walkthrough từng role:** [`references/quickstart-by-role.md`](references/quickstart-by-role.md)

---

## 🗂️ Cấu trúc repo (= 1 skill)

```
vci-skill-cuongbx/                   Repo = skill installable
├── SKILL.md                          ⭐ Skill definition (entry point)
├── README.md                         Human-facing guide (file này)
├── CLAUDE.md                         Project-specific Claude instructions
├── LICENSE                           MIT
├── references/                       Progressive disclosure refs
│   ├── quickstart-by-role.md         Role-specific walkthroughs
│   ├── enterprise-workflow.md        RACI + CODEOWNERS + lifecycle
│   ├── cross-zone-suggestions.md     Cross-zone composition
│   ├── anti-duplication-guards.md    Hard rules + disambiguation
│   ├── common-pitfalls.md            14 anti-patterns
│   ├── patterns/                     Mermaid, UI mockup patterns
│   ├── rules/                        Gap detection rules
│   ├── templates/                    PRD, Dev Guide, Test, PM Report templates
│   └── scripts/                      Pre-flight check (Python)
├── examples/                         Ví dụ output thực tế
│   └── example-dispatch-order.md
├── docs/                             Project contributor docs
├── plans/                            Planning artifacts + reports
│   ├── reports/
│   └── templates/
└── .claude/                          ⚠️ Companion skills (NOT part of main skill install)
    └── skills/
        └── vci/                     🟦 11 SDLC supporting skills (tracked)
```

---

## 🧩 Companion Zones (cài riêng — repo tách biệt)

Repo này **lean**: chỉ giữ main skill + 1 zone support `vci/`. Các zone khác tách thành **repo riêng** để user cài theo nhu cầu, tránh bloat.

| Zone | Skills | Repo riêng | Install |
|---|---|---|---|
| 🟩 **claudekit** | ~1389 core dev | `skills-claudekit` | `bash scripts/install-companion.sh claudekit` |
| 🟣 **xia** | 1 feature heist | `skills-xia` | `bash scripts/install-companion.sh xia` |
| 🟠 **others** | 9 UI/design | `skills-others` | `bash scripts/install-companion.sh others` |

Install tất cả: `bash scripts/install-companion.sh all`

Windows: dùng `scripts/install-companion.ps1` với `-Target claudekit|xia|others|all`.

📚 **Chi tiết:** [.claude/skills/README.md](.claude/skills/README.md)

---

## ✨ Tính năng nổi bật

### 🏢 Enterprise Multi-role Collaboration

- **Ownership Matrix (RACI)** — 6 artifacts × R/A/C/I roles
- **Spec Lifecycle** — DRAFT → IN_REVIEW → APPROVED → FROZEN → DEPRECATED
- **Git Branching Strategy** — 7 patterns mapped to modes
- **Handoff Protocol** — auto-notify via commit message `[notify: @team]`
- **CODEOWNERS** setup per-module
- **Jira/Slack/Teams integration** — via frontmatter fields

📚 [`references/enterprise-workflow.md`](references/enterprise-workflow.md)

### 🛡️ Anti-duplication Guards (4 hard rules)

AI self-enforce để tránh conflict:
1. Mode 1 vs `business-analyst` — REFUSE duplicate
2. Mode 10 precondition — REFUSE nếu spec chưa có Level 4
3. Mode 4 vs `/xia --compare` — disambiguate local audit vs external
4. KHÔNG invoke `/ck:brainstorm` từ Mode 1/xia

**Pre-flight check:**
```bash
python references/scripts/check-mode-prerequisites.py --mode 10 --spec docs/specs/auth/IMS_AUTH_01/spec.md
```

📚 [`references/anti-duplication-guards.md`](references/anti-duplication-guards.md)

### 🔗 Cross-zone Composition

Mode này → compose với skill zone khác. VD:
- Mode 1 Generate → `mermaid-expert` (diagrams) + `brainstorming` (ideation)
- Mode 4 Audit → `spec-to-code-compliance` + `ck:security`
- Mode 5A Backend → `api-documentation-generator` + `ck:plan`

📚 [`references/cross-zone-suggestions.md`](references/cross-zone-suggestions.md)

### 📐 Pipeline End-to-end (10/10 modes)

```
M2 Structure ──┐                              ┌─ M5A Backend ─┐
                ├→ M1 Generate (PRD) ──┬→ M7 ─┼─ M5B Frontend ─┤
Idea ──────────┘                       │ Summary  M10 Mockup  ├→ Code → M4 Audit
                                        │        M6 Test       │         ↓
                                        └→ Sprint kickoff ─────┘      M3 Update + CR
                                                                          ↓
                                                           M8 Track → M9 PMO Report
```

---

## 🧪 Ví dụ thực tế

**Scenario:** Team cần thêm rate limiter vào feature nhập kho batch.

```
1. /brainstorming rate limiter                    (vci)
2. Tạo spec IMS_NK_02                             (Mode 1 + mermaid-expert)
3. /xia --compare github.com/tj/node-ratelimiter  (xia)
4. /xia --port feature                             (xia → ck:plan + ck:cook)
5. Dev guide backend IMS_NK_02                    (Mode 5A + api-documentation-generator)
6. Sinh test cases                                (Mode 6 + test-automator)
7. Audit spec ↔ code                              (Mode 4 + ck:security)
8. /code-review + /commit                         (claudekit)
9. Mode 8/9 Track + Report                        (Mode 8 + ck:loop)
```

→ 7 skills từ 3 zones, ~2 giờ thay vì 1 tuần thủ công.

📚 **Full demo:** [`references/cross-zone-suggestions.md`](references/cross-zone-suggestions.md)

---

## 📚 Documentation Map

| File | Dành cho |
|---|---|
| [`SKILL.md`](SKILL.md) | AI (skill activation + instructions) |
| `README.md` | Human (file này) |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code IDE instructions |
| [`references/quickstart-by-role.md`](references/quickstart-by-role.md) | Per-role walkthrough với prompt mẫu |
| [`references/enterprise-workflow.md`](references/enterprise-workflow.md) | Enterprise multi-role full guide |
| [`references/templates/`](references/templates/) | PRD, Dev Guide, Test, PM Report templates |
| [`references/patterns/`](references/patterns/) | Mermaid diagrams, UI mockup patterns |
| [`references/rules/`](references/rules/) | Gap detection rules |
| [`examples/example-dispatch-order.md`](examples/example-dispatch-order.md) | Ví dụ PRD hoàn chỉnh |

---

## 🛠️ Prerequisites

- **Claude Code** hoặc **Antigravity** hoặc **Cursor** — IDE hỗ trợ Agent Skills
- **Git 2.20+** — cho branch strategy, changelog tracking
- **Python 3.9+** (optional) — cho pre-flight check scripts
- **Node.js 18+** (optional) — nếu dùng `ck` CLI

---

## 🔄 Versioning

| Version | Date | Key changes |
|---|---|---|
| 2.4.0 | 2026-04-14 | Full 10 modes pipeline + SDLC×Mode matrix + anti-dup guards + pre-flight scripts |
| 2.3.0 | 2026-04-14 | Enterprise multi-role: RACI, CODEOWNERS, spec lifecycle, compliance |
| 2.2.0 | 2026-04-14 | Quick Start + Input/Output Contract + Common Pitfalls |
| 2.1.0 | 2026-04-14 | Restructured 10 modes into 5 zones + decision tree |
| 2.0.0 | 2026-04-13 | Initial 10 modes consolidated |

📋 **Full changelog:** xem comment cuối [`SKILL.md`](SKILL.md)

---

## 🤝 Contributing

1. Fork repo
2. Edit `SKILL.md` hoặc files trong `references/`
3. Run validator: `python .claude/skills/vci/skill-creator-ultra/scripts/validate_skill.py SKILL.md`
4. Đảm bảo **Grade A** trở lên
5. Submit PR

Conventional commits required: `feat:`, `fix:`, `docs:`, `refactor:`

---

## 📝 License

[MIT](LICENSE) © 2026 cuongbx
