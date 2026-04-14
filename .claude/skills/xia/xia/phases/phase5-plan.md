# Phase 5: 📋 Plan — Implementation roadmap

**Goal:** Convert Challenge decisions → concrete plan với phases, tasks, rollback strategy.

## Compose skills

| Skill | When |
|---|---|
| **`ck:plan --hard`** | Default — full planning với red-team, research context |
| `plan-writing` | Nhẹ hơn — khi scope nhỏ (<5 files) |
| `acceptance-orchestrator` | Khi cần acceptance criteria rigorous |

## Steps

### 5.1. Prepare context package

Gather từ Phase 1-4:

```yaml
source:
  repo: owner/name
  sha: abc1234
  license: MIT
  feature_path: src/auth/
target:
  project: local project name
  stack: [typescript, fastify, prisma, postgres]
  mode: --improve
map:
  file_impact:
    create: [...]
    modify: [...]
    replace: [...]
challenges_resolved:
  env: "pin Node 18"
  deps: "inline utility"
  async: "add throttle"
  state: "rewire Zustand"
  license: "attribution + NOTICE"
  observability: "structured logger mapping"
```

### 5.2. Invoke ck:plan

```bash
ck plan --hard \
  --context .xia/cache/port-context.yaml \
  --output plans/260414-{HHMM}-xia-port-{feature}/ \
  --research-phase skip  # đã research ở Phase 1
```

`ck:plan --hard` sẽ:
1. Apply red-team review trên context
2. Split vào phases (typically 3-5 phases per port)
3. Generate task checklist với verification criteria
4. Output structure chuẩn `plans/{timestamp}-{slug}/`

### 5.3. Customize plan với xia-specific sections

Thêm vào `plan.md`:

#### Rollback strategy

```yaml
rollback:
  branch: xia/port-{feature}-{timestamp}
  checkpoints:
    - phase_01_deps_added
    - phase_02_core_ported
    - phase_03_tests_added
  rollback_command: git reset --hard {phase_X_commit}
  safety_net: no direct push to main
```

#### Attribution plan

List files sẽ nhận attribution header — format qua `scripts/generate-attribution-header.py`.

#### Manifest update plan

```yaml
manifest_entry:
  id: port_{incrementing}
  feature_name: {from user}
  source_repo: {from Recon}
  source_commit: {sha}
  port_date: {today}
  port_mode: {mode}
  files_ported: [list]
  challenges_passed: [list từ Phase 4]
  rollback_commit: {to fill post-deliver}
```

### 5.4. Phase breakdown theo mode

| Mode | Typical phases |
|---|---|
| `--compare` | — (no plan, output report only) |
| `--copy` | P1: Add deps → P2: Copy files + fix imports → P3: Smoke test |
| `--improve` | P1: Add deps → P2: Port core → P3: Refactor to local patterns → P4: Tests → P5: Verify |
| `--port` | P1: Design local equivalent → P2: Implement skeleton → P3: Port logic → P4: Adapt types → P5: Tests → P6: Integration |

### 5.5. Test strategy per mode

| Mode | Test approach |
|---|---|
| `--compare` | N/A |
| `--copy` | Port tests as-is + adapt runner; skip if tests break |
| `--improve` | Port tests + adapt assertions; fix failures inline |
| `--port` | Regenerate tests from source behavior (source tests often framework-specific) |

## Output

Plan folder `plans/260414-HHMM-xia-port-{feature}/`:

```
plans/260414-1430-xia-port-rate-limiter/
├── plan.md                    # Overview + rollback + manifest plan
├── phase-01-add-deps.md
├── phase-02-port-core.md
├── phase-03-refactor-local.md
├── phase-04-tests.md
└── phase-05-verify.md
```

Each phase file follows `documentation-management.md` rules:
- Context Links
- Overview (priority, status)
- Related Code Files
- Implementation Steps
- Todo List
- Success Criteria
- Risk Assessment
- Security Considerations
- Next Steps

→ Proceed to Phase 6 Deliver (invoke `ck:cook`).
