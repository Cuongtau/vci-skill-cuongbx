# System Architecture — vci-skill-cuongbx

## Overview

vci-skill-cuongbx la mot AI Skill hoat dong nhu mot "virtual BA/Dev/QA/PM assistant" — nhan input tu nhien (tieng Viet) va sinh ra tai lieu chuan .md phu hop voi tung vai tro trong SDLC.

## Architecture Diagram

```
User Input (Natural Language)
       │
       ▼
┌─────────────────┐
│   Mode Router   │  ← SKILL.md Buoc 0: Nhan dien vai tro & mode
│  (10 modes)     │
└─────┬───────────┘
      │
      ├── Mode 1-3: Generate/Structure/Update
      │       │
      │       ▼
      │   ┌──────────────────┐
      │   │  PRD Template    │  ← references/templates/prd-template.md
      │   │  Engine          │
      │   └──────┬───────────┘
      │          │
      │          ▼
      │   ┌──────────────────┐
      │   │  Gap Detection   │  ← references/rules/gap-detection-rules.md
      │   │  + Auto-Fix      │
      │   └──────┬───────────┘
      │          │
      │          ▼
      │   ┌──────────────────┐
      │   │  Mermaid Gen     │  ← references/patterns/mermaid-patterns.md
      │   └──────────────────┘
      │
      ├── Mode 4: Audit
      │       │
      │       ▼
      │   ┌──────────────────┐
      │   │  Gap Detection   │  Full checklist (Level 1-4)
      │   │  Code-Spec       │  RTM + Deviation Report
      │   │  Tech Review     │  Architecture, Security, Perf
      │   └──────────────────┘
      │
      ├── Mode 5: Dev Guide
      │       │
      │       ▼
      │   ┌──────────────────┐
      │   │  Dev Guide       │  ← references/templates/dev-guide-template.md
      │   │  Template        │
      │   │  BE: 8 sections  │
      │   │  FE: 8 sections  │
      │   └──────────────────┘
      │
      ├── Mode 6: Test Gen
      │       │
      │       ▼
      │   ┌──────────────────┐
      │   │  Test Gen        │  ← references/templates/test-gen-template.md
      │   │  Template        │
      │   │  BDD + Security  │
      │   │  + Performance   │
      │   └──────────────────┘
      │
      ├── Mode 7-9: Summary/Track/Report
      │       │
      │       ▼
      │   ┌──────────────────┐
      │   │  PM Report       │  ← references/templates/pm-report-template.md
      │   │  + Git Log       │  git log --oneline --since="1 week ago"
      │   │  + Spec Scan     │  docs/specs/ changelogs
      │   └──────────────────┘
      │
      └── Mode 10: Mockup
              │
              ▼
          ┌──────────────────┐
          │  UI Mockup       │  ← references/patterns/ui-mockup-patterns.md
          │  React/Tailwind  │
          │  Cross-Sync      │  Spec ↔ Mockup
          └──────────────────┘
              │
              ▼
       docs/specs/{module}/{Feature_ID}_{ten}/
       ├── spec.md
       ├── dev_guide.md
       ├── test_cases.md
       └── test_mapping.md
```

## Data Flow

### Input Sources
1. **User text** — mo ta nghiep vu, meeting notes, yeu cau
2. **Existing specs** — docs/specs/ (cho Update, Audit, Dev Guide, Test Gen)
3. **Source code** — code files (cho Audit Mode 4 Code-Spec comparison)
4. **Git history** — git log (cho Track Mode 8, Report Mode 9)

### Output Artifacts
1. **spec.md** — PRD 4 level voi TOC, Changelog, Scope Baseline, CR Log
2. **dev_guide.md** — Backend (8 sections) hoac Frontend (8 sections)
3. **test_cases.md** — BDD + State×Button Matrix + Security + Performance
4. **test_mapping.md** — Requirement → Test traceability matrix
5. **Mockup .tsx** — React/Tailwind static components
6. **Dashboard/Report** — truc tiep trong conversation (khong tao file)

### Quality Gates
1. **Gap Detection** — auto-run sau moi Generate/Structure/Update
2. **Auto-Fix** — 🔴 Critical gaps fixed truoc khi tra output
3. **Cross-reference** — BR↔AC, State↔Button, Field↔Validate, API↔AC
4. **Scope Change Detection** — CR tu dong khi Approved spec bi sua

## Component Interaction

```
references/templates/     references/rules/      references/patterns/
       │                        │                       │
       └────────────┬───────────┘───────────────────────┘
                    │
                    ▼
              SKILL.md (Mode Router)
                    │
                    ├── reads templates for output structure
                    ├── applies rules for quality validation
                    ├── uses patterns for diagrams & mockups
                    │
                    ▼
              Output Files (docs/specs/...)
```

## ClaudeKit Integration

```
.claude/
├── agents/          ← 14 AI agents for orchestration
├── rules/           ← Development rules (YAGNI, KISS, DRY)
├── hooks/           ← Lifecycle hooks
│   ├── session-init       ← Project detection, env setup
│   ├── scout-block        ← Block node_modules from search
│   ├── privacy-block      ← Scan for secrets
│   ├── dev-rules-reminder ← Inject quality rules
│   └── plan-format-kanban ← Format plans as kanban
├── skills/          ← Support skills
│   ├── ck-plan      ← Planning workflow
│   ├── ck-debug     ← Debugging workflow
│   ├── code-review  ← Code review
│   └── scout        ← Codebase exploration
└── settings.json    ← Hook configuration
```
