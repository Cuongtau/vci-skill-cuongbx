---
name: claudekit
description: |
  Entry point cho ClaudeKit core dev tools — 179 skills. Route tới sub-skill: plan,
  cook, debug, debugger, systematic-debugging, code-review, code-reviewer, commit,
  simplify-code, research, scout, docs-seeker, repomix, test-driven-development,
  v.v. Dùng khi user nói "plan task", "debug bug", "code review", "commit",
  "research X", "simplify", "scout codebase".
argument-hint: "<sub-skill> [args]"
---

# /claudekit — ClaudeKit Core Dev Tools Router

Load skill `claudekit/<sub-skill>` từ `.claude/skills/claudekit/{skill-name}/SKILL.md`.

## 🔝 Top 16 sub-skills thường dùng nhất

### Planning & Execution
| Command | Sub-skill | Mục đích |
|---|---|---|
| `/claudekit plan <task>` | `ck-plan` | Planning với research + red-team + phases |
| `/claudekit cook <plan-path>` | (via ck:cook) | Execute plan phase-by-phase |
| `/claudekit loop <interval>` | `ck-loop` | Autonomous long-running tasks |

### Debug & Investigation
| Command | Sub-skill | Mục đích |
|---|---|---|
| `/claudekit debug <issue>` | `ck-debug` | Full debug workflow (log + CI + repro) |
| `/claudekit debugger <issue>` | `debugger` | Lightweight debug agent |
| `/claudekit systematic-debugging <issue>` | `systematic-debugging` | Methodology: bisect, rubber-duck |

### Research & Scouting
| Command | Sub-skill | Mục đích |
|---|---|---|
| `/claudekit research <topic>` | `research` | Deep technical research |
| `/claudekit scout <target>` | `scout` | Parallel codebase scan |
| `/claudekit docs-seeker <lib>` | `docs-seeker` | Fetch docs via Context7 |
| `/claudekit repomix <repo>` | `repomix` | Pack repo for AI context |

### Code Quality
| Command | Sub-skill | Mục đích |
|---|---|---|
| `/claudekit code-review <files>` | `code-review` | Comprehensive adversarial review |
| `/claudekit code-reviewer <files>` | `code-reviewer` | Lightweight review |
| `/claudekit simplify-code <files>` | `simplify-code` | Simplify + refactor |

### TDD & Testing
| Command | Sub-skill | Mục đích |
|---|---|---|
| `/claudekit tdd <feature>` | `test-driven-development` | Red-green-refactor cycle |

### Ship
| Command | Sub-skill | Mục đích |
|---|---|---|
| `/claudekit commit` | `commit` | Conventional commits + PR flow |
| `/claudekit docs <action>` | `docs` | Docs management (init/update/summarize) |

## 📂 Toàn bộ 179 skills

Xem: [.claude/skills/claudekit/](../skills/claudekit/) (gitignored, restore bằng `./.claude/skills/restore-claudekit.sh`)

Categories:
- 🏗️ Architecture (7): architect-review, architecture, senior-architect, ...
- 📋 Planning (5): planning-with-files, writing-plans, concise-planning, ...
- 🔍 Research (3): deep-research, search-specialist, reference-builder
- ⚙️ Build (3): build, lint-and-validate, verification-before-completion
- 🧪 Testing (10): tdd-workflow, testing-qa, test-fixing, ...
- ✨ Quality (12): clean-code, code-simplifier, codebase-audit-pre-push, ...
- 🐛 Debug (12): debugging-strategies, error-detective, postmortem-writing, ...
- 📝 Docs (9): documentation, doc-coauthoring, api-documentation, ...
- 🌳 Git/PR (13): create-pr, git-advanced-workflows, iterate-pr, ...
- 🛠️ Skill meta (12): skill-creator, skill-writer, skill-improver, ...
- 🎭 Agents (9): agent-orchestrator, parallel-agents, multi-agent-patterns, ...
- ⚡ Performance (4): performance-engineer, performance-optimizer, ...
- 🔒 Security (6): security-audit, security-scanning-*, ...
- 🔄 Refactor (11): legacy-modernizer, code-refactoring-*, ...
- 📊 Context (13): context-manager, context-optimization, ...
- 🚀 Deploy (7): devops-deploy, deployment-engineer, ...
- ...

## Usage examples

```
/claudekit plan "tích hợp payment gateway"
/claudekit debug "login fails with 500 on production"
/claudekit research "best practices for JWT refresh"
/claudekit code-review src/auth/
/claudekit commit
/claudekit scout "rate limiter patterns in codebase"
```

## Compose với zones khác

- Sau VCI Mode 1 → `/claudekit plan` nếu impl phức tạp
- Sau xia Phase 5 Plan → `/claudekit cook` execute
- Pre-release → `/claudekit code-review` + `/claudekit security-audit`
- Ship → `/claudekit commit` → `/claudekit create-pr`

## Setup yêu cầu

Install claudekit zone:
```bash
./.claude/skills/restore-claudekit.sh          # Linux/macOS
./.claude/skills/restore-claudekit.ps1         # Windows
```
Hoặc: `npm install -g claudekit-cli && ck skills --list`

$ARGUMENTS
