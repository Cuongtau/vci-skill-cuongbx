# vci-skill-cuongbx

> AI Skill sinh tai lieu PRD/Spec chuan `.md` phuc vu toan bo team phat trien san pham.

## Muc tieu

Sinh tai lieu PRD/Spec chuan trong **10 phut** (thay vi 2-3 gio), phuc vu toan bo team SDLC — tu BA viet spec, Dev implement, QA test, den PM track progress va bao cao PMO.

## Doi tuong su dung

| Vai tro | Modes | Mo ta |
|---------|-------|-------|
| BA | Generate, Structure, Update, Audit, Mockup | Tao & quan ly spec day du |
| Backend Dev | Dev Guide (BE) | Huong dan implement: schema, API, guards |
| Frontend Dev | Dev Guide (FE), Mockup | Components, validation UX, mockup |
| Tech Lead | Audit (Tech Review) | Architecture, performance, security review |
| QA / Tester | Test Gen | BDD tests, security, performance, automation |
| PM | Summary, Track, Report | Dashboard, bao cao PMO, release notes |

## 10 Modes

| # | Mode | Lenh su dung | Mo ta |
|---|------|--------------|-------|
| 1 | **Generate** | `tao spec [ten feature]` | Sinh PRD 4 level tu mo ta nghiep vu |
| 2 | **Structure** | `cau truc lai [meeting notes]` | Bien thong tin roi rac thanh spec chuan |
| 3 | **Update** | `cap nhat spec [feature_id]` | Sua spec + auto changelog + CR detection |
| 4 | **Audit** | `kiem tra spec [feature_id]` | Gap detection + Code-Spec comparison + RTM |
| 5 | **Dev Guide** | `dev guide [BE/FE] cho [feature]` | Sinh huong dan implement (BE hoac FE) |
| 6 | **Test Gen** | `sinh test [feature_id]` | BDD test + Security + Performance + Automation |
| 7 | **Summary** | `tom tat [feature_id]` | Tom tat 1 trang cho PM |
| 8 | **Track** | `tien do` hoac `ai dang lam gi` | Dashboard hoat dong tu git + spec |
| 9 | **Report** | `bao cao PMO` hoac `report` | Bao cao tien do + Release Notes |
| 10 | **Mockup** | `tao mockup [feature_id]` | Giao dien Mockup tinh React/Tailwind |

## Cai dat

### Yeu cau

- [Claude Code](https://claude.ai/code) hoac [Gemini Antigravity](https://gemini.google.com) da cai dat
- Git
- Node.js 18+ (optional, cho ClaudeKit hooks)

### Cach 1: Clone truc tiep (Khuyen nghi)

**Windows (PowerShell):**
```powershell
git clone https://github.com/Cuongtau/vci-skill-cuongbx.git "$env:USERPROFILE\.gemini\antigravity\skills\vci-skill-cuongbx"
```

**macOS / Linux:**
```bash
git clone https://github.com/Cuongtau/vci-skill-cuongbx.git ~/.gemini/antigravity/skills/vci-skill-cuongbx
```

### Cach 2: Dung voi Claude Code

```bash
# Clone repo
git clone https://github.com/Cuongtau/vci-skill-cuongbx.git
cd vci-skill-cuongbx

# Bat dau Claude Code
claude
```

### Cach 3: Cap nhat skill

```bash
cd ~/.gemini/antigravity/skills/vci-skill-cuongbx   # macOS/Linux
cd $env:USERPROFILE\.gemini\antigravity\skills\vci-skill-cuongbx   # Windows
git pull origin master
```

### Kiem tra cai dat

Mo AI agent va thu noi:
```
Tao spec cho tinh nang dang nhap
```
Neu AI nhan dien skill va bat dau hoi thong tin → **cai dat thanh cong!**

## Cau truc output

```
docs/specs/{module}/{Feature_ID}_{ten}/
├── spec.md          ← PRD 4 level (Auto TOC, Changelog, CR Log)
├── diagrams.md      ← Mermaid (optional, khi spec > 500 dong)
├── dev_guide.md     ← Huong dan implement (BE hoac FE)
├── test_cases.md    ← BDD + Matrix + Security + Performance
└── test_mapping.md  ← Requirement → Test traceability
```

## Tinh nang noi bat

- **Auto Gap Detection** — Tu phat hien spec thieu AC, State thieu Button, Field thieu Validate
- **Auto-Fix Critical** — Tu dong bo sung gap 🔴 Critical truoc khi tra output
- **Mermaid Diagrams** — State Machine, Screen Flow, ERD, Sequence, Data Flow
- **Scope Change Detection** — Tu tao Change Request khi spec Approved bi sua
- **Code-Spec Comparison** — So sanh code vs spec → RTM + Deviation Report
- **Auto Changelog** — Version + Author + Date + Changes tu dong
- **Mockup Sync** — Code-as-Mockup React/Tailwind, dong bo cheo Spec↔Mockup
- **BDD Test Cases** — Tu AC sinh Given/When/Then
- **Security & Perf Tests** — SQL injection, XSS, RBAC, k6 load test
- **Automation Skeleton** — Playwright template code
- **PM Dashboard** — Progress Matrix, Scope Alerts, Activity tracking
- **Release Communication** — Email/Slack template cho stakeholders

## Su dung

Chat voi AI bang ngon ngu tu nhien:

### BA
```
tao spec cho tinh nang nhap kho vat tu
cau truc lai meeting notes thanh spec
cap nhat spec IMS_NK_01 them business rule moi
kiem tra spec IMS_NK_01 co thieu gi khong
tao mockup cho man hinh nhap kho
```

### Developer
```
dev guide backend cho feature nhap kho
dev guide frontend cho feature IMS_NK_01
so sanh code voi spec IMS_NK_01
```

### QA / Tester
```
sinh test cases cho feature IMS_NK_01
sinh test matrix cho nhap kho
tao automation script cho IMS_NK_01
```

### PM
```
ai dang lam gi?
tom tat feature nhap kho
bao cao PMO sprint nay
tien do du an hien tai
```

## Cau truc Project

```
vci-skill-cuongbx/
├── SKILL.md                           ← Skill definition (10 modes)
├── CLAUDE.md                          ← Claude Code instructions
├── README.md                          ← This file
├── .claude/                           ← ClaudeKit framework
│   ├── agents/                        ← 14 AI agents (planner, researcher, tester...)
│   ├── rules/                         ← Development rules & workflows
│   ├── hooks/                         ← Lifecycle hooks (session, privacy, scout)
│   ├── skills/                        ← Support skills (ck-plan, ck-debug, etc.)
│   ├── output-styles/                 ← Coding level styles (ELI5 → God)
│   └── settings.json                  ← Hook configuration
├── references/                        ← Reference docs (ClaudeKit-style)
│   ├── templates/                     ← Output templates
│   │   ├── prd-template.md            ← PRD 4-level template
│   │   ├── dev-guide-template.md      ← BE (8 sections) + FE (8 sections)
│   │   ├── test-gen-template.md       ← BDD + Security + Perf + Automation
│   │   └── pm-report-template.md      ← Track dashboard + PMO report
│   ├── rules/                         ← Quality rules
│   │   └── gap-detection-rules.md     ← Audit + Tech Lead checklist
│   └── patterns/                      ← Reusable patterns
│       ├── mermaid-patterns.md        ← 6 diagram types
│       └── ui-mockup-patterns.md      ← Code-as-Mockup sync
├── examples/                          ← Example outputs
│   └── example-dispatch-order.md      ← Full 4-level example
├── docs/                              ← Project documentation
├── plans/                             ← Implementation plans
└── guide/                             ← Skills catalog & environment
```

## ClaudeKit Integration

Project nay duoc tich hop **ClaudeKit Engineer** framework de ho tro phat trien:

- **14 AI Agents**: planner, researcher, code-reviewer, tester, docs-manager...
- **Lifecycle Hooks**: session-init, privacy-block, scout-block, dev-rules-reminder
- **Support Skills**: `/ck:plan`, `/ck:debug`, `/ck:scout`, `/ck:docs`
- **Development Rules**: YAGNI, KISS, DRY, modularization, quality gates

### ClaudeKit commands (khi dung Claude Code):
```bash
/ck:plan "improve gap detection rules"
/ck:debug "fix mode 4 audit issues"
/ck:scout "explore references/ structure"
/ck:docs                                    # Update documentation
```

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-04-13 | ClaudeKit integration, restructure references/, improved SKILL.md |
| 1.2.0 | 2026-04-09 | Them tinh nang Mockup Code tinh (Mode 10) |
| 1.1.1 | 2026-03-11 | Cai thien README: huong dan cai dat, lenh su dung |
| 1.1.0 | 2026-03-11 | Nang cap: them advanced features, 9 modes hoan chinh |
| 1.0.0 | 2026-03-11 | Initial release — 9 modes |

## License

MIT

## Author

**CuongBX** — VCI Team

---

> Gop y & bao loi: Tao [Issue](https://github.com/Cuongtau/vci-skill-cuongbx/issues) tren GitHub
