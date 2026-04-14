# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

**vci-skill-cuongbx** là một AI Skill cho Claude Code / Gemini Antigravity, chuyên sinh tài liệu PRD/Spec chuẩn `.md` phục vụ toàn bộ team phát triển sản phẩm (BA, Dev, QA, Tester, PM, Tech Lead). Skill hỗ trợ **10 chế độ** hoạt động từ Generate spec đến Mockup UI.

## Role & Responsibilities

Your role is to maintain, improve, and extend this skill — ensuring all 10 modes work correctly, templates are comprehensive, gap detection rules are thorough, and output quality is consistently high.

## Workflows

- Primary workflow: `./.claude/rules/primary-workflow.md`
- Development rules: `./.claude/rules/development-rules.md`
- Orchestration protocols: `./.claude/rules/orchestration-protocol.md`
- Documentation management: `./.claude/rules/documentation-management.md`
- Team coordination: `./.claude/rules/team-coordination-rules.md`

## Project Structure

```
vci-skill-cuongbx/
├── SKILL.md                           ← Skill definition (10 modes)
├── CLAUDE.md                          ← This file
├── README.md                          ← User guide & installation
├── .claude/                           ← ClaudeKit framework
│   ├── agents/                        ← 14 AI agents
│   ├── rules/                         ← Development rules & workflows
│   ├── hooks/                         ← Lifecycle hooks
│   ├── skills/                        ← Support skills (ck-plan, ck-debug, etc.)
│   ├── output-styles/                 ← Coding level styles
│   ├── scripts/                       ← Utility scripts
│   └── settings.json                  ← Hook configuration
├── references/                        ← Reference docs for skill modes
│   ├── templates/                     ← Output templates (PRD, dev guide, test, PM report)
│   ├── rules/                         ← Quality & detection rules
│   └── patterns/                      ← Diagram & UI patterns
├── examples/                          ← Example outputs
├── docs/                              ← Project documentation
├── plans/                             ← Implementation plans
└── guide/                             ← Skills catalog & environment resolver
```

## Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Core skill definition — 10 modes, constraints, examples |
| `references/templates/prd-template.md` | 4-level PRD/Spec template |
| `references/templates/dev-guide-template.md` | Backend (8 sections) + Frontend (8 sections) |
| `references/templates/test-gen-template.md` | BDD, security, performance, automation |
| `references/templates/pm-report-template.md` | Track dashboard + PMO report |
| `references/rules/gap-detection-rules.md` | Audit rules & code-spec comparison |
| `references/patterns/mermaid-patterns.md` | 6 diagram types with examples |
| `references/patterns/ui-mockup-patterns.md` | Code-as-Mockup sync mechanism |

## Development Principles

- **YAGNI**: Avoid over-engineering — skill should do exactly what 10 modes define
- **KISS**: Templates must be simple enough for BA/PM to understand
- **DRY**: Share common patterns across modes (gap detection, changelog, TOC)
- **Vietnamese-first**: Primary language is Vietnamese, technical terms in English

## Important Rules

- **MUST** keep SKILL.md under 350 lines — reference `references/` for details
- **MUST** run gap detection after any template change
- **MUST** maintain cross-references: BR → AC, State → Button, API → AC
- **MUST NOT** fabricate data — mark unknown info as `[⚠️ CẦN XÁC NHẬN]`
- **MUST NOT** auto-update spec `.md` when editing mockup `.tsx` without user consent
- **MUST** use kebab-case for all file names in `references/`
- **MUST** follow conventional commits for git history

## Git

- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
- **DO NOT** use `chore` or `docs` for file changes in `.claude/` directory

## Documentation Management

Keep all docs in `./docs` folder:

```
./docs
├── project-overview-pdr.md
├── code-standards.md
├── codebase-summary.md
└── system-architecture.md
```

## Python Scripts (Skills)

When running Python scripts from `.claude/skills/`, use the venv Python interpreter:
- **Windows:** `.claude\skills\.venv\Scripts\python.exe scripts\xxx.py`
- **Linux/macOS:** `.claude/skills/.venv/bin/python3 scripts/xxx.py`

## Modularization

- If a code file exceeds 200 lines, consider modularizing
- Use kebab-case naming with long descriptive names
- Write descriptive code comments
