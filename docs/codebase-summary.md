# Codebase Summary — vci-skill-cuongbx

> Auto-generated: 2026-04-13

## Project Info

| Field | Value |
|-------|-------|
| Name | vci-skill-cuongbx |
| Version | 2.0.0 |
| Type | AI Skill (Claude Code / Gemini Antigravity) |
| Author | CuongBX — VCI Team |
| License | MIT |

## File Manifest

### Core Skill Files

| File | Lines | Purpose |
|------|-------|---------|
| SKILL.md | ~200 | Skill definition — 10 modes, constraints, examples |
| CLAUDE.md | ~80 | Claude Code project instructions |
| README.md | ~200 | User guide, installation, changelog |

### References (templates, rules, patterns)

| File | Lines | Purpose |
|------|-------|---------|
| references/templates/prd-template.md | 267 | 4-level PRD structure (Level 1-4 + NFR + Appendix) |
| references/templates/dev-guide-template.md | 480 | BE (8 sections) + FE (8 sections) implementation |
| references/templates/test-gen-template.md | 310 | BDD + Security + Performance + Automation |
| references/templates/pm-report-template.md | 232 | Track dashboard (Mode 8) + PMO report (Mode 9) |
| references/rules/gap-detection-rules.md | 180 | Audit rules, auto-fix, code-spec comparison, tech review |
| references/patterns/mermaid-patterns.md | 177 | 6 diagram types: state, flow, ERD, activity, sequence, data |
| references/patterns/ui-mockup-patterns.md | 82 | Code-as-Mockup sync mechanism (React/Tailwind) |

### Examples

| File | Lines | Purpose |
|------|-------|---------|
| examples/example-dispatch-order.md | 276 | Full 4-level example output (dispatch order feature) |

### Legacy (to be removed)

| File | Purpose |
|------|---------|
| resources/prd_template.md | Old path → references/templates/prd-template.md |
| resources/dev_guide_template.md | Old path → references/templates/dev-guide-template.md |
| resources/test_gen_template.md | Old path → references/templates/test-gen-template.md |
| resources/pm_report_template.md | Old path → references/templates/pm-report-template.md |
| resources/gap_detection_rules.md | Old path → references/rules/gap-detection-rules.md |
| resources/mermaid_patterns.md | Old path → references/patterns/mermaid-patterns.md |
| resources/ui-mockup.md | Old path → references/patterns/ui-mockup-patterns.md |
| examples/example_dispatch_order.md | Old path → examples/example-dispatch-order.md |

### ClaudeKit Framework (.claude/)

| Directory | Content |
|-----------|---------|
| .claude/agents/ | 14 AI agents (planner, researcher, tester, etc.) |
| .claude/rules/ | 5 development rules & workflow files |
| .claude/hooks/ | 16 lifecycle hooks + lib/ utilities |
| .claude/skills/ | 10 support skills (ck-plan, ck-debug, code-review, etc.) |
| .claude/output-styles/ | 6 coding level styles (ELI5 to God) |
| .claude/scripts/ | Utility scripts (resolve env, scan, worktree) |
| .claude/schemas/ | ck-config JSON schema |

## Mode Coverage

| Mode | Template | Rules | Patterns | Example |
|------|----------|-------|----------|---------|
| 1. Generate | prd-template | gap-detection | mermaid-patterns | dispatch-order |
| 2. Structure | prd-template | gap-detection | mermaid-patterns | - |
| 3. Update | prd-template | gap-detection | - | - |
| 4. Audit | - | gap-detection | - | - |
| 5. Dev Guide | dev-guide-template | - | - | - |
| 6. Test Gen | test-gen-template | - | - | - |
| 7. Summary | - | - | - | - |
| 8. Track | pm-report-template | - | - | - |
| 9. Report | pm-report-template | - | - | - |
| 10. Mockup | - | - | ui-mockup-patterns | - |

## Total Lines of Documentation

~2,400 lines across all reference files + skill definition.
